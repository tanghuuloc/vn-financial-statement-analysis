---
name: analyze-company
description: Phân tích sức khỏe một doanh nghiệp niêm yết Việt Nam theo nhiều kỳ từ số liệu đã tính. Dùng khi người dùng yêu cầu đánh giá, nhận định về một mã chứng khoán.
---

# Phân tích doanh nghiệp

Đầu vào: mã chứng khoán, số kỳ cần xem (mặc định các kỳ gần nhất có dữ liệu).

## Các bước

1. Chạy skill `validate-statements` cho mã và kỳ liên quan. Nếu có kiểm tra không đạt, nêu rõ trước khi phân tích.
2. Lấy các chỉ số đã được tính bằng hàm trong `src/fsa/`. AI không tự tính chỉ số; thiếu chỉ số thì báo thiếu.
3. Nhóm chỉ số: khả năng sinh lời, đòn bẩy và thanh khoản, hiệu quả hoạt động, dòng tiền, chất lượng lợi nhuận.
4. So sánh theo xu hướng nhiều kỳ. So với trung vị ngành nếu có dữ liệu ngành.
5. Lưu ý đặc thù Việt Nam: giao dịch bên liên quan, chênh lệch số liệu trước/sau kiểm toán,
   ý kiến kiểm toán, trái phiếu đến hạn.

## Định dạng kết quả

- **Số liệu cho thấy**: bảng chỉ số theo kỳ, ghi nguồn và đơn vị.
- **Nhận định**: mỗi nhận định kèm mức độ chắc chắn.
- **Cách tự kiểm chứng**: đối chiếu BCTC gốc, báo cáo của công ty chứng khoán, giáo trình hay nghiên cứu gốc của chỉ số.
- **Liên hệ CFA**: chỉ thêm khi thật sự có liên hệ (mảng, khái niệm, vị trí trong project, khác biệt VAS/IFRS).

## Quy tắc

- Không khuyến nghị mua/bán cụ thể.
- Gắn nhãn **[Có nguồn]**, **[Phổ biến]**, **[Đề xuất]** cho practice và ngưỡng được dùng.
- Không bịa nguồn, tác giả hay số liệu.
