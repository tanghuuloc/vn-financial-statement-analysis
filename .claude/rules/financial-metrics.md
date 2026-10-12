# Quy tắc cho hàm tính chỉ số tài chính

- Mỗi hàm tính chỉ số là một hàm thuần (đầu vào là số liệu, đầu ra là số), không đọc file hay gọi mạng bên trong.
- Docstring ghi: công thức, ý nghĩa, nguồn của công thức (chuẩn mực, giáo trình hay nghiên cứu gốc),
  và lưu ý khi áp dụng cho doanh nghiệp Việt Nam (VAS khác IFRS ở đâu nếu liên quan).
- Mỗi hàm phải có test với giá trị tính tay (ghi cách tính trong comment của test).
- Xử lý rõ các trường hợp biên: mẫu số bằng 0, giá trị âm (vốn chủ sở hữu âm), dữ liệu thiếu.
  Trả về `None` thay vì ước tính hoặc ném lỗi chung chung.
- Chỉ số dùng giá trị bình quân (ví dụ ROE, ROA) phải nêu rõ dùng bình quân đầu-cuối kỳ hay cuối kỳ.
- Ngưỡng từ thị trường khác (ví dụ ngưỡng Z-Score của Mỹ) phải ghi chú là có thể không phù hợp với Việt Nam.
- Không bịa nguồn. Nếu không tìm được nguồn cho một công thức hay ngưỡng, ghi rõ là không tìm được.
