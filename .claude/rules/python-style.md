---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Quy ước Python

- Python 3.13, type hint đầy đủ cho tham số và giá trị trả về.
- Mỗi thao tác là một hàm với tham số rõ ràng. Logic nghiệp vụ nằm trong `src/fsa/`,
  tách khỏi lớp gọi (CLI, API, giao diện, skill).
- Dùng `pathlib.Path`, không hard-code đường dẫn tuyệt đối.
- Không đưa secret vào code, không đọc file `.env` trực tiếp từ các công cụ của Claude.
- Thư viện mới: ghim phiên bản `==` trong `requirements.txt`, nêu lý do cần thêm trước khi thêm.
- Test bằng `pytest`, đặt trong `tests/`, phản chiếu cấu trúc của `src/fsa/`.
