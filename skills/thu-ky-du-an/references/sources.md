# Nguồn dữ liệu dự án (Google Drive)

Đây là danh sách file mà thư ký đọc mỗi lần chạy. Khi người dùng tạo thêm kanban/WBS mới,
hãy đề xuất họ bổ sung vào bảng này (skill không tự sửa file này trong lúc chạy nhắc việc).

| Khóa | Tên file trên Drive | File ID | Vai trò |
|---|---|---|---|
| tti | Kanban TTI | `12nW0-RZJI7YkymfhWd6nyPJIfe1QYlOFdUycoAgl_G8` | Kanban công việc ở công ty (nhiều dự án NPD song song) |
| daily | Daily Kanban | `1GHO6MMoIU0QMU6yMy2ODpcH_d2mhyZMPwe57JxXObHw` | Kanban cá nhân: Skill, Gia đình, Tài chính, Công việc + danh mục dự án + nhật ký hoạt động |
| wbs_pm | WBS_ project management | `1vDdwCrphABtnR7CQZfUwEUsy4r8ixrPbmdIQQgNCF2g` | WBS lộ trình học quản lý dự án, mốc 15/12/2026 |

Nếu một ID không mở được (file bị đổi/xóa), tìm lại bằng `search_files` với
`title contains '<tên>'` và báo cho người dùng ID mới để cập nhật bảng.

Tìm thêm (không bắt buộc, dùng khi review tuần hoặc khi người dùng hỏi):
- File WBS / plan khác: `search_files` với `title contains 'WBS' or title contains 'plan'`, sắp theo `modifiedTime desc`.
- Việc được giao qua comment trên Drive: `search_files` với `followUp = 'actionitems'`; đây là nguồn
  việc dễ bị sót vì không nằm trên kanban.
- Thư mục dự án dùng cấu trúc chuẩn `00_PLAN & ADMIN`, `01_DESIGN`, `02_TEST & VALIDATION`,
  `03_FAI`, `04_ISSUE & ANALYSIS`, `05_MEASUREMENT`, `06_LOGISTICS`. File mới trong `04_ISSUE & ANALYSIS`
  hoặc `03_FAI` thường báo hiệu việc mới phát sinh.

## Cấu trúc đã biết (để hiểu dữ liệu, script tự nhận dạng theo tiêu đề cột)

### Kanban TTI
- `Kanban table` (trạng thái hiện tại): Project | Task | Status | Start | Deadline | Finish | Waiting on | Note | Time (day).
  Cột Project chỉ ghi ở dòng đầu nhóm và có các dòng trống phân cách. Status: `Not Start`, `In Progress`, `Done`.
  `Waiting on` là người/bên đang giữ bóng (Theo, Eugene, YUDA, SGS, Lab, Anotech...).
- `RECORD DATA`: bản chụp tự động mỗi ngày của Kanban table (có cột Date). Dùng để biết task nằm im bao lâu
  và đã thay đổi gì trong tuần.
- `estimate plan`: kế hoạch theo ngày, mỗi khối bắt đầu bằng hàng `Project | Việc | <Thứ m/d>`; cột kế bên ghi `done` / `push out`.
  Ngày trong sheet này và trong ghi chú viết kiểu Mỹ **m/d** (vd `Wed 11/11`, `chờ result < 11/25`).

### Daily Kanban
- `Kanban table`: # | Project/Program | Việc | Trạng thái | Ghi chú | Start date | Finish date | Period | Deadline.
- `project list`: Category | Title | Type (Project/Program) | Deadline (kiểu **dd/mm/yyyy**). Đây là mốc lớn của từng mục tiêu.
- `activity log`: Ngày | Gói công việc đã làm | note.
- `RECORD DATA`: bản chụp hằng ngày, tiêu đề cột là DATA1..DATA9 theo thứ tự cột của Kanban table.
- `DATA TABLE` đang có nhiều ô `#REF!`: đây là lỗi công thức, nên nhắc người dùng sửa.

### WBS_ project management
- `WBS`: phần đầu có Project / Target / Milestone; bảng: id | name | owner | duration (day) | preds | Loại (Nhóm/Việc) | Đầu ra | Xong khi | Trạng thái (`Xong` / `Chưa làm`).
- Phần dưới bảng (Thực hành tuần 1-12, Đo lường & cải tiến...) là kế hoạch phụ của dự án "Cải thiện chất lượng suy nghĩ", chưa có id/trạng thái.

## Agent Hub và memory

Cả hai nằm trên Notion **Agent Hub** (Tasks, Events, Agents, Memory). ID và cách đọc / ghi: skill `hub-sync`
(`references/hub-schema.md`, `references/memory.md` trong skill đã cài; nguồn ở repo private `agent-core`).
Repo này public nên không chép ID vào đây.

Memory của thư ký: database Memory, `Repo = Assistant`, `Mảng = project`. Tìm bài học tuần trước:
filter `Repo = Assistant`, `Loại = lesson`, `Trạng thái = mở`, sort `Ngày` descending.
