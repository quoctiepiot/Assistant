# Assistant

Trợ lí AI cá nhân giúp quản lý công việc và kế hoạch, theo dõi tiến độ, xếp ưu tiên, và kèm cặp để người dùng tự nâng năng lực quản lý.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `instruction/` | Instruction tổng cho AI trợ lí: bản gốc (v1), bản viết lại (v2, .md và .docx), bản đánh giá |
| `skills/thu-ky-du-an/` | Skill thư ký dự án: đọc kanban/WBS trên Google Drive, nhắc việc theo ma trận Eisenhower, follow-up, lỗ hổng dữ liệu; đọc Agent Hub để báo tiến độ các agent |
| `skills/hub-sync/` | General skill dùng chung 3 repo: state trên Notion Agent Hub, memory trên Drive. Bản copy giống hệt ở NPD-Engineering, Read-thing |

Repo chỉ chứa skill, instruction, hướng dẫn. **Memory** (bài học sau task) nằm trên Google Drive
`AI AGENT DATA/repo_assistant data/memory/`; **state / tiến độ** dùng chung nằm trên Notion **Agent Hub**.
Chi tiết: `skills/hub-sync/`.

## Skill `thu-ky-du-an`

- `SKILL.md`: quy trình, nguyên tắc ưu tiên, mẫu báo cáo (6 chế độ: nhắc hằng ngày, giờ làm gì, hỏi dự án, review tuần, báo tiến độ, việc mới).
- `references/sources.md`: danh sách file Drive (ID, cấu trúc sheet).
- `references/huan-luyen.md`: giai đoạn kèm cặp hiện tại (GĐ1–3), điều kiện chuyển giai đoạn, kho bài học tuần. Bạn tự sửa file này khi chuyển giai đoạn.
- `scripts/scan.py`: đọc file .xlsx/.csv, chuẩn hóa task, gắn cờ quá hạn / nằm im / chờ người khác / lỗi dữ liệu, tìm việc bị sót, tính chỉ số thành công và xu hướng so với 7 và 30 ngày trước từ RECORD DATA.

Chạy thử script:

```bash
pip install openpyxl
python3 -I skills/thu-ky-du-an/scripts/scan.py --today 2026-11-25 tti.xlsx daily.xlsx wbs_pm.xlsx > scan.json
```

Đóng gói để cài vào claude.ai: nén thư mục `skills/thu-ky-du-an/` thành file `.skill` (zip), rồi bấm **Save skill**.

## Ghi chú

- Skill chỉ đọc dữ liệu, không sửa file trên Drive. Ngoại lệ: tạo mục memory mới và ghi Agent Hub theo `hub-sync`;
  tải kết quả lên Drive thành folder / file mới (hỏi trước, tên + ngày theo `skills/hub-sync/references/drive-output.md`).
- Repo đang public và có tên dự án, mã part, ID file Drive, ID Notion Agent Hub (ID không cấp quyền truy cập, nhưng lộ cấu trúc). Không đưa dữ liệu tải từ Drive lên đây (`.gitignore` đã chặn).
