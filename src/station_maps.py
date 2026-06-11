"""Bản đồ trạm bike-share — 2.visualize/."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

try:
    import folium
    from folium.plugins import MarkerCluster
except ImportError:  # pragma: no cover
    folium = None
    MarkerCluster = None


def load_station_demand(parquet_path: str | Path) -> pd.DataFrame:
    """
    Gom số chuyến bắt đầu theo trạm.

    - Có station_id → gom theo id (trạm cố định).
    - Không có id (e-bike) → gom theo lat/lng làm tròn 4 chữ số (~11 m).
    Tránh GROUP BY tọa độ thô (hàng trăm nghìn điểm trùng lặp).
    """
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            station_key,
            max(start_station_name) AS station_name,
            max(start_station_id) AS station_id,
            avg(start_lat) AS lat,
            avg(start_lng) AS lng,
            COUNT(*) AS n_trips
        FROM (
            SELECT
                CASE
                    WHEN start_station_id IS NOT NULL
                         AND trim(cast(start_station_id AS VARCHAR)) != ''
                    THEN 'id:' || cast(start_station_id AS VARCHAR)
                    ELSE 'geo:' || printf(
                        '%.4f,%.4f',
                        round(start_lat, 4),
                        round(start_lng, 4)
                    )
                END AS station_key,
                start_station_name,
                start_station_id,
                start_lat,
                start_lng
            FROM read_parquet('{path}')
            WHERE start_lat IS NOT NULL
              AND start_lng IS NOT NULL
              AND start_lat != 0
              AND start_lng != 0
        ) t
        GROUP BY station_key
        ORDER BY n_trips DESC
    """).fetchdf()


def _marker_radius(n_trips: float, n_max: float) -> float:
    if n_max <= 0:
        return 4.0
    t = (float(n_trips) / n_max) ** 0.5
    return 3.0 + t * 11.0


def plot_station_map(
    parquet_path: str | Path,
    system_name: str,
    *,
    top_n: int | None = None,
    tiles: str = "OpenStreetMap",
    use_cluster: bool = True,
) -> "folium.Map":
    """
    Bản đồ thật (OSM) + điểm trạm theo số chuyến bắt đầu.
    Trả về folium.Map — Jupyter hiển thị khi cell là biểu thức cuối.
    """
    if folium is None:
        raise ImportError("Cần cài folium: pip install folium")

    df = load_station_demand(parquet_path)
    if df.empty:
        raise ValueError("Không có trạm nào có tọa độ start_lat/start_lng.")

    if top_n is not None:
        df = df.head(int(top_n)).copy()

    center_lat = float(df["lat"].median())
    center_lng = float(df["lng"].median())
    n_max = float(df["n_trips"].max())

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=12,
        tiles=tiles,
        control_scale=True,
    )

    target = MarkerCluster().add_to(m) if use_cluster and MarkerCluster else m

    for row in df.itertuples(index=False):
        name = row.station_name if pd.notna(row.station_name) else row.station_id
        label = str(name) if pd.notna(name) else "(không tên)"
        n = int(row.n_trips)
        folium.CircleMarker(
            location=[float(row.lat), float(row.lng)],
            radius=_marker_radius(n, n_max),
            popup=folium.Popup(
                f"<b>{label}</b><br>{n:,} chuyến bắt đầu",
                max_width=280,
            ),
            tooltip=f"{label} ({n:,})",
            color="#2c3e50",
            weight=1,
            fill=True,
            fill_color="#e74c3c",
            fill_opacity=0.65,
        ).add_to(target)

    title_html = (
        f'<div style="position:fixed;top:10px;left:50px;z-index:9999;'
        f'background:white;padding:6px 10px;border:1px solid #ccc;'
        f'font-size:13px;border-radius:4px;">'
        f"{system_name} — {len(df):,} điểm trạm (kích thước ∝ số chuyến)"
        f"</div>"
    )
    m.get_root().html.add_child(folium.Element(title_html))
    return m
