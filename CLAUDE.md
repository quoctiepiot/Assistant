# CLAUDE.md — Assistant

Repo chứa skill, instruction và hướng dẫn cho trợ lí quản lý công việc. Chỉ một mình tôi dùng.

## Dữ liệu không nằm trong repo

| Kho | Ở đâu |
|---|---|
| Kanban, WBS, kế hoạch (nguồn sự thật việc của tôi) | Google Drive, ID ở `skills/thu-ky-du-an/references/sources.md` |
| **Memory** (bài học, quyết định, quy ước rút ra sau task) | Notion **Agent Hub → Memory**, cột `Repo = Assistant` |
| **State / tiến độ** của mọi agent (3 repo) | Notion **Agent Hub** (Tasks, Events, Agents) |

Protocol state + memory: skill `hub-sync`; giao việc / rà các agent / hàng chờ duyệt: skill `dieu-phoi`.
Cả hai **không nằm trong repo này**: nguồn duy nhất là repo private `agent-core`, cài ở claude.ai Settings → Skills.
Tóm tắt:
- Đầu task nhiều bước (hoặc được giao `HUB-n`): đọc / nhận Task bằng lease; đọc memory liên quan.
- Update tiến độ của agent khác (repo khác): chỉ ghi **Event**, không ghi đè Status / Owner / Lease.
- Cuối task: cập nhật hub (`Duyệt = cần duyệt` → `review`, `không cần` → `done`); ghi memory nếu có điều đáng nhớ.
  Không ghi memory vào repo.
- Ghi hub / memory không cần hỏi. Dữ liệu chỉ dùng mã, không tên thật supplier / đồng nghiệp, không giá.

## Cách làm việc

- Trả lời tiếng Việt, ngắn, kết luận trước. Instruction tổng: `instruction/Instruction_for_AI_assistant_v2.md`.
- File kết quả (báo cáo nhắc việc, scan.json, xlsx tải về) không lưu vào repo (`.gitignore` đã chặn).
- Repo đang **public**: không đưa dữ liệu tải từ Drive, memory, nội dung hub lên repo.
- Không thêm ID Notion / Drive mới vào repo (repo public); ID nằm trong skill `hub-sync` đã cài.
- **Git:** agent tự commit và push lên **nhánh riêng**, rồi mở PR, không cần hỏi. Không push thẳng `main`,
  không tự merge. Tôi duyệt khi merge. Mô tả PR liệt kê file thay đổi và lý do.
