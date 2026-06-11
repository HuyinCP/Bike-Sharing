"""Thống kê mô tả dữ liệu bike-sharing (bản cleaned)."""

from __future__ import annotations

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import pandas as pd
import pyarrow.parquet as pq
import seaborn as sns


def is_missing_value(s: pd.Series) -> pd.Series:
    missing = s.isna()
    if pd.api.types.is_string_dtype(s) or s.dtype == object:
        missing = missing | (s == "")
        missing = missing | (s.notna() & s.astype(str).str.fullmatch(r"\s+", na=False))
    return missing


def print_dataset_overview(data_path: Path, system_name: str) -> int:
    meta = pq.read_metadata(data_path)
    n_records = meta.num_rows

    print(f"Hệ thống: {system_name}")
    print(f"File: {data_path.name}")
    print(f"Đọc từ: {data_path}")
    print(f"Số record (dòng): {n_records:,}")

    conn = duckdb.connect()
    path_sql = str(data_path).replace("\\", "/")
    n_distinct = conn.execute(
        f"SELECT COUNT(*) FROM (SELECT DISTINCT * FROM read_parquet('{path_sql}'))"
    ).fetchone()[0]
    dup_count = n_records - n_distinct
    dup_pct = (dup_count / n_records) * 100 if n_records else 0
    print(f"Số dòng trùng lặp hoàn toàn: {dup_count:,} ({dup_pct:.4f}%)")

    started = pd.read_parquet(data_path, columns=["started_at"])["started_at"]
    print(f"Khoảng thời gian: {started.min()} → {started.max()}")
    del started
    return n_records


def print_column_stats(data_path: Path, n_records: int) -> None:
    print("=== SỐ UNIQUE & GIÁ TRỊ THIẾU THEO CỘT ===")
    print("Null/NaN: pandas isna() — thường gặp ở cột số.")
    print('Chuỗi rỗng "": so sánh == "" — thường gặp ở cột tên trạm.')
    print('Chỉ khoảng trắng: chuỗi như "   " — isna() và == "" đều không bắt được.\n')

    col_stats = []
    for col in pq.ParquetFile(data_path).schema_arrow.names:
        s = pd.read_parquet(data_path, columns=[col])[col]
        null_count = int(s.isna().sum())
        empty_count = 0
        space_count = 0
        if pd.api.types.is_string_dtype(s) or s.dtype == object:
            str_vals = s.dropna().astype(str)
            empty_count = int((str_vals == "").sum())
            space_count = int(str_vals.str.match(r"^\s+$", na=False).sum())
        missing_total = null_count + empty_count + space_count
        col_stats.append({
            "Cột": col,
            "Kiểu dữ liệu": str(s.dtype),
            "Số unique (không tính null)": int(s.nunique(dropna=True)),
            "Null/NaN": null_count,
            'Chuỗi rỗng ""': empty_count,
            "Chỉ khoảng trắng": space_count,
            "Tổng thiếu": missing_total,
            "Tỷ lệ thiếu (%)": round(missing_total / n_records * 100, 4),
        })
        del s

    display_df = pd.DataFrame(col_stats)
    try:
        from IPython.display import display
        display(display_df)
    except ImportError:
        print(display_df.to_string(index=False))

    station_geo_cols = [
        "start_station_name",
        "end_station_name",
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
    ]
    schema_cols = set(pq.ParquetFile(data_path).schema_arrow.names)
    load_cols = [c for c in station_geo_cols if c in schema_cols]
    if not load_cols:
        return

    df_joint = pd.read_parquet(data_path, columns=load_cols)
    miss_map = {col: is_missing_value(df_joint[col]) for col in load_cols}

    def count_joint_missing(cols: list[str]) -> int:
        cols = [c for c in cols if c in miss_map]
        if not cols:
            return 0
        joint = miss_map[cols[0]]
        for col in cols[1:]:
            joint = joint & miss_map[col]
        return int(joint.sum())

    joint_cases = [
        ("TH1", "start_station_name", ["start_station_name"]),
        ("TH2", "end_station_name", ["end_station_name"]),
        ("TH3", "start_station_name và end_station_name", ["start_station_name", "end_station_name"]),
        ("TH4", "start_lat và start_lng", ["start_lat", "start_lng"]),
        ("TH5", "end_lat và end_lng", ["end_lat", "end_lng"]),
        ("TH6", "start_lat, start_lng, end_lat và end_lng", ["start_lat", "start_lng", "end_lat", "end_lng"]),
        ("TH7", "tất cả cột trên (TH1–TH6)", station_geo_cols),
    ]

    print("\n=== THIẾU ĐỒNG THỜI NHIỀU CỘT ===")
    print('(Cùng định nghĩa thiếu: Null/NaN, chuỗi rỗng "", chỉ khoảng trắng)\n')

    joint_rows = []
    for th_id, desc, cols in joint_cases:
        n_joint = count_joint_missing(cols)
        joint_rows.append({
            "TH": th_id,
            "Mô tả": desc,
            "Số chuyến": n_joint,
            "Tỷ lệ (%)": round(n_joint / n_records * 100, 4),
        })

    joint_df = pd.DataFrame(joint_rows)
    try:
        from IPython.display import display
        display(joint_df)
    except ImportError:
        print(joint_df.to_string(index=False))


