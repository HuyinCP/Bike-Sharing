"""In bảng tổng hợp loại bỏ 3 thành phố."""
import sys
from pathlib import Path

import duckdb

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from src.clean_rules import exclusion_breakdown, kept_pattern_scan, schema_dtype_map

FILES = {
    "Citi Bike": "citibike_nyc_merged.parquet",
    "Divvy": "divvybike_merged.parquet",
    "Capital": "capitalbike_merged.parquet",
}

conn = duckdb.connect()

for city, fname in FILES.items():
    p = (root / "dataraw" / fname).as_posix()
    raw = f"read_parquet('{p}')"
    dm = schema_dtype_map(conn, raw)
    print(f"\n{'='*60}\n{city}\n{'='*60}")
    for row in exclusion_breakdown(conn, raw, dm):
        print(row)
    print("\nKept patterns:")
    for row in kept_pattern_scan(conn, raw, dm):
        print(row)
