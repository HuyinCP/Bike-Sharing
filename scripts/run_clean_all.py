"""Chạy clean cho cả 3 thành phố — output vào dataclean/."""
import os
import sys
from pathlib import Path

# Windows console: in tiếng Việt không lỗi encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from src.data_cleaner import CITY_FILES, DataCleaner  # noqa: E402

if __name__ == "__main__":
    cleaner = DataCleaner(
        str(root / "dataraw"),
        str(root / "dataclean"),
    )
    for city, fname in CITY_FILES.items():
        raw = root / "dataraw" / fname
        if not raw.exists():
            print(f"⚠ Bỏ qua {city}: không có {raw}")
            continue
        cleaner.process_file(city, fname)
