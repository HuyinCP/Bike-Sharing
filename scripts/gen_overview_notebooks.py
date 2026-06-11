"""Tạo 3 notebook overview: thống kê TRƯỚC clean → clean → SAU clean → minh chứng → xuất."""
import json
from pathlib import Path

CONFIGS = [
    (
        "overview_citibike.ipynb",
        "citibike_nyc_merged.parquet",
        "Citi Bike (New York City)",
        "citibike_nyc_cleaned.parquet",
    ),
    (
        "overview_divvybike.ipynb",
        "divvybike_merged.parquet",
        "Divvy (Chicago)",
        "divvybike_cleaned.parquet",
    ),
    (
        "overview_capitalbike.ipynb",
        "capitalbike_merged.parquet",
        "Capital Bikeshare",
        "capitalbike_cleaned.parquet",
    ),
]

CELL_SETUP = r'''import os
import sys
from pathlib import Path

import duckdb
import pandas as pd

current_dir = os.getcwd()
if current_dir.endswith(("notebooks", "1.statistic", "1.statics")):
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
else:
    project_root = current_dir

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import importlib
import src.clean_rules as clean_rules
importlib.reload(clean_rules)

from src.clean_rules import (
    DURATION_SEC_SQL,
    build_exclusion_context,
    clean_trips_select_sql,
    exclusion_breakdown,
    is_varchar,
    kept_pattern_scan,
    missing_expr,
)

PARQUET_FILE = "{parquet}"
SYSTEM_NAME = "{system}"
DATA_PATH = Path(project_root) / "dataraw" / PARQUET_FILE
PATH_SQL = str(DATA_PATH).replace("\\", "/")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Không tìm thấy {DATA_PATH}.")

conn = duckdb.connect()
CTX = build_exclusion_context(conn, PATH_SQL)
SCHEMA_DTYPE_MAP = CTX["dtype_map"]
KEEP_SQL = CTX["keep_sql"]
TH1_SQL = CTX["th1_sql"]
TH2_SQL = CTX["th2_sql"]
TH4_START_SQL = CTX["th4_start_sql"]
TH5_END_SQL = CTX["th5_end_sql"]
EXCLUSION_RULES = CTX["exclusion_rules"]
CLEAN_SELECT_SQL = clean_trips_select_sql(SCHEMA_DTYPE_MAP)
raw_from = CTX["raw_from"]
active_from = raw_from
n_records = 0
n_records_raw = 0
'''

