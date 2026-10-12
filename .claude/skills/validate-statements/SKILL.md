---
name: validate-statements
description: Kiểm tra tính nhất quán của BCTC đã nạp (cân đối kế toán, khớp giữa các báo cáo, đơn vị, kỳ). Dùng trước khi tính chỉ số hoặc khi nghi ngờ số liệu sai.
---

# Kiểm tra chất lượng BCTC

Đầu vào: mã chứng khoán và kỳ báo cáo (hoặc phạm vi kỳ). Dữ liệu lấy qua các hàm trong `src/fsa/`
từ `DATA_DIR`; không đọc file `.env`.

## Các bước

1. Xác định phạm vi: mã, kỳ, loại báo cáo (hợp nhất/riêng lẻ), trạng thái kiểm toán.
2. Chạy các kiểm tra, mỗi kiểm tra báo `đạt`, `không đạt` hoặc `không đủ dữ liệu`:
   - Tổng tài sản = Tổng nguồn vốn.
   - Tổng tài sản bằng tổng các khoản mục con; tương tự cho nợ phải trả và vốn chủ sở hữu.
   - Lợi nhuận sau thuế trên báo cáo kết quả kinh doanh khớp với phần tương ứng trong báo cáo lưu chuyển tiền tệ.
   - Tiền cuối kỳ trên lưu chuyển tiền tệ khớp với tiền và tương đương tiền trên bảng cân đối.
   - Số đầu kỳ của kỳ này khớp số cuối kỳ của kỳ trước.
   - Đơn vị nhất quán giữa các kỳ (không nhảy giữa đồng và triệu đồng).
3. Báo cáo kết quả dạng bảng: kiểm tra, giá trị hai vế, chênh lệch, kết luận.

## Quy tắc

- Chỉ dùng số có trong dữ liệu. Thiếu thì ghi `không đủ dữ liệu`, không ước tính.
- Cho phép sai lệch làm tròn nhỏ; nêu rõ ngưỡng đã dùng.
- Khi có chênh lệch, gợi ý cách tự đối chiếu với BCTC gốc (file PDF/bản công bố trên trang công ty hoặc sàn).
- Không sửa dữ liệu. Chỉ báo cáo.