def plot_categorical_share(
    data_path: Path,
    column: str,
    system_name: str,
    title_label: str,
    order: list[str],
    palette: dict[str, str],
) -> None:
    print(f"=== TỶ LỆ {title_label.upper()} ({column}) ===\n")
    s = pd.read_parquet(data_path, columns=[column])[column]
    s = s.map(lambda x: "Null" if pd.isna(x) or str(x).strip() == "" else str(x).strip())
    counts = s.value_counts().reindex(order, fill_value=0)
    counts = counts[counts > 0]

    summary = counts.rename("Số chuyến").to_frame().assign(
        **{"Tỷ lệ (%)": (counts / counts.sum() * 100).round(4)}
    )
    try:
        from IPython.display import display
        display(summary)
    except ImportError:
        print(summary)

    sns.set_theme(style="whitegrid", context="talk", font_scale=0.9)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        counts,
        labels=counts.index,
        colors=[palette.get(k, "#999") for k in counts.index],
        autopct="%1.2f%%",
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2},
        textprops={"fontsize": 13},
        pctdistance=0.6,
    )
    for t in ax.texts:
        if "%" in t.get_text():
            t.set_fontsize(16)
            t.set_fontweight("bold")
    ax.set_title(f"{title_label} — {system_name}", fontweight="bold", pad=16)
    plt.tight_layout()
    plt.show()


