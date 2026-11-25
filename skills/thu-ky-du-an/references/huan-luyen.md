# Kèm cặp năng lực quản lí

Theo instruction v2, mục 7. Người dùng tự sửa file này khi chuyển giai đoạn.
Skill chỉ đọc file này, không tự sửa.

## Giai đoạn hiện tại

**GĐ1**, bắt đầu từ 25/11/2026.

| Giai đoạn | AI làm | Người dùng làm |
|---|---|---|
| GĐ1 | Xếp ưu tiên hằng ngày, lên kế hoạch, giải thích lý do | Đọc lý do. Trong review tuần, tự xếp top 3 trước khi xem cách AI xếp |
| GĐ2 | Nhận xét top 3 của người dùng, bổ sung việc sót và rủi ro. Bản nhắc sáng vẫn đề xuất 3 việc, ghi rõ là để đối chiếu | Mỗi khi hỏi "nên ưu tiên gì", tự xếp top 3 trước |
| GĐ3 | Chỉ kiểm tra việc sót, rủi ro và tính khả thi. Bản nhắc sáng không xếp hộ | Tự lập kế hoạch ngày và tuần |

## Điều kiện chuyển giai đoạn

[Cần bạn chốt] Bản nháp: 4 tuần liền giữ được số việc đang làm thật ≤ 3, 100% việc có deadline,
và top 3 tự xếp trùng với AI ít nhất 2/3 trong 3 lần review tuần gần nhất.
AI chỉ đề xuất chuyển hoặc lùi giai đoạn. Người dùng quyết định.

## Nhật ký kèm cặp

[Cần bạn chốt] Nơi ghi nhật ký, ví dụ một sheet "coaching log" trong Daily Kanban do bạn tự cập nhật,
với các cột: Tuần | Top 3 tự xếp | Top 3 của AI | Số việc trùng | Bài học tuần | Thử gì tuần sau.
Khi sheet này có, script đọc được như mọi sheet khác, và skill dùng nó để theo dõi tỉ lệ trùng.

## Kho bài học tuần

Chọn bài học gắn với dữ liệu thật của tuần đó, không giảng lý thuyết suông. Mỗi bài gồm:
**thói quen lặp lại** (có số liệu) → **vì sao nó gây hại** → **một thay đổi nhỏ để thử tuần sau**.

Các chủ đề hay gặp với dữ liệu hiện tại:
- Ôm nhiều việc cùng lúc (WIP vượt 3): việc nào cũng chậm. Thử: chọn 3 việc, tạm dừng hẳn phần còn lại.
- Việc không có deadline: không có tín hiệu trễ, và việc to luôn thua việc gấp. Thử: mỗi việc mới phải có deadline ngay khi thêm vào kanban.
- Việc nằm ở mình nhưng nằm im lâu: thường do bước tiếp theo mơ hồ. Thử: viết bước tiếp theo bắt đầu bằng động từ.
- Chờ người khác mà không hẹn ngày nhắc lại: bóng lăn mất. Thử: ghi ngày nhắc vào Note khi chuyển sang "Waiting on".
- Kế hoạch ngày bị bỏ dở: dấu hiệu kế hoạch quá tải. Thử: chỉ ghi 3 việc mỗi ngày.
- Kế hoạch không khả thi (khối lượng vượt thời gian): báo sớm, chọn dời mốc hoặc cắt phạm vi ngay thay vì để trượt dần.
