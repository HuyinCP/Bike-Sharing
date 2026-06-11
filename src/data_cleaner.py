import os
import sys
import time

import duckdb

from src.clean_rules import (
    clean_trips_select_sql,
    exclusion_breakdown,
    keep_where_sql,
    schema_dtype_map,
)

CITY_FILES = {
    "citibike": "citibike_nyc_merged.parquet",
    "divvy": "divvybike_merged.parquet",
    "capital": "capitalbike_merged.parquet",
}

CLEAN_OUTPUT = {
    "citibike": "citibike_nyc_cleaned.parquet",
    "divvy": "divvybike_cleaned.parquet",
    "capital": "capitalbike_cleaned.parquet",
}


class DataCleaner:
    def __init__(self, raw_dir, clean_dir):
        self.raw_dir = raw_dir.replace("\\", "/")
        self.clean_dir = clean_dir.replace("\\", "/")
        self.conn = duckdb.connect()
        os.makedirs(clean_dir, exist_ok=True)

    def process_file(self, city_name, file_name):
        """Clean theo E1–E7 trong docs/report/cleaning_rules.md."""
        raw_path = f"{self.raw_dir}/{file_name}".replace("\\", "/")
        out_name = CLEAN_OUTPUT.get(city_name, f"{city_name}_cleaned.parquet")
        clean_path = f"{self.clean_dir}/{out_name}".replace("\\", "/")
        raw_from = f"read_parquet('{raw_path}')"

        print(f"=== BẮT ĐẦU XỬ LÝ DỮ LIỆU CHO {city_name.upper()} ===")
        start_time = time.time()

        dtype_map = schema_dtype_map(self.conn, raw_from)
        keep_sql = keep_where_sql(dtype_map)
        select_sql = clean_trips_select_sql(dtype_map)

        raw_stats = self.conn.execute(f"""
            SELECT
                COUNT(*),
                SUM(CASE WHEN lower(trim(member_casual)) = 'member' THEN 1 ELSE 0 END),
                SUM(CASE WHEN lower(trim(member_casual)) = 'casual' THEN 1 ELSE 0 END)
            FROM {raw_from}
        """).fetchone()
        raw_total, raw_member, raw_casual = raw_stats
        breakdown = exclusion_breakdown(self.conn, raw_from, dtype_map)

        print("\n--- BẢNG LOẠI BỎ (E1–E7) ---")
        for row in breakdown:
            if row["Mã"] in ("—", "✓"):
                print(f"  {row['Lý do loại bỏ']}: {row['Số chuyến (trên raw)']:,} ({row['% raw']}%)")
            elif row["Số chuyến (trên raw)"] > 0:
                print(
                    f"  {row['Mã']} {row['Lý do loại bỏ']}: "
                    f"{row['Số chuyến (trên raw)']:,} (tuần tự: {row['Loại bỏ tuần tự (không trùng)']:,})"
                )

        print("\nĐang làm sạch và ghi ra Parquet (thiếu → NULL)...")
        self.conn.execute(f"""
            COPY (
                SELECT
                    {select_sql}
                FROM {raw_from}
                WHERE {keep_sql}
            ) TO '{clean_path}' (FORMAT PARQUET)
        """)

        clean_stats = self.conn.execute(f"""
            SELECT
                COUNT(*),
                SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END),
                SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END),
                SUM(CASE WHEN has_start_station = 0 THEN 1 ELSE 0 END),
                SUM(CASE WHEN has_end_station = 0 THEN 1 ELSE 0 END)
            FROM read_parquet('{clean_path}')
        """).fetchone()
        clean_total, clean_member, clean_casual, no_start_st, no_end_st = clean_stats

        self.discussing_step(
            raw_total, raw_member, raw_casual,
            clean_total, clean_member, clean_casual,
        )
        print(f"  Sau clean — không tên trạm start: {no_start_st:,} | không tên trạm end: {no_end_st:,}")

        elapsed = time.time() - start_time
        print(f"✅ Xử lý xong {city_name} trong {elapsed:.2f} giây. File: {clean_path}\n")
        return clean_path

    def discussing_step(
        self, raw_total, raw_member, raw_casual, clean_total, clean_member, clean_casual
    ):
        print(f"\nRetention: {clean_total:,} / {raw_total:,} ({clean_total/raw_total*100:.2f}%)")
        print("\n--- BIAS CHECK (member vs casual) ---")
        raw_member_pct = (raw_member / raw_total) * 100 if raw_total else 0
        raw_casual_pct = (raw_casual / raw_total) * 100 if raw_total else 0
        clean_member_pct = (clean_member / clean_total) * 100 if clean_total else 0
        clean_casual_pct = (clean_casual / clean_total) * 100 if clean_total else 0
        print(f"  Trước: Member {raw_member_pct:.2f}% | Casual {raw_casual_pct:.2f}%")
        print(f"  Sau : Member {clean_member_pct:.2f}% | Casual {clean_casual_pct:.2f}%")

    def process_all(self):
        for city, fname in CITY_FILES.items():
            self.process_file(city, fname)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    cleaner = DataCleaner(
        os.path.join(root, "dataraw"),
        os.path.join(root, "dataclean"),
    )
    cleaner.process_all()
