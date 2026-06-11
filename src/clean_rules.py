"""Quy tắc làm sạch dữ liệu bike-share — dùng chung cho notebook overview và DataCleaner."""

from __future__ import annotations

from typing import Any

DURATION_SEC_SQL = (
    "date_diff('second', started_at::TIMESTAMP, ended_at::TIMESTAMP)"
)
DURATION_SQL = (
    "date_diff('minute', started_at::TIMESTAMP, ended_at::TIMESTAMP)::DOUBLE"
)

START_DROP_COLS = [
    "start_station_name",
    "start_station_id",
    "start_lat",
    "start_lng",
]
END_DROP_COLS = [
    "end_station_name",
    "end_station_id",
    "end_lat",
    "end_lng",
]

TH1_COLS = ["start_station_name", "start_station_id"]
TH2_COLS = ["end_station_name", "end_station_id"]
TH4_START_COLS = ["start_lat", "start_lng"]
TH5_END_COLS = ["end_lat", "end_lng"]

CRITICAL_COLS = ["ride_id", "started_at", "ended_at", "rideable_type", "member_casual"]


def is_varchar(dtype: str) -> bool:
    d = dtype.upper()
    if any(
        x in d
        for x in (
            "TIMESTAMP",
            "INTEGER",
            "INT",
            "BIGINT",
            "DOUBLE",
            "FLOAT",
            "DECIMAL",
            "BOOLEAN",
            "DATE",
            "TIME",
            "HUGEINT",
        )
    ):
        return False
    return "VARCHAR" in d or "STRING" in d or "BLOB" in d


def missing_expr(col: str, dtype: str) -> str:
    if is_varchar(dtype):
        return (
            f"({col} IS NULL OR {col} = '' "
            f"OR ({col} IS NOT NULL AND regexp_matches({col}, '^[[:space:]]+$')))"
        )
    return f"({col} IS NULL)"


def schema_dtype_map(conn, from_sql: str) -> dict[str, str]:
    df = conn.execute(f"DESCRIBE SELECT * FROM {from_sql} LIMIT 1").fetchdf()
    return dict(zip(df["column_name"], df["column_type"]))


def joint_missing_clause(cols: list[str], dtype_map: dict[str, str]) -> str:
    present = [c for c in cols if c in dtype_map]
    if not present:
        return "FALSE"
    return " AND ".join(missing_expr(c, dtype_map[c]) for c in present)


def th1_clause(dtype_map: dict[str, str]) -> str:
    return joint_missing_clause(TH1_COLS, dtype_map)


def th2_clause(dtype_map: dict[str, str]) -> str:
    return joint_missing_clause(TH2_COLS, dtype_map)


def th4_start_clause(dtype_map: dict[str, str]) -> str:
    return joint_missing_clause(TH4_START_COLS, dtype_map)


def th5_end_clause(dtype_map: dict[str, str]) -> str:
    return joint_missing_clause(TH5_END_COLS, dtype_map)


def unlocatable_start_clause(dtype_map: dict[str, str]) -> str:
    """Không có metadata trạm VÀ không có GPS phía đi."""
    return joint_missing_clause(START_DROP_COLS, dtype_map)


def unlocatable_end_clause(dtype_map: dict[str, str]) -> str:
    """Không có metadata trạm VÀ không có GPS phía đến."""
    return joint_missing_clause(END_DROP_COLS, dtype_map)


def bad_coords_clause(dtype_map: dict[str, str]) -> str:
    parts = []
    if "start_lat" in dtype_map and "start_lng" in dtype_map:
        parts.append("(start_lat = 0 AND start_lng = 0)")
    if "end_lat" in dtype_map and "end_lng" in dtype_map:
        parts.append("(end_lat = 0 AND end_lng = 0)")
    return " OR ".join(parts) if parts else "FALSE"


def critical_missing_clause(dtype_map: dict[str, str]) -> str:
    present = [c for c in CRITICAL_COLS if c in dtype_map]
    if not present:
        return "FALSE"
    return " OR ".join(missing_expr(c, dtype_map[c]) for c in present)


def time_inversion_clause() -> str:
    return "(started_at::TIMESTAMP > ended_at::TIMESTAMP)"


