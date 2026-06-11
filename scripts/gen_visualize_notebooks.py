"""Sinh 3 notebook visualize trong 2.visualize/."""
import json
from pathlib import Path

CONFIGS = [
    ("viz_citibike.ipynb", "citibike_nyc_cleaned.parquet", "Citi Bike (NYC)"),
    ("viz_divvybike.ipynb", "divvybike_cleaned.parquet", "Divvy (Chicago)"),
    ("viz_capitalbike.ipynb", "capitalbike_cleaned.parquet", "Capital Bikeshare"),
]

CELL_SETUP = r'''import importlib
import os
import sys
from pathlib import Path

current_dir = os.getcwd()
if current_dir.endswith(("notebooks", "1.statistic", "2.visualize")):
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
else:
    project_root = current_dir

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import src.visualize_plots as visualize_plots
import src.station_maps as station_maps
importlib.reload(visualize_plots)
importlib.reload(station_maps)

from src.visualize_plots import (
    plot_user_type_pie,
    plot_bike_type_pie_by_user,
    plot_duration_by_bike_type,
    plot_duration_by_bike_type_pct,
    plot_duration_box_by_bike,
    plot_hourly_demand_by_bike_type_count,
    plot_hourly_demand_by_bike_type,
    plot_duration_by_user_group,
    plot_duration_by_user_group_pct,
    plot_duration_box_by_user,
    plot_hourly_demand_by_user_count,
    plot_hourly_demand_by_user,
    plot_monthly_demand_by_user_count,
    plot_monthly_demand_by_user,
    plot_weekday_demand_by_bike_type,
    plot_weekday_demand_by_user,
    plot_weekly_usage_heatmap,
    plot_weekly_usage_heatmap_by_bike_type,
    plot_weekly_usage_heatmap_user_bike_grid,
    plot_monthly_usage_heatmaps,
    plot_monthly_usage_heatmaps_by_bike_type,
    plot_monthly_usage_heatmaps_member_by_bike,
    plot_monthly_usage_heatmaps_casual_by_bike,
)
from src.station_maps import plot_station_map

CLEAN_FILE = "{clean_file}"
SYSTEM_NAME = "{system}"
DATA_PATH = Path(project_root) / "dataclean" / CLEAN_FILE

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Chưa có {DATA_PATH}. Chạy scripts/run_clean_all.py trước.")
'''

CELL_USER_PIE = r'''plot_user_type_pie(DATA_PATH, SYSTEM_NAME)
'''

