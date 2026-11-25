# Đánh giá "Instruction for AI assistant" (bản gốc)

Bản gốc: `Instruction for AI assistant.docx` (4 đoạn: Background, Mục đích, Vai trò, Việc cần làm).
Bản viết lại: `Instruction_for_AI_assistant_v2.docx` / `.md`.

## 1. Bảng điểm

| # | Tiêu chí | Điểm (1–5) | Nhận xét ngắn |
|---|---|---|---|
| 1 | Rõ mục tiêu & tiêu chí thành công | 2 | Hướng đúng, nhưng không có tiêu chí đo được |
| 2 | Phạm vi & ranh giới | 1 | Không nói AI được / không được làm gì, quyền đọc / ghi, dữ liệu công ty |
| 3 | Nguồn dữ liệu & cách làm việc | 1 | Không nói đọc ở đâu, chạy khi nào |
| 4 | Nâng cao năng lực, không phụ thuộc AI | 2 | Ý định rất tốt, nhưng chưa có cơ chế nào |
| 5 | Phong cách giao tiếp & định dạng | 1 | Chưa có |
| 6 | Khả năng hành động của AI | 2 | AI khác đọc xong chưa biết bắt đầu từ đâu; có chỗ mơ hồ, lệch vai |
| 7 | Thiếu sót so với bối cảnh thực tế | 1 | Chưa phản ánh Eisenhower, WIP, chỉ đọc, lịch 7:40, các lỗ hổng dữ liệu đã thấy |
| | **Tổng quan** | **≈ 1,4 / 5** | Định hướng tốt, nhưng mới là bản ý tưởng, chưa phải instruction để AI làm theo |

## 2. Điểm tốt nên giữ

- **"Tập trung vào các công việc trọng yếu thay vì quản lí toàn bộ công việc nhưng không việc nào tới nơi tới chốn."** Đây là chẩn đoán đúng, và khớp với dữ liệu thật (13 việc đang làm cùng lúc, nhiều việc nằm im 30+ ngày). Bản mới giữ câu này làm trục chính (mục 1, mục 6 "Tập trung").
- **"Nâng cao năng lực quản lí, để không phụ thuộc hoàn toàn vào AI."** Đây là điểm hay nhất của bản gốc: rất ít người đặt mục tiêu này cho trợ lí AI. Bản mới biến nó thành cả một mục có cơ chế (mục 7).
- **"Lên kế hoạch thực hiện công việc để người dùng thực thi."** Phân vai đúng: AI lập kế hoạch và giám sát, người dùng làm. Bản mới giữ và nói rõ hơn ranh giới (mục 3).
- Có tách ngắn hạn / dài hạn, và có ý "xây dựng 1 thói quen quản lí". Hai ý này được giữ qua nhịp ngày / tuần / tháng.

## 3. Nhận xét chi tiết theo tiêu chí

### 3.1 Mục tiêu & tiêu chí thành công (2/5)
- "tăng cường hiệu quả", "theo dõi tiến độ, đánh giá tiến độ, achievement" đều đúng ý nhưng không đo được. AI không biết lúc nào mình làm tốt hay chưa.
- Thiếu định nghĩa "trợ lí làm tốt". Bản mới thêm bảng chỉ số có mốc hiện tại: việc có deadline (0/27), WIP thật (13 so với ≤ 3), việc nằm im, việc bị sót, kế hoạch khả thi (WBS học PM: 63 ngày công so với 14 ngày làm việc).

### 3.2 Phạm vi & ranh giới (1/5)
- Không có chữ nào về quyền đọc / ghi. Người dùng đã chốt "AI chỉ đọc + đề xuất" nhưng instruction chưa ghi, nên AI khác có thể tự sửa kanban.
- Không nói về dữ liệu công ty (mã part, supplier, đồng nghiệp) và dữ liệu cá nhân nhạy cảm (nợ, tìm việc).
- Không nói ai quyết những việc lớn (dời mốc, dừng dự án). Bản mới: AI đưa phương án, người dùng quyết.

### 3.3 Nguồn dữ liệu & nhịp làm việc (1/5)
- "AI nằm thời khóa biểu làm việc, kế hoạch của người dùng" (nhiều khả năng là "nắm"): không nói thời khóa biểu nằm ở đâu. Thực tế có 3 file Google Sheets và cấu trúc thư mục dự án.
- Không có nhịp: hằng ngày lúc nào, có review tuần / tháng không. Bản mới thêm bảng nhịp, trỏ sang skill thay vì chép chi tiết.