CELL_HELPERS = r'''def print_overview(title: str) -> int:
    """In tổng quan: số chuyến, trùng ride_id, khoảng thời gian."""
    global n_records
    n_records = conn.execute(f"SELECT COUNT(*) FROM {active_from}").fetchone()[0]
    dup = conn.execute(
        f"SELECT COUNT(*) - COUNT(DISTINCT ride_id) FROM {active_from}"
    ).fetchone()[0]
    dup_pct = (dup / n_records) * 100 if n_records else 0
    tmin, tmax = conn.execute(
        f"SELECT MIN(started_at::TIMESTAMP), MAX(started_at::TIMESTAMP) FROM {active_from}"
    ).fetchone()
    print(f"Hệ thống: {SYSTEM_NAME}")
    print(f"Nguồn: {active_from}")
    print(f"Số chuyến: {n_records:,}")
    print(f"ride_id trùng: {dup:,} ({dup_pct:.4f}%)")
    print(f"Thời gian: {tmin} → {tmax}")
    return n_records


def _schema_context():
    """Đọc schema + hàm đếm thiếu đồng thời nhiều cột."""
    cols_info = conn.execute(
        f"DESCRIBE SELECT * FROM {active_from} LIMIT 1"
    ).fetchdf()
    schema_cols = set(cols_info["column_name"])
    dtype_map = cols_info.set_index("column_name")["column_type"].to_dict()

    def count_joint_missing(cols):
        cols = [c for c in cols if c in schema_cols]
        if not cols:
            return 0
        where_clause = " AND ".join(missing_expr(c, dtype_map[c]) for c in cols)
        return int(conn.execute(f"""
            SELECT COUNT(*) FROM {active_from}
            WHERE {where_clause}
        """).fetchone()[0])

    return cols_info, schema_cols, dtype_map, count_joint_missing


def build_column_missing_df(unified: bool = False):
    """Bảng missing từng cột.

    unified=False (raw): tách Null/NaN và chuỗi rỗng.
    unified=True (sau clean): chỉ đếm IS NULL — blank đã ép về NULL.
    """
    cols_info, _, dtype_map, _ = _schema_context()
    rows = []
    for _, row in cols_info.iterrows():
        col, dtype = row["column_name"], row["column_type"]
        if unified:
            null_count = int(conn.execute(f"""
                SELECT COUNT(*) FILTER (WHERE {col} IS NULL)
                FROM {active_from}
            """).fetchone()[0])
            rows.append({
                "Cột": col,
                "Kiểu dữ liệu": dtype,
                "Thiếu (NULL)": null_count,
                "Tỷ lệ thiếu (%)": round(null_count / n_records * 100, 4) if n_records else 0,
            })
            continue

        miss = missing_expr(col, dtype)
        if is_varchar(dtype):
            null_count, empty_count, _n_unique = conn.execute(f"""
                SELECT
                    COUNT(*) FILTER (WHERE {col} IS NULL),
                    COUNT(*) FILTER (WHERE {col} = ''),
                    COUNT(DISTINCT {col}) FILTER (WHERE NOT {miss})
                FROM {active_from}
            """).fetchone()
        else:
            null_count, _n_unique = conn.execute(f"""
                SELECT
                    COUNT(*) FILTER (WHERE {col} IS NULL),
                    COUNT(DISTINCT {col}) FILTER (WHERE {col} IS NOT NULL)
                FROM {active_from}
            """).fetchone()
            empty_count = 0
        missing_total = int(null_count + empty_count)
        rows.append({
            "Cột": col,
            "Kiểu dữ liệu": dtype,
            "Null/NaN": int(null_count),
            'Chuỗi rỗng ""': int(empty_count),
            "Tổng thiếu": missing_total,
            "Tỷ lệ thiếu (%)": round(missing_total / n_records * 100, 4) if n_records else 0,
        })
    return pd.DataFrame(rows)


def show_column_missing(unified: bool = False):
    """Bảng — thiếu theo từng cột."""
    df = build_column_missing_df(unified=unified)
    display(df)
    miss_col = "Thiếu (NULL)" if unified else "Tổng thiếu"
    df_miss = df[df[miss_col] > 0].sort_values(miss_col, ascending=False)
    if df_miss.empty:
        print("Không còn cột nào thiếu dữ liệu.")
    else:
        print(f"\n{len(df_miss)} cột còn thiếu (trên {len(df)} cột):")
        display(df_miss)


def show_joint_th():
    """Bảng — TH1–TH7: thiếu đồng thời nhiều cột."""
    _, schema_cols, _, count_joint_missing = _schema_context()
    station_name_cols = [
        c for c in ["start_station_name", "start_station_id",
                    "end_station_name", "end_station_id"]
        if c in schema_cols
    ]
    geo_cols = [
        c for c in ["start_station_name", "start_station_id",
                    "end_station_name", "end_station_id",
                    "start_lat", "start_lng", "end_lat", "end_lng"]
        if c in schema_cols
    ]
    if "start_station_id" in schema_cols:
        th1_desc = "Thiếu start_station_name và start_station_id"
        th1_cols = ["start_station_name", "start_station_id"]
    else:
        th1_desc = "Thiếu start_station_name"
        th1_cols = ["start_station_name"]
    if "end_station_id" in schema_cols:
        th2_desc = "Thiếu end_station_name và end_station_id"
        th2_cols = ["end_station_name", "end_station_id"]
    else:
        th2_desc = "Thiếu end_station_name"
        th2_cols = ["end_station_name"]

    cases = [
        ("TH1", th1_desc, th1_cols),
        ("TH2", th2_desc, th2_cols),
        ("TH3", "Thiếu cả 4 cột tên/id trạm", station_name_cols),
        ("TH4", "Thiếu start_lat và start_lng", ["start_lat", "start_lng"]),
        ("TH5", "Thiếu end_lat và end_lng", ["end_lat", "end_lng"]),
        ("TH6", "Thiếu cả 4 tọa độ", ["start_lat", "start_lng", "end_lat", "end_lng"]),
        ("TH7", "Thiếu tất cả cột trạm & tọa độ", geo_cols),
    ]
    rows = []
    for th_id, desc, cols in cases:
        n = count_joint_missing(cols)
        rows.append({
            "Mã": th_id,
            "Mô tả": desc,
            "Số chuyến": n,
            "Tỷ lệ (%)": round(n / n_records * 100, 4) if n_records else 0,
        })
    display(pd.DataFrame(rows))


def show_duration_outliers():
    """Bảng — chuyến quá ngắn / quá dài (ngưỡng Lyft: <60s, >24h)."""
    _, schema_cols, dtype_map, _ = _schema_context()
    n_under60, n_over24 = conn.execute(f"""
        SELECT
            COUNT(*) FILTER (WHERE {DURATION_SEC_SQL} < 60),
            COUNT(*) FILTER (WHERE {DURATION_SEC_SQL} > 86400)
        FROM {active_from}
    """).fetchone()

    n_over24_th5 = 0
    pct_over24_th5 = None
    if {"end_lat", "end_lng"}.issubset(schema_cols) and n_over24:
        end_th5 = " AND ".join(
            missing_expr(c, dtype_map[c]) for c in ["end_lat", "end_lng"]
        )
        n_over24_th5 = int(conn.execute(f"""
            SELECT COUNT(*) FROM {active_from}
            WHERE ({DURATION_SEC_SQL} > 86400) AND ({end_th5})
        """).fetchone()[0])
        pct_over24_th5 = round(n_over24_th5 / n_over24 * 100, 2)

    display(pd.DataFrame([
        {
            "Nhóm": "Dưới 1 phút (< 60 giây)",
            "Số chuyến": int(n_under60),
            "Tỷ lệ (%)": round(n_under60 / n_records * 100, 4) if n_records else 0,
            "% trong chuyến > 24h": None,
        },
        {
            "Nhóm": "Trên 24 tiếng",
            "Số chuyến": int(n_over24),
            "Tỷ lệ (%)": round(n_over24 / n_records * 100, 4) if n_records else 0,
            "% trong chuyến > 24h": None,
        },
        {
            "Nhóm": "↳ Trong đó thiếu tọa độ kết thúc (end_lat & end_lng)",
            "Số chuyến": int(n_over24_th5),
            "Tỷ lệ (%)": round(n_over24_th5 / n_records * 100, 4) if n_records else 0,
            "% trong chuyến > 24h": pct_over24_th5,
        },
    ]))
'''

