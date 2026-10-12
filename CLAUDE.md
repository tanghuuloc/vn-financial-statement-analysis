# vn-financial-statement-analysis

Hệ thống phân tích BCTC doanh nghiệp niêm yết Việt Nam: thu thập BCTC, lưu trữ,
tính chỉ số tài chính, rồi dùng AI diễn giải. Bối cảnh đầy đủ: `.claude/system-prompt.md`.

## Ràng buộc bắt buộc
- Chạy được trên cả Windows và Kubuntu: dùng `pathlib`, không hard-code đường dẫn tuyệt đối.
- Dữ liệu KHÔNG nằm trong repo. Mọi file dữ liệu nằm dưới biến môi trường `DATA_DIR`
  (khai báo trong `.env`, khác nhau mỗi máy). Code chỉ dùng đường dẫn tương đối so với `DATA_DIR`.
- Mọi thao tác là một hàm Python có tham số rõ ràng và type hint. Logic nằm trong hàm nghiệp vụ,
  tách khỏi cách gọi (CLI, API, giao diện, skill).
- Không đưa secret vào code. Không đọc file `.env`.

## Nguyên tắc
- Code tính con số (SQL/Python có test), AI chỉ diễn giải. Thiếu số liệu thì báo thiếu, không ước tính.
- Đơn giản trước. Không thêm thư viện hay hạ tầng khi chưa có nhu cầu thật; nếu đề xuất thì nêu lý do.
- Mỗi hàm tính chỉ số tài chính phải có test với giá trị tính tay.

## Môi trường
- Conda env `fsa` (Python 3.12). Thư viện cài bằng pip từ `requirements.txt`, ghim `==`.
- Không dùng `pip freeze`, không `conda install` thư viện Python.

## Cấu trúc
- `src/fsa/`: package Python.

## Cách làm việc
- Với thay đổi lớn hơn một file: trình bày kế hoạch trước, chờ đồng ý rồi mới sửa.
- Không tự commit hay push.