### 3.4 Cơ chế "nâng cao năng lực, không phụ thuộc AI" (2/5)
- Có mục tiêu ("Xây dựng 1 thói quen quản lí để người dùng cải thiện năng lực quản lí") nhưng không có cách làm. Nếu không có cơ chế, AI sẽ mặc định làm hộ mọi thứ, tức là tăng phụ thuộc, ngược với mục tiêu.
- Bản mới thêm 5 cơ chế: luôn nói lý do; người dùng xếp trước, AI so sau; mỗi tuần một bài học gắn dữ liệu thật; giảm dần hỗ trợ qua 3 giai đoạn; đo tiến bộ hằng tháng.

### 3.5 Phong cách giao tiếp & định dạng (1/5)
- Không nói ngôn ngữ, độ dài, xưng hô, cách nói khi có tin xấu, ngôn ngữ cho tin nhắn gửi đồng nghiệp nước ngoài. Bản mới thêm mục 8, khớp với cách skill thu-ky-du-an đang viết.

### 3.6 Khả năng hành động (2/5)
- **Câu chỉ dẫn duy nhất là lệnh "meta":** "AI sẽ xây dựng những skill liên quan tới kĩ năng trợ lí". Đây là việc cần làm một lần (và đã làm: thu-ky-du-an), không phải hướng dẫn cho AI mỗi lần làm việc. Bản mới đổi thành "Danh mục skill": skill nào đã có, skill nào nên làm tiếp và theo thứ tự nào.
- **Lệch vai nhẹ:** "Vai trò: … chủ yếu giám sát tiến độ, kế hoạch" trong khi "Mục đích" còn gồm lên kế hoạch, đánh giá và xây thói quen. Bản mới gộp: trợ lí kiêm người kèm cặp.
- **Câu bối cảnh tự hạ thấp:** "Người dùng không có năng lực quản lí tác vụ như AI" dễ khiến AI làm thay thay vì kèm cặp, và không mô tả đúng vấn đề. Vấn đề thật là khối lượng vượt khả năng theo dõi bằng trí nhớ. Bản mới viết lại theo hướng đó.
- Lỗi chính tả "nằm" → "nắm"; trộn "achievement" giữa câu tiếng Việt (giữ lại, kèm nghĩa "kết quả").
- Không có lý do cho các chỉ dẫn, nên AI không biết xử lý tình huống ngoài lệ. Bản mới thêm "vì sao" cho từng nguyên tắc quan trọng.

### 3.7 Thiếu sót so với bối cảnh thực tế (1/5)
Bản gốc chưa nhắc tới các điều đã biết và đã chốt:
- Ưu tiên theo **ma trận Eisenhower**; giới hạn **WIP ≤ 3** người dùng tự đặt.
- **Chỉ đọc + đề xuất**; nhắc khi được hỏi và **bản nhắc tự động 7:40 sáng** giờ VN.
- Các lỗ hổng thật: 27/27 việc công ty không có deadline; không có cột mức quan trọng; 13 việc đang làm; việc nằm im 30+ ngày; việc trong kế hoạch ngày bị sót không lên kanban; estimate plan ngừng cập nhật từ 15/11; WBS học PM không khả thi (63 ngày công / 14 ngày).
- Phạm vi gồm cả mục tiêu cá nhân (học, gia đình / tài chính, tìm việc), không chỉ công việc công ty.
- Làm việc với supplier và đồng nghiệp nước ngoài, nên cần nháp tin nhắn tiếng Anh.

## 4. Thay đổi chính (cũ → mới)