CELL_P1 = r'''active_from = raw_from
n_records_raw = print_overview("TRƯỚC CLEAN")
'''

CELL_P2 = r'''df_drop = pd.DataFrame(exclusion_breakdown(conn, raw_from, SCHEMA_DTYPE_MAP))
display(df_drop)

n_dropped = int(df_drop.loc[df_drop["Mã"] == "—", "Số chuyến (trên raw)"].iloc[0])
n_records_clean = int(df_drop.loc[df_drop["Mã"] == "✓", "Số chuyến (trên raw)"].iloc[0])

conn.execute(f"""
    CREATE OR REPLACE TEMP VIEW trips_clean AS
    SELECT
        {CLEAN_SELECT_SQL}
    FROM {raw_from}
    WHERE {KEEP_SQL}
""")
active_from = "trips_clean"

print(f"\nGiữ lại: {n_records_clean:,} chuyến")
print(f"Đã bỏ: {n_dropped:,} ({round(n_dropped / n_records_raw * 100, 4) if n_records_raw else 0}%)")

print("\n--- Pattern vẫn giữ sau clean (K1–K6) ---")
display(pd.DataFrame(kept_pattern_scan(conn, raw_from, SCHEMA_DTYPE_MAP)))
'''

CELL_P3 = r'''print_overview("SAU CLEAN")

display(pd.DataFrame([
    {"Giai đoạn": "Trước clean", "Số chuyến": n_records_raw},
    {"Giai đoạn": "Sau clean", "Số chuyến": n_records},
    {"Giai đoạn": "Đã bỏ", "Số chuyến": n_records_raw - n_records},
]))
'''

