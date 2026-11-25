#!/usr/bin/env python3
"""Quét file kanban / WBS (.xlsx hoặc .csv) và in ra JSON gọn cho agent thư ký.

Cách dùng:
    python3 -I scan.py --today 2026-11-25 file1.xlsx file2.xlsx ...
    python3 -I scan.py --today 2026-11-25 --window 7 --stale 7 --soon 3 --wip 3 *.xlsx

Script tự nhận dạng sheet theo tiêu đề cột, không cần cấu hình:
  - Sheet kanban : có cột Task/Việc và Status/Trạng thái
  - Sheet RECORD : có cột Date/DATE ở cột đầu + cột việc (hoặc DATA1..N) -> bản chụp hằng ngày
  - Sheet WBS    : có hàng tiêu đề chứa 'id' và 'preds'
  - Sheet nhật ký: có cột 'Ngày' + 'Gói công việc'
  - Sheet plan   : hàng có 'Project' | 'Việc' | '<Thứ> m/d' (estimate plan)
  - Sheet danh mục dự án: có cột Category + Title (+ Deadline)

Chỉ ĐỌC file, không ghi gì ra ngoài stdout.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import unicodedata

try:
    import openpyxl
except ImportError:  # pragma: no cover
    openpyxl = None

# ---------------------------------------------------------------- helpers

def norm(s):
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s)


ALIASES = {
    "project": ["project", "project/program", "dự án", "du an", "category"],
    "task": ["task", "việc", "name", "title", "công việc"],
    "status": ["status", "trạng thái", "trang thai"],
    "start": ["start", "start date", "ngày bắt đầu"],
    "deadline": ["deadline", "hạn", "due", "due date", "milestone"],
    "finish": ["finish", "finish date", "ngày xong"],
    "waiting": ["waiting on", "chờ", "waiting"],
    "note": ["note", "ghi chú", "ghi chu", "notes"],
    "period": ["time (day)", "period", "period(date)", "duration (day)"],
    "date": ["date", "ngày"],
    "id": ["#", "id"],
    "owner": ["owner", "người", "pic"],
    "preds": ["preds", "predecessors", "phụ thuộc"],
    "kind": ["loại", "type"],
    "deliverable": ["đầu ra/deliverables", "deliverables", "đầu ra"],
    "done_when": ["xong khi", "definition of done"],
    "priority": ["priority", "ưu tiên", "uu tien", "quan trọng"],
}


def field_of(header):
    h = norm(header)
    for f, names in ALIASES.items():
        if h in names:
            return f
    return None


ERR_RE = re.compile(r"^#(ref|value|n/a|div/0|name|num|null)[!?]?", re.I)


def is_err(v):
    return isinstance(v, str) and bool(ERR_RE.match(v.strip()))


def parse_date(v):
    """Trả về (date|None, lỗi: bool). Hiểu datetime, YYYY-MM-DD, dd/mm/yyyy."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return None, False
    if isinstance(v, dt.datetime):
        return v.date(), False
    if isinstance(v, dt.date):
        return v, False
    s = str(v).strip()
    if is_err(s):
        return None, True
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        try:
            return dt.date(int(m[1]), int(m[2]), int(m[3])), False
        except ValueError:
            return None, True
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)  # dd/mm/yyyy (kiểu VN)
    if m:
        try:
            return dt.date(int(m[3]), int(m[2]), int(m[1])), False
        except ValueError:
            return None, True
    return None, True


def clean(v):
    if v is None:
        return ""
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


def status_kind(s):
    n = norm(s)
    if not n:
        return "blank"
    if n in ("done", "xong", "hoàn thành", "completed", "closed"):
        return "done"
    if n in ("in progress", "đang làm", "doing", "wip", "ongoing"):
        return "doing"
    if n in ("not start", "not started", "not start ", "chưa làm", "todo", "to do", "chờ"):
        return "todo"
    if n in ("cancel", "cancelled", "hủy", "huỷ", "drop", "rejected"):
        return "cancelled"
    if n in ("waiting", "on hold", "hold", "chờ bên khác", "blocked"):
        return "waiting"
    return "other:" + n