| # | Cũ | Mới | Lý do |
|---|---|---|---|
| 1 | "Người dùng không có năng lực quản lí tác vụ như AI" | Bối cảnh cụ thể: kỹ sư NPD, ~10 dự án, mục tiêu cá nhân; vấn đề là khối lượng vượt trí nhớ | Mô tả đúng vấn đề, tránh để AI làm thay thay vì kèm cặp |
| 2 | Mục đích chung chung, không đo được | Bảng 5 chỉ số có mốc hiện tại và mục tiêu | AI và người dùng cùng biết thế nào là "làm tốt" |
| 3 | Không có ranh giới | Mục 3: chỉ đọc, không gửi thay, quyết định lớn thuộc người dùng, bảo mật, không bịa | Đúng điều người dùng đã chốt; bảo vệ dữ liệu công ty |
| 4 | "Nằm thời khóa biểu" nhưng không nói ở đâu | Mục 4: 3 file Sheets + thư mục dự án, trỏ tới `sources.md`; kanban là nguồn sự thật duy nhất | AI biết đọc ở đâu, không chép trùng chi tiết |
| 5 | Không có nhịp | Mục 5: hằng ngày 7:40, khi được hỏi, tuần, tháng | Biến "theo dõi tiến độ" thành lịch cụ thể |
| 6 | Không có nguyên tắc ưu tiên | Mục 6: Eisenhower, tập trung (≤ 3 việc / ngày, WIP ≤ 3), bước tiếp theo cụ thể, không bỏ sót, kế hoạch khả thi, mỗi cái có lý do | Hiện thực ý "tập trung vào việc trọng yếu" |
| 7 | "Xây dựng 1 thói quen quản lí" (không cơ chế) | Mục 7: 5 cơ chế kèm cặp, 3 giai đoạn giảm hỗ trợ, đo tiến bộ | Hiện thực mục tiêu "không phụ thuộc AI" |
| 8 | Không có phong cách | Mục 8: tiếng Việt, ngắn, kết luận trước, nói thẳng không trách, tin nhắn tiếng Anh cho người nước ngoài | Đầu ra nhất quán giữa các skill |
| 9 | "AI sẽ xây dựng những skill…" | Mục 9: danh mục skill (đã có thu-ky-du-an + 5 skill đề xuất theo thứ tự) | Từ lệnh một lần thành bản đồ hệ thống skill |
| 10 | — | Mục 10 + các nhãn [Cần bạn chốt] | Nói rõ chỗ AI cần người dùng quyết thay vì tự đoán |

## 5. Câu hỏi người dùng cần chốt

1. Mục tiêu "100% việc công ty có deadline": đạt trong bao lâu?
2. Bản nhắc hằng ngày có gộp việc cá nhân (tài chính, tìm việc) chung với việc công ty không, ví dụ khi bạn mở trên máy công ty?
3. Review tuần vào lúc nào: chiều thứ Sáu hay tối Chủ Nhật?
4. Review tháng vào ngày nào?
5. Điều kiện chuyển giai đoạn kèm cặp (gợi ý: 4 tuần liền WIP ≤ 3, 100% việc có deadline, top 3 của bạn trùng với AI ít nhất 2/3)?
6. Ghi nhật ký kèm cặp ở đâu (gợi ý: một sheet trong Daily Kanban do bạn tự cập nhật, vì AI chỉ đọc)?
7. Có thêm cột "Mức quan trọng" vào Kanban TTI không?
8. WBS học quản lý dự án: dời mốc 15/12 hay cắt phạm vi?
9. Giữ estimate plan theo ngày, hay thay bằng kế hoạch tuần?
10. Thứ tự ưu tiên giữa các mục tiêu lớn (công việc, học, tài chính, tìm việc) khi chúng tranh nhau thời gian, và quỹ thời gian thực tế mỗi tuần cho việc cá nhân và việc học?
11. Xưng hô: giữ "bạn" hay muốn cách khác?

## 6. Chỗ skill thu-ky-du-an hiện lệch với instruction mới (chưa sửa)

- Chưa có cơ chế kèm cặp (mục 7): review tuần chưa hỏi người dùng tự xếp top 3 trước, chưa có "bài học tuần", chưa biết đang ở giai đoạn nào.
- Chưa có review tháng và chưa theo dõi xu hướng chỉ số qua thời gian (mới chỉ nêu lỗ hổng tại thời điểm chạy).
- Bản nhắc thử ngày 25/11 dài 67 dòng; nguyên tắc "ba dòng đầu đủ để biết hôm nay làm gì" và "ngắn hơn bảng gốc" nên được siết thêm (vd rút gọn mục "Lên lịch trong tuần" và "Đề xuất cập nhật").
- Skill nói rõ "không sửa file", nhưng chưa nói rõ "không gửi mail / tin nhắn thay", dù hiện chỉ soạn nháp.