CELL_P4 = r'''print("--- TH1 & TH2 theo loại xe (raw) ---\n")
display(conn.execute(f"""
    SELECT
        rideable_type,
        COUNT(*) AS tong,
        COUNT(*) FILTER (WHERE {TH1_SQL}) AS th1,
        COUNT(*) FILTER (WHERE {TH2_SQL}) AS th2,
        COUNT(*) FILTER (WHERE {TH1_SQL} AND NOT ({TH4_START_SQL})) AS th1_co_gps,
        COUNT(*) FILTER (WHERE {TH2_SQL} AND NOT ({TH5_END_SQL})) AS th2_co_gps
    FROM {raw_from}
    GROUP BY 1 ORDER BY tong DESC
""").fetchdf())

n_giu = conn.execute(f"SELECT COUNT(*) FROM {raw_from} WHERE {KEEP_SQL}").fetchone()[0]
n_th1_keep = conn.execute(
    f"SELECT COUNT(*) FROM {raw_from} WHERE {KEEP_SQL} AND {TH1_SQL}"
).fetchone()[0]
n_th2_keep = conn.execute(
    f"SELECT COUNT(*) FROM {raw_from} WHERE {KEEP_SQL} AND {TH2_SQL}"
).fetchone()[0]

print("\n--- Nếu bỏ thêm chuyến thiếu tên trạm (có GPS)? ---\n")
display(pd.DataFrame([
    {"Kịch bản": "Giữ hiện tại (E1–E7)", "Ghi chú": f"{n_giu:,} chuyến"},
    {"Kịch bản": "Thêm bỏ TH1 (thiếu tên trạm đi)", "Ghi chú": f"Mất {n_th1_keep:,} chuyến"},
    {"Kịch bản": "Thêm bỏ TH2 (thiếu tên trạm đến)", "Ghi chú": f"Mất {n_th2_keep:,} chuyến"},
]))

print("\n--- Tỷ lệ member / casual ---\n")
display(conn.execute(f"""
    SELECT * FROM (
        SELECT 'Trước clean' AS giai_doan,
            round(100.0 * sum(lower(trim(member_casual))='member') / count(*), 2) AS member_pct,
            round(100.0 * sum(lower(trim(member_casual))='casual') / count(*), 2) AS casual_pct
        FROM {raw_from}
        UNION ALL
        SELECT 'Sau clean',
            round(100.0 * sum(lower(trim(member_casual))='member') / count(*), 2),
            round(100.0 * sum(lower(trim(member_casual))='casual') / count(*), 2)
        FROM {raw_from} WHERE {KEEP_SQL}
    )
""").fetchdf())
'''

CELL_P5 = r'''CLEAN_DIR = Path(project_root) / "dataclean"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_FILE = "{clean_out}"
OUT_PATH = CLEAN_DIR / CLEAN_FILE
OUT_SQL = str(OUT_PATH).replace("\\", "/")

conn.execute(f"COPY (SELECT * FROM trips_clean) TO '{OUT_SQL}' (FORMAT PARQUET)")
n_out = conn.execute(f"SELECT COUNT(*) FROM read_parquet('{OUT_SQL}')").fetchone()[0]
print(f"Đã ghi {n_out:,} chuyến → dataclean/{CLEAN_FILE}")
'''


