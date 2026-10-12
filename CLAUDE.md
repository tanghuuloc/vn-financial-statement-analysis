# vn-financial-statement-analysis

Hệ thống phân tích BCTC doanh nghiệp niêm yết Việt Nam: thu thập BCTC, lưu trữ,
tính chỉ số tài chính, rồi dùng AI diễn giải. Bối cảnh đầy đủ: `docs/system-prompt.md`.

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

## Thư viện
- Chỉ dùng thư viện chuẩn của Python và các thư viện đã có trong `requirements.txt`.
- Muốn thêm thư viện mới: DỪNG LẠI và hỏi trước. Nêu lý do cần, và cách làm nếu không dùng nó.
  Chỉ thêm khi thư viện chuẩn không làm được, hoặc làm được nhưng rất phức tạp.
- Không thêm thư viện chỉ để tiết kiệm vài dòng code (ví dụ: click, typer, loguru, pydantic, tqdm).

## Phong cách code
- Ưu tiên dễ đọc hơn ngắn gọn. Người mới đọc lần đầu phải hiểu được.
- Một hàm làm một việc, nên dưới khoảng 40 dòng. Dài hơn thì tách hàm.
- Dùng hàm thường. Chỉ dùng class khi thật sự cần giữ trạng thái.
- Không viết abstraction "để dành cho sau này": không base class, không plugin system,
  không decorator tự viết, không generic framework khi mới có một trường hợp sử dụng.
- Không viết one-liner phức tạp: không list comprehension lồng nhau,
  không chuỗi pandas method dài quá khoảng 4 bước. Tách ra biến trung gian có tên rõ nghĩa.
- Tên biến và tên hàm bằng tiếng Anh, đầy đủ nghĩa (`net_revenue`, không viết `nr` hay `x`).
- Comment giải thích VÌ SAO làm như vậy, không lặp lại code đang LÀM GÌ.
- Không dùng `from __future__ import annotations` (project chạy Python 3.13).

## Môi trường
- Conda env `vn_fsa` (Python 3.13). Thư viện cài bằng pip từ `requirements.txt`, ghim `==`.
- Không dùng `pip freeze`, không `conda install` thư viện Python.

## Cấu trúc
- `src/fsa/`: package Python. Logic nghiệp vụ là các hàm có tham số; CLI, notebook, giao diện chỉ gọi lại.
- `src/fsa/ingest/`: lấy dữ liệu từ nguồn. Nơi import vnstock (ngoài `utils/vnstock_auth.py`).
- `src/fsa/utils/`: hàm dùng lại ở ít nhất hai module. Đặt tên file theo việc nó làm, không đặt `helpers.py`.
- `config/`: cấu hình do người viết tay. Không chứa dữ liệu.
- `docs/`: tài liệu về project; kiến trúc ở `docs/architect.md`. `.claude/`: chỉ dẫn cho Claude Code.

## Cách làm việc
- Với thay đổi lớn hơn một file: trình bày kế hoạch trước, chờ đồng ý rồi mới sửa.
- Không tự commit hay push.