import pandas as pd
from vnstock import Fundamental


def get_income_statement(symbol: str, period: str = "year") -> pd.DataFrame:
    """Lấy báo cáo kết quả kinh doanh của một mã theo kỳ (year hoặc quarter)."""
    return Fundamental().equity(symbol).income_statement(period=period)


if __name__ == "__main__":
    # Chạy thử: python -m fsa.ingest.read_income_statement
    df = get_income_statement("VIC", period="quarter")
    df = df[df["period"] == "2026-Q2"]
    print(df)
