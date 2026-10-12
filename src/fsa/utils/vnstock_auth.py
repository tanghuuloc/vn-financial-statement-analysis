import os
from typing import Any

import vnstock
from dotenv import load_dotenv

API_KEY_ENV = "VNSTOCK_API_KEY"


def login(api_key: str | None = None) -> None:
    """Đăng nhập vnstock. Theo tài liệu vnstock, chỉ cần một lần trên mỗi máy.

    Nếu không truyền `api_key`, đọc từ biến môi trường VNSTOCK_API_KEY (nạp từ .env nếu có).
    """
    if api_key is None:
        load_dotenv()
        api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Thiếu API key: truyền api_key hoặc khai báo {API_KEY_ENV} trong .env")
    vnstock.login(api_key)


def logout() -> None:
    """Xoá khoá vnstock khỏi máy."""
    vnstock.logout()


def get_status() -> dict[str, Any]:
    """Trạng thái đăng nhập từ vnstock.status() (tier, authenticated, expires_at, device_id, ...)."""
    return vnstock.status()


def get_usage() -> dict[str, Any]:
    """Hạn mức sử dụng từ vnstock.usage() (limits, used, rule)."""
    return vnstock.usage()


def is_logged_in() -> bool:
    """True nếu vnstock.status() báo đã xác thực. Thiếu trường `authenticated` thì coi là chưa."""
    return bool(get_status().get("authenticated", False))
