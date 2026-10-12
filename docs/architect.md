# Kiến trúc hệ thống

> Tài liệu mô tả trạng thái hiện tại của hệ thống. Các mục ghi **Đã chốt** là quyết định đang áp dụng;
> các mục ghi **Dự kiến** là hướng đi hiện tại, có thể thay đổi khi bắt tay vào làm.

Cập nhật lần cuối: 2026-10-12

---

## 1. Mục đích

Hệ thống phân tích báo cáo tài chính (BCTC) của doanh nghiệp niêm yết Việt Nam:

1. Thu thập BCTC cho một danh sách mã chọn trước.
2. Lưu trữ dữ liệu gốc, truy vết được nguồn và thời điểm thu thập.
3. Tính các chỉ số tài chính bằng code có kiểm thử.
4. Dùng AI để diễn giải các chỉ số đã tính. AI không tự tính số.

Phạm vi hiện tại: một nhóm nhỏ mã chọn lọc, không phải toàn thị trường.

---

## 2. Môi trường

| Thành phần | Lựa chọn | Trạng thái |
|---|---|---|
| Ngôn ngữ | Python **3.13** | Đã chốt |
| Quản lý môi trường | Miniconda: conda chỉ tạo env Python; mọi thư viện cài bằng pip | Đã chốt |
| Danh sách thư viện | `requirements.txt`, viết tay | Đã chốt |
| Hệ điều hành | Windows và Kubuntu (dual-boot). Mọi thứ phải chạy được trên cả hai | Đã chốt |
| Mã nguồn | GitHub, repo public | Đã chốt |
| Dữ liệu | Nằm ngoài repo, dưới thư mục gốc `DATA_DIR`, khai báo trong `.env` của từng máy | Đã chốt |

Tạo môi trường (giống nhau trên cả hai OS):

```bash
conda create -n vn_fsa python=3.13 -y
conda activate vn_fsa
pip install -r requirements.txt
pip install -e .          # để `import fsa` chạy được ở mọi nơi
```

---

## 3. Tổng quan luồng dữ liệu

```
config/universe.csv          (danh sách mã cần xử lý)
        │
        ▼
[1] Ingest ── vnstock 5.0.0 ── API của các CTCK (VCI, KBS)
        │
        ▼
DATA_DIR/raw/                 (dữ liệu gốc, chỉ thêm, không ghi đè)
        │
        ▼
[2] Xử lý và chuẩn hóa        (để sau)
        │
        ▼
[3] Tính chỉ số và cờ cảnh báo (để sau)
        │
        ▼
[4] Diễn giải bằng AI         (để sau; đọc kết quả đã tính, không tự tính)
```

Nguyên tắc xuyên suốt:

- **Code tính con số, AI diễn giải.** Mọi chỉ số được tính bằng code có test.
- **Dữ liệu gốc là bất biến.** Các tầng sau đều dựng lại được từ tầng raw.
- **Logic nằm trong hàm nghiệp vụ**, tách khỏi cách gọi (CLI, API, giao diện, skill).

---

## 4. Danh sách mã xử lý (universe)

**Trạng thái: Đã chốt, chưa tạo file**

- File: `config/universe.csv`, nằm trong repo vì đây là cấu hình, cần theo dõi lịch sử thay đổi.
- Cột: `symbol`, `active`, `groups`, `note`.
- Hàm ingest **nhận danh sách mã làm tham số**, không tự đọc file. Universe chỉ là nguồn mặc định.
- Bỏ một mã khỏi universe không xóa dữ liệu đã tải của mã đó.

---

## 5. Ingest

### 5.1 Nguồn dữ liệu

**Trạng thái: Đã chốt**

| Mục | Chi tiết |
|---|---|
| Thư viện | `vnstock==5.0.0`, cài từ index của vnstocks.com |
| API | `Fundamental().equity(symbol).<báo cáo>(period=..., source=..., lang=...)` |
| Báo cáo | `income_statement`, `balance_sheet`, `cash_flow` |
| Nguồn bên dưới | `vci` (mặc định), `kbs` |
| Định dạng trả về | Long: `period, id, name, order, level, unit, value`. `id` là mã chỉ tiêu ổn định (ví dụ `IS_NET_REVENUE`). Bảng cân đối có thêm `off_balance` |
| Kỳ | `period` dạng `2025` (năm) hoặc `2026-Q2` (quý) |
| Đơn vị | Đồng (không phải tỷ đồng). Chi phí được ghi số âm |
| Xác thực | `VNSTOCK_API_KEY` trong `.env`; đăng nhập qua `fsa.utils.vnstock_auth.login()`. Kiểm tra bằng `get_status()` |

Vị trí của vnstock trong chuỗi dữ liệu:

```
BCTC gốc (PDF trên HOSE/HNX, website doanh nghiệp)
  → các CTCK / vendor số hóa thành bảng số
  → API của CTCK
  → vnstock
```

Dữ liệu đã qua ít nhất hai lần xử lý trước khi tới hệ thống, nên về sau cần đối chiếu với BCTC gốc.

