# CLAUDE.md — Assistant

Repo chứa skill, instruction và hướng dẫn cho trợ lí quản lý công việc. Chỉ một mình tôi dùng.

## Dữ liệu không nằm trong repo

| Kho | Ở đâu |
|---|---|
| Kanban, WBS, kế hoạch (nguồn sự thật việc của tôi) | Google Drive, ID ở `skills/thu-ky-du-an/references/sources.md` |
| **Memory** (bài học, quyết định, quy ước rút ra sau task) — riêng repo này | Google Drive `AI-Agent-Data/repo Assistant-Data/memory/` |
| **State / tiến độ** của mọi agent (3 repo) | Notion **Agent Hub** (Tasks, Events, Agents) |

Protocol state + memory: skill `hub-sync` (`skills/hub-sync/SKILL.md`). Tóm tắt:
- Đầu task nhiều bước: tìm Task trùng trên hub, nhận việc bằng lease; đọc memory liên quan.
- Update tiến độ của agent khác (repo khác): chỉ ghi **Event**, không ghi đè Status / Owner / Lease.
- Cuối task: cập nhật hub; ghi memory nếu có điều đáng nhớ. Không ghi memory vào repo.
- Ghi hub / memory không cần hỏi. Dữ liệu chỉ dùng mã, không tên thật supplier / đồng nghiệp, không giá.

## Cách làm việc

- Trả lời tiếng Việt, ngắn, kết luận trước. Instruction tổng: `instruction/Instruction_for_AI_assistant_v2.md`.
- File kết quả (báo cáo nhắc việc, scan.json, xlsx tải về) không lưu vào repo (`.gitignore` đã chặn).
- Repo đang **public**: không đưa dữ liệu tải từ Drive, memory, nội dung hub lên repo.
- `skills/hub-sync/` là bản copy giống hệt ở repo NPD-Engineering và Read-thing: sửa thì sửa cả 3.
- **Luôn hỏi trước** khi commit hoặc push; liệt kê file thay đổi và commit message đề xuất.