def _md(lines: list[str]) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def _code(source: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def _section_cells(title: str, run_lines: list[str]) -> list[dict]:
    return [
        _md([f"### {title}\n"]),
        _code("\n".join(run_lines)),
    ]


def build_notebook(system: str, parquet: str, clean_out: str) -> dict:
    setup = CELL_SETUP.replace("{parquet}", parquet).replace("{system}", system)
    export = CELL_P5.replace("{clean_out}", clean_out)

    cells = [
        _md([
            f"# Khảo sát & làm sạch — {system}\n",
            "\n",
            "Chạy **Run All** từ trên xuống.\n",
            "\n",
            "| Phần | Nội dung |\n",
            "|------|----------|\n",
            "| 0 | Cài đặt & hàm dùng chung |\n",
            "| 1 | Thống kê **trước** clean (`dataraw/`) |\n",
            "| 2 | Áp quy tắc loại bỏ E1–E7 |\n",
            "| 3 | Thống kê **sau** clean |\n",
            "| 4 | Minh chứng (e-bike, bias) |\n",
            "| 5 | Ghi file `dataclean/` |\n",
            "\n",
            "**Giá trị thiếu** được đếm là: `NULL`/`NaN` (cột số) hoặc chuỗi rỗng `""` (cột chữ). "
            "Chi tiết quy tắc: [`docs/report/cleaning_rules.md`](../docs/report/cleaning_rules.md) · số liệu city: [`citibike.md`](../docs/report/citibike.md) / [`divvy.md`](../docs/report/divvy.md) / [`capital.md`](../docs/report/capital.md).\n",
        ]),
        _md(["## Phần 0 — Cài đặt\n"]),
        _code(setup),
        _code(CELL_HELPERS),
        _md([
            "## Phần 1 — Thống kê trước clean\n",
            "\n",
            "Dữ liệu thô từ `dataraw/`. Các bảng dưới giúp quyết định **bỏ** (E1–E7) hay **giữ** (K1–K6).\n",
        ]),
        _md(["### 1.1 Tổng quan\n"]),
        _code(CELL_P1),
        *_section_cells("1.2 Thiếu theo từng cột", ["show_column_missing()"]),
        *_section_cells(
            "1.3 Thiếu đồng thời nhiều cột (TH1–TH7)",
            [
                "print('TH1/TH2 = thiếu tên trạm · TH4/TH5 = thiếu start/end_lat-lng (GPS)\\n')",
                "show_joint_th()",
            ],
        ),
        *_section_cells(
            "1.4 Thời lượng bất thường",
            [
                "print('Ngưỡng Lyft: < 60 giây (E1) · > 24 giờ (E2).\\n')",
                "print('Dòng ↳ = trong chuyến > 24h, bao nhiêu chuyến mất end_lat/end_lng.\\n')",
                "show_duration_outliers()",
            ],
        ),
        _md([
            "## Phần 2 — Clean (E1–E7)\n",
            "\n",
            "Logic trong `src/clean_rules.py`:\n",
            "\n",
            "- **E1** — dưới 60 giây\n",
            "- **E2** — trên 24 giờ\n",
            "- **E3/E4** — mất hết thông tin điểm đi / điểm đến\n",
            "- **E5** — tọa độ (0, 0)\n",
            "- **E6/E7** — thiếu trường bắt buộc / thời gian đảo\n",
            "\n",
            "Sau bước lọc: chuỗi rỗng `""` ở cột trạm được **ép về NULL** để chỉ còn một kiểu thiếu.\n",
        ]),
        _code(CELL_P2),
        _md([
            "## Phần 3 — Thống kê sau clean\n",
            "\n",
            "Cùng bộ bảng như Phần 1, trên view `trips_clean`. "
            "Thiếu chỉ còn dạng **NULL** (không còn `""`). "
            "Kỳ vọng: thời lượng lỗi và mất GPS về 0; có thể còn thiếu **tên trạm** e-bike (K1/K2).\n",
        ]),
        _md(["### 3.1 Tổng quan & so sánh\n"]),
        _code(CELL_P3),
        *_section_cells("3.2 Thiếu theo từng cột (chỉ NULL)", ["show_column_missing(unified=True)"]),
        *_section_cells("3.3 TH1–TH7", ["show_joint_th()"]),
        *_section_cells("3.4 Thời lượng bất thường", ["show_duration_outliers()"]),
        _md([
            "## Phần 4 — Minh chứng\n",
            "\n",
            "Vì sao **giữ** chuyến e-bike thiếu tên trạm nhưng có GPS, và clean có làm lệch member/casual không.\n",
        ]),
        _code(CELL_P4),
        _md(["## Phần 5 — Xuất file clean\n"]),
        _code(export),
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


out_dir = Path(__file__).resolve().parent.parent / "1.statistic"
out_dir.mkdir(parents=True, exist_ok=True)

for fname, parquet, system, clean_out in CONFIGS:
    nb = build_notebook(system, parquet, clean_out)
    path = out_dir / fname
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Wrote", path)