def investigate_th5_and_duration(data_path: Path, n_records: int) -> None:
    print("=== ĐIỀU TRA TH5: THIẾU end_lat & end_lng vs THỜI LƯỢNG ===")
    print('TH5 = cùng thiếu end_lat và end_lng (Null/NaN, "", chỉ khoảng trắng)\n')

    schema = set(pq.ParquetFile(data_path).schema_arrow.names)
    cols = ["end_lat", "end_lng"]
    if "duration_minutes" in schema:
        cols.append("duration_minutes")
    else:
        cols.extend(["started_at", "ended_at"])

    df = pd.read_parquet(data_path, columns=cols)

    if "duration_minutes" in df.columns:
        duration_min = df["duration_minutes"].astype(float)
    else:
        started = pd.to_datetime(df["started_at"], utc=True, errors="coerce")
        ended = pd.to_datetime(df["ended_at"], utc=True, errors="coerce")
        duration_min = (ended - started).dt.total_seconds() / 60

    th5 = is_missing_value(df["end_lat"]) & is_missing_value(df["end_lng"])
    negative = duration_min < 0
    over_24h = duration_min >= 1440
    in_24_25h = (duration_min >= 1440) & (duration_min < 1500)
    normal = ~negative & ~over_24h

    n_th5 = int(th5.sum())
    n_neg = int(negative.sum())
    n_over24 = int(over_24h.sum())

    breakdown_rows = [
        ("TH5 & thời lượng ÂM", th5 & negative),
        ("TH5 & ≥ 24 giờ", th5 & over_24h),
        ("TH5 & ≥ 24 giờ (bucket 24–25h)", th5 & in_24_25h),
        ("TH5 & 0 ≤ dur < 24h (ngoại lệ)", th5 & normal),
    ]
    df_th5_breakdown = pd.DataFrame([
        {
            "Nhóm": label,
            "Số chuyến": int(mask.sum()),
            "% trong TH5": round(int(mask.sum()) / n_th5 * 100, 2) if n_th5 else 0,
            "% tổng dataset": round(int(mask.sum()) / n_records * 100, 4),
        }
        for label, mask in breakdown_rows
    ])

    cross_rows = [
        ("Chuyến thời lượng ÂM", n_neg, int((negative & th5).sum())),
        ("Chuyến ≥ 24 giờ", n_over24, int((over_24h & th5).sum())),
        ("TH5 (thiếu end_lat & end_lng)", n_th5, n_th5),
    ]
    df_cross = pd.DataFrame(cross_rows, columns=["Nhóm", "Tổng", "Có TH5 (thiếu end geo)"])
    df_cross["% TH5 trong nhóm"] = (
        df_cross["Có TH5 (thiếu end geo)"] / df_cross["Tổng"] * 100
    ).round(2)

    try:
        from IPython.display import display
        display(df_th5_breakdown)
        display(df_cross)
    except ImportError:
        print(df_th5_breakdown.to_string(index=False))
        print(df_cross.to_string(index=False))

    if n_th5 == 0:
        print("\n=> Sau làm sạch: không còn TH5 (đã lọc trạm null / outlier thời lượng).")
    else:
        pct_th5_from_over24 = (th5 & over_24h).sum() / n_th5 * 100
        print(f"\n=> {pct_th5_from_over24:.1f}% TH5 nằm trong chuyến ≥ 24h.")


def print_temporal_summary(data_path: Path) -> None:
    print("=== THỐNG KÊ THỜI GIAN (SAU LÀM SẠCH) ===\n")
    path_sql = str(data_path).replace("\\", "/")
    conn = duckdb.connect()
    schema = set(pq.ParquetFile(data_path).schema_arrow.names)

    if "duration_minutes" in schema:
        row = conn.execute(f"""
            SELECT MIN(duration_minutes), MAX(duration_minutes),
                   AVG(duration_minutes), MEDIAN(duration_minutes)
            FROM read_parquet('{path_sql}')
        """).fetchone()
        print(
            f"duration_minutes — min: {row[0]}, max: {row[1]}, "
            f"mean: {row[2]:.2f}, median: {row[3]:.1f}"
        )

    if "hour_of_day" in schema:
        print("\nTop 5 giờ có nhiều chuyến nhất:")
        print(conn.execute(f"""
            SELECT hour_of_day, COUNT(*) AS n
            FROM read_parquet('{path_sql}')
            GROUP BY 1 ORDER BY n DESC LIMIT 5
        """).df().to_string(index=False))

    if "day_of_week" in schema:
        print("\nSố chuyến theo ngày trong tuần:")
        print(conn.execute(f"""
            SELECT day_of_week, COUNT(*) AS n
            FROM read_parquet('{path_sql}')
            GROUP BY 1 ORDER BY n DESC
        """).df().to_string(index=False))

    if "is_weekend" in schema:
        wk = conn.execute(f"""
            SELECT is_weekend, COUNT(*) AS n
            FROM read_parquet('{path_sql}')
            GROUP BY 1
        """).df().set_index("is_weekend")["n"]
        print(f"\nCuối tuần (is_weekend=1): {wk.get(1, 0):,} | Ngày thường (0): {wk.get(0, 0):,}")