def exclusion_rules(dtype_map: dict[str, str]) -> list[dict[str, str]]:
    """Danh sách quy tắc LOẠI BỎ — chuyến không có ý nghĩa phân tích."""
    return [
        {
            "code": "E1",
            "label": "Thời lượng < 60 giây",
            "sql": f"({DURATION_SEC_SQL} < 60)",
            "reason": "False start / re-dock (theo chuẩn Lyft: loại chuyến dưới 60 giây)",
        },
        {
            "code": "E2",
            "label": "Thời lượng > 24 giờ",
            "sql": f"({DURATION_SEC_SQL} > 86400)",
            "reason": "Giữ xe quá hạn / auto-close hệ thống (~24 giờ)",
        },
        {
            "code": "E3",
            "label": "Không xác định điểm đi (thiếu hết name+id+lat+lng start)",
            "sql": f"({unlocatable_start_clause(dtype_map)})",
            "reason": "Không có tên trạm lẫn GPS phía xuất phát",
        },
        {
            "code": "E4",
            "label": "Không xác định điểm đến (thiếu hết name+id+lat+lng end)",
            "sql": f"({unlocatable_end_clause(dtype_map)})",
            "reason": "Không có tên trạm lẫn GPS phía kết thúc",
        },
        {
            "code": "E5",
            "label": "Tọa độ (0, 0) start hoặc end",
            "sql": f"({bad_coords_clause(dtype_map)})",
            "reason": "Tọa độ sentinel / lỗi ghi nhận",
        },
        {
            "code": "E6",
            "label": "Thiếu trường bắt buộc (ride_id, thời gian, loại xe, user)",
            "sql": f"({critical_missing_clause(dtype_map)})",
            "reason": "Không đủ thông tin tối thiểu cho một chuyến",
        },
        {
            "code": "E7",
            "label": "ended_at trước started_at (không trùng E1)",
            "sql": time_inversion_clause(),
            "reason": "Lỗi timestamp (bắt thêm trường hợp duration âm do thời gian)",
        },
    ]


def keep_where_sql(dtype_map: dict[str, str]) -> str:
    parts = [f"NOT ({r['sql']})" for r in exclusion_rules(dtype_map)]
    return " AND ".join(parts)


STATION_COLS = [
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
]


def nullif_blank_sql(col: str, dtype: str) -> str:
    """Chuẩn hóa blank / chuỗi rỗng → NULL (cột chữ). Cột số giữ nguyên."""
    if is_varchar(dtype):
        return f"NULLIF(trim({col}), '')"
    return col


def station_col_select_sql(col: str, dtype_map: dict[str, str]) -> str:
    if col not in dtype_map:
        return col
    normed = nullif_blank_sql(col, dtype_map[col])
    return col if normed == col else f"{normed} AS {col}"


def station_present_sql(col: str, dtype_map: dict[str, str]) -> str:
    if col not in dtype_map:
        return f"{col} IS NOT NULL"
    dtype = dtype_map[col]
    if is_varchar(dtype):
        return f"{nullif_blank_sql(col, dtype)} IS NOT NULL"
    return f"{col} IS NOT NULL"


def has_start_station_sql(dtype_map: dict[str, str]) -> str:
    return (
        f"CASE WHEN {station_present_sql('start_station_name', dtype_map)} "
        f"AND {station_present_sql('start_station_id', dtype_map)} "
        f"THEN 1 ELSE 0 END"
    )


def has_end_station_sql(dtype_map: dict[str, str]) -> str:
    return (
        f"CASE WHEN {station_present_sql('end_station_name', dtype_map)} "
        f"AND {station_present_sql('end_station_id', dtype_map)} "
        f"THEN 1 ELSE 0 END"
    )


def clean_trips_select_sql(dtype_map: dict[str, str]) -> str:
    """SELECT cột cho tập clean — ép mọi thiếu (blank) về NULL."""
    lines = [
        "ride_id",
        "trim(lower(rideable_type)) AS rideable_type",
        "started_at::TIMESTAMP AS started_at",
        "ended_at::TIMESTAMP AS ended_at",
    ]
    for col in STATION_COLS:
        if col in dtype_map:
            lines.append(station_col_select_sql(col, dtype_map))
    lines.extend([
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
        "trim(lower(member_casual)) AS member_casual",
        f"{DURATION_SQL}::INTEGER AS duration_minutes",
        "extract('hour' FROM started_at::TIMESTAMP) AS hour_of_day",
        "dayname(started_at::TIMESTAMP) AS day_of_week",
        "CASE WHEN dayofweek(started_at::TIMESTAMP) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend",
        f"{has_start_station_sql(dtype_map)} AS has_start_station",
        f"{has_end_station_sql(dtype_map)} AS has_end_station",
    ])
    if "data_month" in dtype_map:
        lines.append("data_month")
    return ",\n                    ".join(lines)


