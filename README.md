# Assistant

Trợ lí AI cá nhân giúp quản lý công việc và kế hoạch, theo dõi tiến độ, xếp ưu tiên, và kèm cặp để người dùng tự nâng năng lực quản lý.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `instruction/` | Instruction tổng cho AI trợ lí: bản gốc (v1), bản viết lại (v2, .md và .docx), bản đánh giá |
| `skills/thu-ky-du-an/` | Skill thư ký dự án: đọc kanban/WBS trên Google Drive, nhắc việc theo ma trận Eisenhower, follow-up, lỗ hổng dữ liệu |

## Skill `thu-ky-du-an`

- `SKILL.md`: quy trình, nguyên tắc ưu tiên, mẫu báo cáo (6 chế độ: nhắc hằng ngày, giờ làm gì, hỏi dự án, review tuần, báo tiến độ, việc mới).
- `references/sources.md`: danh sách file Drive (ID, cấu trúc sheet).
- `scripts/scan.py`: đọc file .xlsx/.csv, chuẩn hóa task, gắn cờ quá hạn / nằm im / chờ người khác / lỗi dữ liệu, so bản chụp RECORD DATA.

Chạy thử script:

```bash
pip install openpyxl
python3 -I skills/thu-ky-du-an/scripts/scan.py --today 2026-11-25 tti.xlsx daily.xlsx wbs_pm.xlsx > scan.json
```

Đóng gói để cài vào claude.ai: nén thư mục `skills/thu-ky-du-an/` thành file `.skill` (zip), rồi bấm **Save skill**.

## Ghi chú

- Skill chỉ đọc dữ liệu, không sửa file trên Drive.
- Repo đang public và có tên dự án, mã part, ID file Drive. Không đưa dữ liệu tải từ Drive lên đây (`.gitignore` đã chặn).
