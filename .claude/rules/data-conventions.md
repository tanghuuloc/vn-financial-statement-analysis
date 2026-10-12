# Quy ước dữ liệu

- Mọi file dữ liệu nằm dưới `DATA_DIR` (đọc từ biến môi trường qua một hàm duy nhất, ví dụ `get_data_dir()`).
  Code chỉ dùng đường dẫn tương đối so với `DATA_DIR`, dựng bằng `pathlib.Path`.
- Không hard-code `C:\...` hay `/home/...`. Không dùng `os.path.join` với chuỗi có dấu `\`.
- Mọi con số tài chính phải truy vết được về nguồn: mã chứng khoán, kỳ báo cáo, loại báo cáo
  (hợp nhất/riêng lẻ), trạng thái kiểm toán (trước/sau kiểm toán), đơn vị.
- Ghi rõ đơn vị (đồng, triệu đồng, tỷ đồng) trong tên cột hoặc metadata; không trộn đơn vị trong cùng một bảng.
- Dữ liệu thiếu để là `NULL`/`None`, không điền 0 và không ước tính.
- Mẫu BCTC khác nhau theo ngành (doanh nghiệp thường, ngân hàng, bảo hiểm, chứng khoán):
  không áp một công thức chung nếu chưa kiểm tra mẫu báo cáo.