CELL_PIE = r'''plot_bike_type_pie_by_user(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_BIKE = r'''plot_duration_by_bike_type(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_BIKE_PCT = r'''plot_duration_by_bike_type_pct(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_BOX_BIKE = r'''plot_duration_box_by_bike(DATA_PATH, SYSTEM_NAME)
'''

CELL_HOURLY_BIKE_COUNT = r'''plot_hourly_demand_by_bike_type_count(DATA_PATH, SYSTEM_NAME)
'''

CELL_HOURLY_BIKE = r'''plot_hourly_demand_by_bike_type(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_USER = r'''plot_duration_by_user_group(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_USER_PCT = r'''plot_duration_by_user_group_pct(DATA_PATH, SYSTEM_NAME)
'''

CELL_DURATION_BOX_USER = r'''plot_duration_box_by_user(DATA_PATH, SYSTEM_NAME)
'''

CELL_HOURLY_COUNT = r'''plot_hourly_demand_by_user_count(DATA_PATH, SYSTEM_NAME)
'''

CELL_HOURLY = r'''plot_hourly_demand_by_user(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY_COUNT = r'''plot_monthly_demand_by_user_count(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY = r'''plot_monthly_demand_by_user(DATA_PATH, SYSTEM_NAME)
'''

CELL_WEEKDAY_BIKE = r'''plot_weekday_demand_by_bike_type(DATA_PATH, SYSTEM_NAME)
'''

CELL_WEEKDAY_USER = r'''plot_weekday_demand_by_user(DATA_PATH, SYSTEM_NAME)
'''

CELL_HEATMAP = r'''plot_weekly_usage_heatmap(DATA_PATH, SYSTEM_NAME)
'''

CELL_HEATMAP_BIKE = r'''plot_weekly_usage_heatmap_by_bike_type(DATA_PATH, SYSTEM_NAME)
'''

CELL_HEATMAP_USER_BIKE = r'''plot_weekly_usage_heatmap_user_bike_grid(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY_HEATMAP = r'''plot_monthly_usage_heatmaps(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY_HEATMAP_BIKE = r'''plot_monthly_usage_heatmaps_by_bike_type(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY_HEATMAP_MEMBER_BIKE = r'''plot_monthly_usage_heatmaps_member_by_bike(DATA_PATH, SYSTEM_NAME)
'''

CELL_MONTHLY_HEATMAP_CASUAL_BIKE = r'''plot_monthly_usage_heatmaps_casual_by_bike(DATA_PATH, SYSTEM_NAME)
'''

CELL_STATION_MAP = r'''plot_station_map(DATA_PATH, SYSTEM_NAME)
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


out_dir = Path(__file__).resolve().parent.parent / "2.visualize"
out_dir.mkdir(parents=True, exist_ok=True)

for fname, clean_file, system in CONFIGS:
    setup = CELL_SETUP.replace("{clean_file}", clean_file).replace("{system}", system)
    cells = [
        _md([
            f"# {system} — Trực quan hóa\n",
            "\n",
            "Dữ liệu: `dataclean/`. Chạy **Run All** sau khi đã clean.\n",
        ]),
        _code(setup),
        _md(["## Khối 0 · Tổng quan cơ cấu\n"]),
        _md([
            "### 1. Tỷ lệ member vs casual\n",
            "\n",
            "Biểu đồ tròn toàn bộ chuyến trong kỳ phân tích.\n",
        ]),
        _code(CELL_USER_PIE),
        _md([
            "### 2. Tỷ lệ loại xe theo nhóm người dùng\n",
            "\n",
            "Hai pie nhỏ: member và casual, mỗi pie tách classic / e-bike.\n",
        ]),
        _code(CELL_PIE),
        _md(["## Khối A · Classic vs e-bike\n"]),
        _md([
            "### 3. Thời lượng — số chuyến (0–120 phút)\n",
            "\n",
            "Histogram chồng theo số chuyến thực tế.\n",
        ]),
        _code(CELL_DURATION_BIKE),
        _md([
            "### 4. Thời lượng — % trong từng loại xe\n",
            "\n",
            "Mỗi loại xe chuẩn hóa 100% — so sánh hình dạng phân phối.\n",
        ]),
        _code(CELL_DURATION_BIKE_PCT),
        _md([
            "### Box plot — classic vs e-bike (0–120 phút)\n",
            "\n",
            "Tóm tắt Q1, median, Q3 và whisker Tukey — bổ sung cho histogram.\n",
        ]),
        _code(CELL_DURATION_BOX_BIKE),
        _md([
            "### 5. Nhu cầu theo giờ — số chuyến\n",
            "\n",
            "Trục X: giờ bắt đầu (0–23). Vùng vàng/cam: cao điểm 7–9h và 16–18h.\n",
        ]),
        _code(CELL_HOURLY_BIKE_COUNT),
        _md([
            "### 6. Nhu cầu theo giờ — % trong từng loại xe\n",
            "\n",
            "Mỗi loại xe chuẩn hóa 100% theo 24 giờ.\n",
        ]),
        _code(CELL_HOURLY_BIKE),
        _md(["## Khối B · Member vs casual\n"]),
        _md([
            "### 7. Thời lượng — số chuyến (0–120 phút)\n",
            "\n",
            "Histogram chồng theo số chuyến thực tế.\n",
        ]),
        _code(CELL_DURATION_USER),
        _md([
            "### 8. Thời lượng — % trong từng nhóm\n",
            "\n",
            "Mỗi nhóm chuẩn hóa 100% — so sánh hình dạng phân phối.\n",
        ]),
        _code(CELL_DURATION_USER_PCT),
        _md([
            "### Box plot — member vs casual (0–120 phút)\n",
            "\n",
            "Tóm tắt Q1, median, Q3 và whisker Tukey — bổ sung cho histogram.\n",
        ]),
        _code(CELL_DURATION_BOX_USER),
        _md([
            "### 9. Nhu cầu theo giờ — số chuyến\n",
            "\n",
            "Trục X: giờ bắt đầu (0–23).\n",
        ]),
        _code(CELL_HOURLY_COUNT),
        _md([
            "### 10. Nhu cầu theo giờ — % trong từng nhóm\n",
            "\n",
            "Mỗi nhóm chuẩn hóa 100% theo 24 giờ.\n",
        ]),
        _code(CELL_HOURLY),
        _md([
            "### 11. Nhu cầu theo tháng — số chuyến\n",
            "\n",
            "Kỳ 04/2025–04/2026. Nền cam: hè (6–8); nền xanh nhạt: đông (12–2).\n",
        ]),
        _code(CELL_MONTHLY_COUNT),
        _md([
            "### 12. Nhu cầu theo tháng — % trong từng nhóm\n",
            "\n",
            "Mỗi nhóm chuẩn hóa 100% theo 13 tháng.\n",
        ]),
        _code(CELL_MONTHLY),
        _md(["## Khối C · Ngày trong tuần (T2–CN)\n"]),
        _md([
            "### 13. Classic vs e-bike — số chuyến\n",
            "\n",
            "Line chart 7 ngày. Vùng tím nhạt: cuối tuần (T7–CN).\n",
        ]),
        _code(CELL_WEEKDAY_BIKE),
        _md([
            "### 14. Member vs casual — số chuyến\n",
            "\n",
            "Line chart 7 ngày, chỉ số chuyến (không chuẩn hóa %).\n",
        ]),
        _code(CELL_WEEKDAY_USER),
        _md(["## Khối D · Heatmap giờ × ngày — toàn kỳ\n"]),
        _md([
            "### 15. Member | casual\n",
            "\n",
            "Trục X: giờ (0–23). Trục Y: ngày (T2–CN). Mỗi panel scale màu riêng.\n",
        ]),
        _code(CELL_HEATMAP),
        _md([
            "### 16. Classic | e-bike\n",
            "\n",
            "Cùng form với phần 15.\n",
        ]),
        _code(CELL_HEATMAP_BIKE),
        _md([
            "### 17. Lưới 2×2 (người dùng × loại xe)\n",
            "\n",
            "Member×classic, member×e-bike, casual×classic, casual×e-bike.\n",
        ]),
        _code(CELL_HEATMAP_USER_BIKE),
        _md(["## Khối E · Heatmap giờ × ngày — theo tháng\n"]),
        _md([
            "### 18. Member | casual\n",
            "\n",
            "13 hàng (04/2025–04/2026), mỗi hàng 2 cột.\n",
        ]),
        _code(CELL_MONTHLY_HEATMAP),
        _md([
            "### 19. Classic | e-bike\n",
            "\n",
            "13 hàng, 2 cột — cùng form với phần 16.\n",
        ]),
        _code(CELL_MONTHLY_HEATMAP_BIKE),
        _md([
            "### 20. Member — classic | e-bike\n",
            "\n",
            "13 hàng, 2 cột — tách riêng nhóm member.\n",
        ]),
        _code(CELL_MONTHLY_HEATMAP_MEMBER_BIKE),
        _md([
            "### 21. Casual — classic | e-bike\n",
            "\n",
            "13 hàng, 2 cột — tách riêng nhóm casual.\n",
        ]),
        _code(CELL_MONTHLY_HEATMAP_CASUAL_BIKE),
        _md(["## Khối F · Bản đồ trạm\n"]),
        _md([
            "### Bản đồ trạm — số chuyến bắt đầu\n",
            "\n",
            "Nền OpenStreetMap. Gom trạm theo `station_id` hoặc tọa độ làm tròn (e-bike). "
            "Kích thước chấm ∝ số chuyến; cluster khi zoom xa.\n",
        ]),
        _code(CELL_STATION_MAP),
    ]
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = out_dir / fname
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Wrote", path)