def build_exclusion_context(conn, path_sql: str) -> dict[str, Any]:
    """Sinh toàn bộ mảnh SQL + metadata cho notebook / cleaner."""
    raw_from = f"read_parquet('{path_sql}')"
    dtype_map = schema_dtype_map(conn, raw_from)
    rules = exclusion_rules(dtype_map)
    return {
        "raw_from": raw_from,
        "dtype_map": dtype_map,
        "keep_sql": keep_where_sql(dtype_map),
        "exclusion_rules": rules,
        "th1_sql": th1_clause(dtype_map),
        "th2_sql": th2_clause(dtype_map),
        "th4_start_sql": th4_start_clause(dtype_map),
        "th5_end_sql": th5_end_clause(dtype_map),
        "drop_start_sql": unlocatable_start_clause(dtype_map),
        "drop_end_sql": unlocatable_end_clause(dtype_map),
        "clean_select_sql": clean_trips_select_sql(dtype_map),
    }


def exclusion_breakdown(conn, raw_from: str, dtype_map: dict[str, str]) -> list[dict]:
    """
  Trả về bảng loại bỏ:
  - count_raw: số chuyến khớp điều kiện trên toàn bộ raw
  - count_sequential: số chuyến bị loại ở bước đó trong pipeline (không trùng bước trước)
  """
    rules = exclusion_rules(dtype_map)
    total = conn.execute(f"SELECT COUNT(*) FROM {raw_from}").fetchone()[0]
    keep = keep_where_sql(dtype_map)
    kept = conn.execute(f"SELECT COUNT(*) FROM {raw_from} WHERE {keep}").fetchone()[0]

    rows = []
    prior_or = "FALSE"
    for r in rules:
        sql = r["sql"]
        n_raw = conn.execute(
            f"SELECT COUNT(*) FROM {raw_from} WHERE {sql}"
        ).fetchone()[0]
        n_seq = conn.execute(
            f"SELECT COUNT(*) FROM {raw_from} WHERE ({sql}) AND NOT ({prior_or})"
        ).fetchone()[0]
        rows.append({
            "Mã": r["code"],
            "Lý do loại bỏ": r["label"],
            "Giải thích": r["reason"],
            "Số chuyến (trên raw)": int(n_raw),
            "% raw": round(n_raw / total * 100, 4) if total else 0,
            "Loại bỏ tuần tự (không trùng)": int(n_seq),
        })
        prior_or = f"({prior_or}) OR ({sql})"

    rows.append({
        "Mã": "—",
        "Lý do loại bỏ": "Tổng bị loại (hợp các quy tắc E1–E7)",
        "Giải thích": "OR của tất cả điều kiện loại bỏ",
        "Số chuyến (trên raw)": int(total - kept),
        "% raw": round((total - kept) / total * 100, 4) if total else 0,
        "Loại bỏ tuần tự (không trùng)": int(total - kept),
    })
    rows.append({
        "Mã": "✓",
        "Lý do loại bỏ": "Giữ lại sau clean",
        "Giải thích": "Đủ ý nghĩa: có điểm đi/đến, thời lượng hợp lệ",
        "Số chuyến (trên raw)": int(kept),
        "% raw": round(kept / total * 100, 4) if total else 0,
        "Loại bỏ tuần tự (không trùng)": 0,
    })
    return rows


def kept_pattern_scan(conn, raw_from: str, dtype_map: dict[str, str]) -> list[dict]:
    """Các pattern còn lại trong tập clean — có ý nghĩa nhưng cần lưu ý khi phân tích."""
    keep = keep_where_sql(dtype_map)
    th1, th2 = th1_clause(dtype_map), th2_clause(dtype_map)
    th4, th5 = th4_start_clause(dtype_map), th5_end_clause(dtype_map)
    has_end_name = f"NOT ({missing_expr('end_station_name', dtype_map['end_station_name'])})" if "end_station_name" in dtype_map else "FALSE"

    patterns = [
        ("K1", "TH1: thiếu tên trạm start, có GPS", f"({keep}) AND ({th1}) AND NOT ({th4})"),
        ("K2", "TH2: thiếu tên trạm end, có GPS", f"({keep}) AND ({th2}) AND NOT ({th5})"),
        ("K3", "TH1 và TH2 (thiếu tên cả hai đầu, có GPS)", f"({keep}) AND ({th1}) AND ({th2})"),
        ("K4", "Có end_station_name nhưng thiếu end_lat/lng", f"({keep}) AND ({has_end_name}) AND ({th5})"),
        ("K5", "Đủ tên trạm start (classic/dock)", f"({keep}) AND NOT ({th1})"),
        ("K6", "Đủ tên trạm end", f"({keep}) AND NOT ({th2})"),
    ]
    kept = conn.execute(f"SELECT COUNT(*) FROM {raw_from} WHERE {keep}").fetchone()[0]
    rows = []
    for code, label, sql in patterns:
        n = conn.execute(f"SELECT COUNT(*) FROM {raw_from} WHERE {sql}").fetchone()[0]
        rows.append({
            "Mã": code,
            "Pattern giữ lại": label,
            "Số chuyến": int(n),
            "% trong clean": round(n / kept * 100, 4) if kept else 0,
        })
    return rows