### 5.2 Giới hạn cần biết

- **Số kỳ mỗi lần gọi** phụ thuộc tier: Guest 4 kỳ, Community 8 kỳ, Sponsor toàn bộ.
  Lịch sử dài được tích lũy dần qua nhiều lần tải.
- **Số lần gọi mỗi phút**: Guest 20, Community 60.
- **License**: miễn phí cho mục đích cá nhân, học tập, nghiên cứu. **Không đưa dữ liệu lên repo.**
  Phải xem lại license trước khi làm sản phẩm cho người khác dùng.

### 5.3 Bảo mật

- Chỉ import vnstock trong `src/fsa/ingest/` và `src/fsa/utils/vnstock_auth.py`.
- Các phiên bản vnstock cũ từng tự ghi file chỉ dẫn cho AI assistant khi import.
  Sau mỗi lần nâng cấp vnstock: chạy `git status` và kiểm tra các file như `CLAUDE.md`, `AGENTS.md`, `~/.claude/`.
- API key không bao giờ xuất hiện trong code, notebook hay chat.

### 5.4 Cách chạy

**Trạng thái: Đang làm**

- Mỗi báo cáo một hàm, nhận tham số rõ ràng: mã, loại kỳ.
- Giai đoạn hiện tại: gọi API và in DataFrame ra để xem. Chưa ghi file.
- Bước tiếp theo: gộp ba báo cáo của một mã, thêm cột metadata, ghi ra Parquet (xem mục 6).

---

## 6. Data model và lưu trữ

**Trạng thái: Dự kiến**

### 6.1 Bảng `raw_financial_statement`

Một bảng logic duy nhất cho cả ba báo cáo. Mỗi dòng là **một chỉ tiêu, của một kỳ, của một mã, trong một lần tải**.

| Cột | Nguồn | Ý nghĩa |
|---|---|---|
| `symbol` | thêm | Mã chứng khoán |
| `statement` | thêm | `income_statement`, `balance_sheet`, `cash_flow` |
| `period` | vnstock | `2025` hoặc `2026-Q2` |
| `period_type` | thêm, suy ra từ `period` | `year` / `quarter` |
| `id` | vnstock | Mã chỉ tiêu |
| `name`, `order`, `level`, `unit` | vnstock | Giữ nguyên |
| `value` | vnstock | Giữ nguyên kiểu vnstock trả về |
| `off_balance` | vnstock | Chỉ có ở bảng cân đối, để trống với hai báo cáo kia |
| `source` | thêm | Ví dụ `vci` |
| `fetched_at` | thêm | Thời điểm tải (UTC) |

Khóa logic: `symbol, source, period, id, fetched_at`.

Tầng raw lưu nguyên trạng. Đổi kiểu, đảo dấu, chuẩn hóa để sang bước xử lý sau.

### 6.2 Lưu trên đĩa

```
DATA_DIR/
└── raw/
    └── vnstock/
        └── fetch_date=2026-10-12/
            ├── FPT.parquet       ba báo cáo của một mã trong một lần tải
            └── ...
```

- Mỗi lần tải là một thư mục `fetch_date` mới, không ghi đè lần trước.
- Bảng `raw_financial_statement` là tập hợp mọi file Parquet trong `raw/vnstock/`.
- Ghi Parquet cần thêm thư viện `pyarrow` (chưa thêm).

### 6.3 Các tầng sau

Xử lý, chuẩn hóa, bảng số liệu hiện hành, tính chỉ số: để sau, mô tả khi bắt đầu làm.

---

## 7. Quy ước thư mục trong repo

| Thư mục | Quy ước |
|---|---|
| `src/fsa/` | Package Python. Logic nghiệp vụ là các hàm có tham số; CLI, notebook, giao diện chỉ gọi lại |
| `src/fsa/ingest/` | Lấy dữ liệu từ nguồn. Nơi import vnstock |
| `src/fsa/utils/` | Hàm dùng lại ở ít nhất hai module. Đặt tên file theo việc nó làm |
| `config/` | Cấu hình do người viết tay (ví dụ `universe.csv`). Không chứa dữ liệu |
| `docs/` | Tài liệu về project |
| `.claude/` | Chỉ dẫn cho Claude Code (rule, skill, agent, settings) |

Dữ liệu không nằm trong repo mà dưới `DATA_DIR` (xem mục 6.2).

---

## 8. Câu hỏi còn mở

- vnstock trả về BCTC **hợp nhất** hay **riêng**? Cần đối chiếu với BCTC gốc của một tập đoàn.
- `vnstock.login()` có cần gọi lại mỗi lần chạy không? Kiểm tra bằng `get_status()` ở lần chạy sau.
- Windows và Kubuntu có bị tính là hai thiết bị không? So `device_id` trong `get_status()` trên hai OS.
- Có cần cột loại hình công ty (`com_type`) trong universe không?
- Hai nguồn `vci` và `kbs` có độc lập với nhau không?