DATE_IN_NOTE = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?(?![\d/])")


def dates_in_note(note, today):
    """Bắt các mốc kiểu '< 11/25', '11/2-11/9' trong ghi chú (m/d theo thói quen file)."""
    out = []
    for m in DATE_IN_NOTE.finditer(note or ""):
        a, b, y = int(m[1]), int(m[2]), m[3]
        year = int(y) if y else today.year
        if year < 100:
            year += 2000
        for mo, d in ((a, b), (b, a)):  # thử m/d trước, rồi d/m
            try:
                out.append(dt.date(year, mo, d).isoformat())
                break
            except ValueError:
                continue
    return out

# ---------------------------------------------------------------- loading

def load_tables(path):
    """Trả về list (sheet_name, rows[list[list]])."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, newline="", encoding="utf-8-sig") as f:
            return [(os.path.basename(path), [list(r) for r in csv.reader(f)])]
    if openpyxl is None:
        raise SystemExit("Thiếu openpyxl: pip install openpyxl")
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        rows = []
        for r in ws.iter_rows(values_only=True):
            rows.append(list(r))
        # bỏ đuôi rỗng
        while rows and not any(c not in (None, "") for c in rows[-1]):
            rows.pop()
        out.append((ws.title, rows))
    return out


def find_header(rows, must, limit=15):
    for i, r in enumerate(rows[:limit]):
        fields = [field_of(c) for c in r]
        if all(m in fields for m in must):
            return i, fields
    return None, None

# ---------------------------------------------------------------- parsers

def parse_kanban(rows, hi, fields, today, src, sheet):
    tasks = []
    current_project = ""
    for r in rows[hi + 1:]:
        rec = {}
        for j, f in enumerate(fields):
            if f and j < len(r) and f not in rec:
                rec[f] = r[j]
        proj = clean(rec.get("project"))
        if proj:
            current_project = proj
        task = clean(rec.get("task"))
        status_raw = clean(rec.get("status"))
        if not task:
            if status_raw:  # có trạng thái mà không có tên việc
                tasks.append({"source": src, "sheet": sheet, "project": proj or current_project,
                              "task": "(trống tên việc)", "status": status_raw,
                              "status_kind": status_kind(status_raw), "flags": ["data_error:thiếu tên việc"]})
            continue
        t = {"source": src, "sheet": sheet, "project": proj or current_project, "task": task,
             "status": status_raw, "status_kind": status_kind(status_raw),
             "waiting_on": clean(rec.get("waiting")), "note": clean(rec.get("note")),
             "owner": clean(rec.get("owner")), "priority": clean(rec.get("priority")), "flags": []}
        if rec.get("id") not in (None, ""):
            t["id"] = clean(rec.get("id"))
        for f in ("start", "deadline", "finish"):
            d, err = parse_date(rec.get(f))
            t[f] = d.isoformat() if d else ""
            if err:
                t["flags"].append(f"data_error:{f} không đọc được ({clean(rec.get(f))})")
        if is_err(clean(rec.get("period"))):
            t["flags"].append(f"data_error:cột thời gian lỗi ({clean(rec.get('period'))})")
        for f in ("task", "status", "note", "project"):
            if is_err(t.get(f, "")):
                t["flags"].append(f"data_error:{f} = {t[f]}")
        tasks.append(t)
    return tasks


def parse_record(rows, hi, kanban_fields_by_sheet):
    """Bản chụp hằng ngày. Trả về list dict có date + các field."""
    header = rows[hi]
    fields = [field_of(c) for c in header]
    # Trường hợp header là DATA1..N -> ánh xạ theo thứ tự cột kanban (bỏ cột rỗng)
    if any(re.match(r"^data\d+$", norm(c)) for c in header if c):
        base = [f for f in (kanban_fields_by_sheet or []) if f]
        fields = []
        for c in header:
            m = re.match(r"^data(\d+)$", norm(c))
            if m and int(m[1]) - 1 < len(base):
                fields.append(base[int(m[1]) - 1])
            else:
                fields.append(field_of(c))
    snaps = []
    for r in rows[hi + 1:]:
        rec = {}
        for j, f in enumerate(fields):
            if f and j < len(r) and f not in rec:
                rec[f] = r[j]
        d, _ = parse_date(rec.get("date"))
        task = clean(rec.get("task"))
        if not d or not task:
            continue
        snaps.append({"date": d, "project": clean(rec.get("project")), "task": task,
                      "status": clean(rec.get("status")), "waiting": clean(rec.get("waiting")),
                      "note": clean(rec.get("note")), "deadline": clean(rec.get("deadline"))})
    return snaps


def parse_wbs(rows, today, src, sheet):
    hi, fields = find_header(rows, ["id", "preds"], limit=30)
    meta = {}
    for r in rows[:hi]:
        if r and r[0] not in (None, "") and len(r) > 1 and r[1] not in (None, ""):
            meta[clean(r[0]).rstrip(":")] = clean(r[1])
    items = []
    for r in rows[hi + 1:]:
        rec = {f: r[j] for j, f in enumerate(fields) if f and j < len(r)}
        _id = clean(rec.get("id"))
        if not _id or not re.match(r"^\d+(\.\d+)*$", _id):
            continue
        dur = rec.get("period")
        try:
            dur = float(dur)
        except (TypeError, ValueError):
            dur = None
        items.append({"id": _id, "name": clean(rec.get("task")), "kind": clean(rec.get("kind")),
                      "status": clean(rec.get("status")), "status_kind": status_kind(rec.get("status")),
                      "preds": [p.strip() for p in re.split(r"[,;]", clean(rec.get("preds"))) if p.strip()],
                      "duration": dur, "owner": clean(rec.get("owner")),
                      "done_when": clean(rec.get("done_when"))})
    leaves = [i for i in items if norm(i["kind"]) != "nhóm"]
    done_ids = {i["id"] for i in leaves if i["status_kind"] == "done"}
    by_id = {i["id"]: i for i in items}
    next_up, blocked = [], []
    for i in leaves:
        if i["status_kind"] == "done":
            continue
        missing = [p for p in i["preds"] if p not in done_ids]
        entry = {"id": i["id"], "name": i["name"], "duration": i["duration"], "done_when": i["done_when"]}
        if missing:
            entry["waiting_for"] = missing
            blocked.append(entry)
        else:
            next_up.append(entry)
    # đếm số việc phụ thuộc vào mỗi việc (để ước lượng mức quan trọng)
    dependents = {}
    for i in leaves:
        for p in i["preds"]:
            dependents[p] = dependents.get(p, 0) + 1
    for e in next_up + blocked:
        e["dependents"] = dependents.get(e["id"], 0)
    remaining = sum(i["duration"] or 0 for i in leaves if i["status_kind"] != "done")
    milestone = None
    for k, v in meta.items():
        if norm(k) in ("milestone", "deadline"):
            d, _ = parse_date(v)
            milestone = d
    res = {"source": src, "sheet": sheet, "project": meta.get("Project", ""),
           "target": meta.get("Target", ""),
           "milestone": milestone.isoformat() if milestone else "",
           "done": len(done_ids), "total": len(leaves),
           "remaining_duration_days": remaining,
           "next_actionable": next_up, "blocked_by_preds": blocked[:8]}
    if milestone:
        days_left = (milestone - today).days
        res["days_to_milestone"] = days_left
        # ngày làm việc còn lại (T2-T6)
        wd = sum(1 for k in range(max(days_left, 0)) if (today + dt.timedelta(days=k + 1)).weekday() < 5)
        res["workdays_to_milestone"] = wd
        res["schedule_risk"] = remaining > wd
    return res


def parse_log(rows, hi):
    out = []
    for r in rows[hi + 1:]:
        d, _ = parse_date(r[0] if r else None)
        if d and len(r) > 1 and r[1]:
            out.append({"date": d.isoformat(), "what": clean(r[1]),
                        "note": clean(r[2]) if len(r) > 2 else ""})
    return out


def parse_plan(rows):
    """estimate plan: trả về nhãn ngày cuối cùng + các việc của ngày đó."""
    blocks = []
    for i, r in enumerate(rows):
        if r and norm(r[0]) == "project" and len(r) > 2 and norm(r[1]) == "việc":
            labels = [clean(c) for c in r[2:] if c not in (None, "")]
            blocks.append((i, labels))
    if not blocks:
        return None
    i, labels = blocks[-1]
    items = []
    for r in rows[i + 1:]:
        if r and norm(r[0]) == "project":
            break
        if any(c not in (None, "") for c in r[2:]):
            cells = [clean(c) for c in r[2:] if c not in (None, "")]
            items.append({"project": clean(r[0]), "task": clean(r[1]),
                          "plan": " | ".join(c for c in cells if norm(c) != "done"),
                          "done": any(norm(c) == "done" for c in cells)})
    return {"last_plan_label": " / ".join(labels), "items": items[:25]}


def parse_project_list(rows, hi, fields):
    out = []
    for r in rows[hi + 1:]:
        rec = {f: r[j] for j, f in enumerate(fields) if f and j < len(r)}
        title = clean(rec.get("task"))
        if not title:
            continue
        d, _ = parse_date(rec.get("deadline"))
        out.append({"category": clean(rec.get("project")), "title": title,
                    "type": clean(rec.get("kind")), "deadline": d.isoformat() if d else ""})
    return out

# ---------------------------------------------------------------- analysis

def analyse_history(tasks, snaps, today, window):
    """Gắn days_unchanged cho task + trả về các thay đổi trong `window` ngày."""
    hist = {}
    for s in snaps:
        hist.setdefault((norm(s["project"]), norm(s["task"])), []).append(s)
    changes = []
    last_snapshot = max((s["date"] for s in snaps), default=None)
    for key, lst in hist.items():
        lst.sort(key=lambda s: s["date"])
        # gộp theo ngày (lấy bản cuối của ngày)
        per_day = {}
        for s in lst:
            per_day[s["date"]] = s
        days = sorted(per_day)
        prev = None
        for d in days:
            cur = per_day[d]
            if prev is not None and (today - d).days <= window:
                for f in ("status", "waiting", "note"):
                    if norm(prev[f]) != norm(cur[f]):
                        changes.append({"date": d.isoformat(), "project": cur["project"], "task": cur["task"],
                                        "field": f, "from": prev[f], "to": cur[f]})
            prev = cur
    for t in tasks:
        key = (norm(t["project"]), norm(t["task"]))
        lst = hist.get(key)
        if not lst:
            continue
        per_day = {}
        for s in lst:
            per_day[s["date"]] = s
        days = sorted(per_day)
        sig = lambda s: (norm(s["status"]), norm(s["waiting"]), norm(s["note"]))
        cur_sig = (norm(t["status"]), norm(t.get("waiting_on", "")), norm(t.get("note", "")))
        since = None
        for d in reversed(days):
            if sig(per_day[d]) == cur_sig:
                since = d
            else:
                break
        if since is None:  # khác bản chụp cuối -> vừa được cập nhật sau lần chụp
            t["days_unchanged"] = 0
        else:
            t["days_unchanged"] = (today - since).days
            t["unchanged_since"] = since.isoformat()
        t["first_seen"] = days[0].isoformat()
    return changes, (last_snapshot.isoformat() if last_snapshot else "")


def snapshot_metrics(snaps, target):
    """Chỉ số tại bản chụp gần nhất <= target (để so xu hướng mà không cần lưu gì)."""
    days = sorted({s["date"] for s in snaps if s["date"] <= target})
    if not days:
        return None
    d = days[-1]
    rows = {}
    for s in snaps:
        if s["date"] == d:
            rows[(norm(s["project"]), norm(s["task"]))] = s
    open_rows = [s for s in rows.values() if status_kind(s["status"]) not in ("done", "cancelled")]
    with_dl = sum(1 for s in open_rows if parse_date(s.get("deadline"))[0])
    active = sum(1 for s in open_rows if status_kind(s["status"]) == "doing" and not norm(s["waiting"]))
    return {"date": d.isoformat(), "open": len(open_rows), "with_deadline": with_dl, "doing_active": active}


def flag_tasks(tasks, today, soon, stale):
    for t in tasks:
        k = t["status_kind"]
        if k in ("done", "cancelled"):
            continue
        fl = t["flags"]
        if k == "blank":
            fl.append("no_status")
        if k.startswith("other:"):
            fl.append(f"status_lạ:{t['status']}")
        if t.get("deadline"):
            dd = dt.date.fromisoformat(t["deadline"])
            delta = (dd - today).days
            t["days_to_deadline"] = delta
            if delta < 0:
                fl.append("overdue")
            elif delta <= soon:
                fl.append("due_soon")
            if t.get("start") and dd < dt.date.fromisoformat(t["start"]):
                fl.append("data_error:deadline trước ngày start")
        else:
            fl.append("no_deadline")
        if t.get("start"):
            t["age_days"] = (today - dt.date.fromisoformat(t["start"])).days
            if t["age_days"] >= 30:
                fl.append("long_running")
            if t["age_days"] < 0 and k == "doing":
                fl.append("data_error:start ở tương lai")
        elif k == "doing":
            fl.append("no_start")
        w = norm(t.get("waiting_on"))
        if w:
            if w in ("rejected", "cancel", "hold", "done"):
                fl.append(f"waiting_on_bất_thường:{t['waiting_on']}")
            else:
                fl.append("waiting_external")
        if t.get("days_unchanged", 0) >= stale:
            fl.append("stale")
        nd = dates_in_note(t.get("note"), today)
        if nd:
            t["dates_in_note"] = nd
            if any(dt.date.fromisoformat(x) <= today + dt.timedelta(days=soon) for x in nd):
                fl.append("note_date_due")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--window", type=int, default=7, help="số ngày lấy lịch sử thay đổi")
    ap.add_argument("--stale", type=int, default=7, help="số ngày không đổi thì coi là nằm im")
    ap.add_argument("--soon", type=int, default=3, help="số ngày tới hạn thì coi là gấp")
    ap.add_argument("--wip", type=int, default=3, help="giới hạn số việc đang làm")
    ap.add_argument("--project", default="", help="lọc theo tên dự án (chứa chuỗi)")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)

    out = {"today": a.today, "weekday": ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][today.weekday()],
           "sources": [], "tasks": [], "wbs": [], "recent_changes": [], "activity_log_tail": [],
           "project_list": [], "plans": [], "warnings": []}

    for path in a.files:
        src = os.path.splitext(os.path.basename(path))[0]
        try:
            tables = load_tables(path)
        except Exception as e:  # noqa
            out["warnings"].append(f"{src}: không mở được ({e})")
            continue
        info = {"file": src, "sheets": []}
        kanban_tasks, kanban_fields, snaps = [], None, []
        record_sheets = []
        for name, rows in tables:
            kind = None
            if find_header(rows, ["id", "preds"], limit=30)[0] is not None:
                kind = "wbs"
                try:
                    out["wbs"].append(parse_wbs(rows, today, src, name))
                except Exception as e:  # noqa
                    out["warnings"].append(f"{src}/{name}: lỗi đọc WBS ({e})")
            hi, fields = (None, None) if kind else find_header(rows, ["task", "status"])
            first = norm(rows[hi][0]) if hi is not None and rows[hi] else ""
            if hi is not None and first not in ("date",) and "date" not in fields[:1]:
                kind = "kanban"
                if kanban_fields is None or "kanban" in norm(name):
                    kanban_fields = fields
                kanban_tasks += parse_kanban(rows, hi, fields, today, src, name) if ("kanban" in norm(name) or not kanban_tasks) else []
            if kind is None:
                for i, r in enumerate(rows[:5]):
                    if r and norm(r[0]) == "date" and len(r) > 2:
                        kind = "record"
                        record_sheets.append((name, rows, i))
                        break
            if kind is None:
                for i, r in enumerate(rows[:3]):
                    if r and norm(r[0]) == "ngày" and len(r) > 1 and "gói công việc" in norm(r[1]):
                        kind = "log"
                        out["activity_log_tail"] += [dict(x, source=src) for x in parse_log(rows, i)[-10:]]
                        break
            if kind is None:
                p = parse_plan(rows)
                if p:
                    kind = "plan"
                    p["source"] = src
                    out["plans"].append(p)
            if kind is None:
                h2, f2 = find_header(rows, ["task", "project"])
                if h2 is not None and norm(rows[h2][0]) == "category":
                    kind = "project_list"
                    out["project_list"] += [dict(x, source=src) for x in parse_project_list(rows, h2, f2)]
            info["sheets"].append({"name": name, "kind": kind or "bỏ qua", "rows": len(rows)})
        for name, rows, i in record_sheets:
            snaps += parse_record(rows, i, kanban_fields)
        changes, last_snap = analyse_history(kanban_tasks, snaps, today, a.window)
        info["last_snapshot"] = last_snap
        if snaps:
            last = dt.date.fromisoformat(last_snap)
            info["trend"] = {"latest": snapshot_metrics(snaps, last),
                             "7_days_ago": snapshot_metrics(snaps, last - dt.timedelta(days=7)),
                             "30_days_ago": snapshot_metrics(snaps, last - dt.timedelta(days=30))}
        out["recent_changes"] += [dict(c, source=src) for c in changes]
        out["tasks"] += kanban_tasks
        out["sources"].append(info)

    flag_tasks(out["tasks"], today, a.soon, a.stale)
    if a.project:
        q = norm(a.project)
        out["tasks"] = [t for t in out["tasks"] if q in norm(t["project"])]
        out["recent_changes"] = [c for c in out["recent_changes"] if q in norm(c["project"])]

    open_tasks = [t for t in out["tasks"] if t["status_kind"] not in ("done", "cancelled")]
    summary = {"open": len(open_tasks), "by_source": {}}
    for t in open_tasks:
        s = summary["by_source"].setdefault(t["source"], {"open": 0, "doing": 0, "doing_active": 0})
        s["open"] += 1
        s["doing"] += t["status_kind"] == "doing"
        # việc "đang làm" mà không chờ ai = việc thực sự nằm trên tay mình
        s["doing_active"] += t["status_kind"] == "doing" and "waiting_external" not in t["flags"]
    for k in ("overdue", "due_soon", "note_date_due", "stale", "waiting_external", "no_deadline", "long_running"):
        summary[k] = sum(1 for t in open_tasks if k in t["flags"])
    summary["data_errors"] = sum(1 for t in out["tasks"] if any(f.startswith("data_error") for f in t["flags"]))
    summary["wip_limit"] = a.wip
    summary["wip_over"] = {s: v["doing_active"] for s, v in summary["by_source"].items() if v["doing_active"] > a.wip}
    # Việc sót: có trong kế hoạch ngày gần nhất, chưa done, không có trên kanban
    known = {norm(t["task"]) for t in out["tasks"]}
    omissions = []
    for p in out["plans"]:
        for it in p.get("items", []):
            if it.get("done"):
                continue
            if it["task"] and norm(it["task"]) in known:
                continue
            omissions.append({"source": p["source"], "plan_date": p["last_plan_label"],
                              "project": it["project"], "task": it["task"], "plan": it["plan"]})
    out["omissions"] = omissions
    # Chỉ số thành công (instruction v2, mục 2)
    metrics = {"deadline_coverage": {}, "doing_active_total": sum(v["doing_active"] for v in summary["by_source"].values()),
               "wip_limit": a.wip,
               "stale_14_open": sum(1 for t in open_tasks if t.get("days_unchanged", 0) >= 14),
               "omissions": len(omissions),
               "wbs_feasibility": [{"project": w["project"], "remaining_days": w["remaining_duration_days"],
                                    "workdays_left": w.get("workdays_to_milestone"),
                                    "feasible": not w.get("schedule_risk", False)} for w in out["wbs"]]}
    for src in summary["by_source"]:
        rows = [t for t in open_tasks if t["source"] == src and t["task"] != "(trống tên việc)"]
        metrics["deadline_coverage"][src] = f'{sum(1 for t in rows if t.get("deadline"))}/{len(rows)}'
    summary["metrics"] = metrics
    out["summary"] = summary
    # bỏ task đã xong khỏi output cho gọn (giữ số đếm)
    out["done_count"] = len(out["tasks"]) - len(open_tasks)
    out["tasks"] = open_tasks
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
