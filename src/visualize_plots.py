"""Biểu đồ khám phá dữ liệu clean — 2.visualize/."""

from __future__ import annotations

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

BIKE_LABELS = {
    "classic_bike": "Classic",
    "electric_bike": "E-bike",
    "docked_bike": "Docked",
}

USER_LABELS = {
    "member": "Member",
    "casual": "Casual",
}

USER_COLORS = {
    "member": "#3498db",
    "casual": "#e67e22",
}

BIKE_COLORS = {
    "classic_bike": "#27ae60",
    "electric_bike": "#8e44ad",
    "docked_bike": "#f39c12",
}

BIKE_ORDER = ["classic_bike", "electric_bike"]

USER_BIKE_SEGMENTS = [
    ("member", "classic_bike"),
    ("member", "electric_bike"),
    ("casual", "classic_bike"),
    ("casual", "electric_bike"),
]

# Histogram thời lượng classic vs e-bike — cùng palette & thứ tự chồng với member vs casual
DURATION_BIKE_COLORS = {
    "classic_bike": USER_COLORS["member"],
    "electric_bike": USER_COLORS["casual"],
}
DURATION_BIKE_ORDER = ["electric_bike", "classic_bike"]  # e-bike dưới, classic đè lên

DAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]
DAY_LABELS = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

# Phạm vi phân tích nhóm: 04/2025 – 04/2026 (loại ngoại lệ 31/03/2025 trong raw)
ANALYSIS_START = "2025-04-01"
ANALYSIS_END = "2026-04-30"
ANALYSIS_MONTHS = [f"2025/{m:02d}" for m in range(4, 13)] + [f"2026/{m:02d}" for m in range(1, 5)]


def load_bike_type_counts(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT member_casual, rideable_type, COUNT(*) AS n
        FROM read_parquet('{path}')
        GROUP BY 1, 2
        ORDER BY 1, 3 DESC
    """).fetchdf()


def load_duration_minutes(parquet_path: str | Path) -> np.ndarray:
    path = str(parquet_path).replace("\\", "/")
    return (
        duckdb.connect()
        .execute(f"""
            SELECT duration_minutes::DOUBLE AS m
            FROM read_parquet('{path}')
            WHERE duration_minutes > 0
        """)
        .df()["m"]
        .to_numpy()
    )


def load_user_type_counts(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT member_casual, COUNT(*) AS n
        FROM read_parquet('{path}')
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()


def plot_user_type_pie(parquet_path: str | Path, system_name: str) -> None:
    """Biểu đồ tròn: tỷ lệ member vs casual."""
    df = load_user_type_counts(parquet_path)
    order = ["member", "casual"]
    df = df.set_index("member_casual").reindex(order).dropna()
    labels = [USER_LABELS.get(u, u) for u in df.index]
    colors = ["#3498db", "#e74c3c"]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(df["n"], labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.set_title(f"{system_name} — Tỷ lệ member vs casual")
    plt.tight_layout()
    plt.show()


def plot_bike_type_pie_by_user(parquet_path: str | Path, system_name: str) -> None:
    """Pie chart: tỷ lệ loại xe theo member / casual."""
    df = load_bike_type_counts(parquet_path)
    users = ["member", "casual"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, user in zip(axes, users):
        sub = df[df["member_casual"] == user]
        labels = [BIKE_LABELS.get(x, x) for x in sub["rideable_type"]]
        ax.pie(sub["n"], labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title(USER_LABELS[user])

    fig.suptitle(f"{system_name} — Tỷ lệ loại xe theo nhóm người dùng")
    plt.tight_layout()
    plt.show()


def load_duration_by_bike_stats(parquet_path: str | Path, xmax: int = 120) -> tuple[pd.DataFrame, pd.DataFrame]:
    path = str(parquet_path).replace("\\", "/")
    con = duckdb.connect()
    counts = con.execute(f"""
        SELECT
            rideable_type,
            CAST(duration_minutes AS INTEGER) AS m,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
          AND duration_minutes <= {xmax}
          AND rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2
    """).fetchdf()
    summary = con.execute(f"""
        SELECT
            rideable_type,
            COUNT(*) AS n,
            quantile_cont(duration_minutes, 0.5)
                FILTER (WHERE duration_minutes <= {xmax}) AS med,
            avg(duration_minutes)
                FILTER (WHERE duration_minutes <= {xmax}) AS mean
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
          AND rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1
    """).fetchdf()
    return counts, summary


def _draw_duration_centroid_vlines(
    ax,
    summary: pd.DataFrame,
    group_col: str,
    groups: list[str],
    colors: dict[str, str],
    labels: dict[str, str],
) -> None:
    for g in groups:
        row = summary[summary[group_col] == g]
        if row.empty or pd.isna(row["med"].iloc[0]):
            continue
        med = float(row["med"].iloc[0])
        mean = float(row["mean"].iloc[0])
        lbl = labels[g]
        ax.axvline(
            med, color=colors[g], linestyle="-", linewidth=1.5,
            label=f"{lbl} median ({med:.1f} phút)",
        )
        ax.axvline(
            mean, color=colors[g], linestyle="--", linewidth=1.5,
            label=f"{lbl} mean ({mean:.1f} phút)",
        )


def _plot_duration_by_bike_type(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int,
    as_pct: bool,
) -> None:
    counts, summary = load_duration_by_bike_stats(parquet_path, xmax=xmax)
    minutes = np.arange(0, xmax)

    fig, ax = plt.subplots(figsize=(12, 6))
    for bike in DURATION_BIKE_ORDER:
        sub = counts[counts["rideable_type"] == bike].set_index("m")["n"]
        n_vals = np.array([sub.get(m, 0) for m in minutes], dtype=float)
        if as_pct:
            row = summary.loc[summary["rideable_type"] == bike]
            if row.empty:
                continue
            y_vals = n_vals / int(row["n"].iloc[0]) * 100
        else:
            y_vals = n_vals
        ax.bar(
            minutes + 0.5,
            y_vals,
            width=1.0,
            alpha=0.55,
            color=DURATION_BIKE_COLORS[bike],
            edgecolor="#333333",
            linewidth=0.4,
            label=BIKE_LABELS[bike],
            align="center",
        )

    _draw_duration_centroid_vlines(
        ax, summary, "rideable_type", DURATION_BIKE_ORDER,
        DURATION_BIKE_COLORS, BIKE_LABELS,
    )
    ax.set_xlim(0, xmax)
    ax.set_xlabel("Thời lượng chuyến đi (phút)")
    if as_pct:
        ax.set_ylabel("Tỷ lệ chuyến trong từng loại xe (%)")
        suffix = " (chuẩn hóa theo loại xe)"
    else:
        ax.set_ylabel("Số chuyến")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
        suffix = ""
    ax.set_title(f"{system_name} — Phân phối thời lượng theo loại xe{suffix}")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    plt.show()


def plot_duration_by_bike_type(parquet_path: str | Path, system_name: str, **kwargs) -> None:
    """Histogram chồng: số chuyến theo phút — classic vs e-bike."""
    _plot_duration_by_bike_type(
        parquet_path, system_name,
        xmax=kwargs.get("xmax", 120),
        as_pct=False,
    )


def plot_duration_by_bike_type_pct(parquet_path: str | Path, system_name: str, **kwargs) -> None:
    """Histogram chồng: % trong từng loại xe — classic vs e-bike."""
    _plot_duration_by_bike_type(
        parquet_path, system_name,
        xmax=kwargs.get("xmax", 120),
        as_pct=True,
    )


def load_duration_box_stats_by_bike(
    parquet_path: str | Path,
    xmax: int = 120,
) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            rideable_type,
            COUNT(*) AS n,
            min(duration_minutes) AS vmin,
            quantile_cont(duration_minutes, 0.25) AS q1,
            quantile_cont(duration_minutes, 0.5) AS med,
            quantile_cont(duration_minutes, 0.75) AS q3,
            max(duration_minutes) AS vmax,
            avg(duration_minutes) AS mean
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
          AND duration_minutes <= {xmax}
          AND rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()


def load_duration_box_stats_by_user(
    parquet_path: str | Path,
    xmax: int = 120,
) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            member_casual,
            COUNT(*) AS n,
            min(duration_minutes) AS vmin,
            quantile_cont(duration_minutes, 0.25) AS q1,
            quantile_cont(duration_minutes, 0.5) AS med,
            quantile_cont(duration_minutes, 0.75) AS q3,
            max(duration_minutes) AS vmax,
            avg(duration_minutes) AS mean
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
          AND duration_minutes <= {xmax}
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()


def _duration_row_to_bxp(row: pd.Series) -> dict:
    q1, med, q3 = float(row["q1"]), float(row["med"]), float(row["q3"])
    vmin, vmax = float(row["vmin"]), float(row["vmax"])
    iqr = q3 - q1
    return {
        "med": med,
        "q1": q1,
        "q3": q3,
        "whislo": max(vmin, q1 - 1.5 * iqr),
        "whishi": min(vmax, q3 + 1.5 * iqr),
        "mean": float(row["mean"]),
    }


def _plot_duration_box(
    stats: pd.DataFrame,
    group_col: str,
    groups: list[str],
    labels: dict[str, str],
    colors: dict[str, str],
    system_name: str,
    title_suffix: str,
    *,
    xmax: int = 120,
) -> None:
    bxp_stats = []
    xlabels = []
    box_colors = []
    for g in groups:
        row = stats[stats[group_col] == g]
        if row.empty:
            continue
        bxp_stats.append(_duration_row_to_bxp(row.iloc[0]))
        xlabels.append(labels[g])
        box_colors.append(colors[g])

    if not bxp_stats:
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    positions = list(range(1, len(bxp_stats) + 1))
    bp = ax.bxp(
        bxp_stats,
        positions=positions,
        showfliers=False,
        patch_artist=True,
        widths=0.55,
    )
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.55)
        patch.set_edgecolor("#333333")
    for med_line in bp["medians"]:
        med_line.set_color("#222222")
        med_line.set_linewidth(1.5)

    x_axis = 0.42
    legend_handles: list[Line2D] = []
    for pos, bxp, color, lbl in zip(positions, bxp_stats, box_colors, xlabels):
        mean = bxp["mean"]
        med = bxp["med"]
        x0 = pos - 0.28
        ax.scatter(
            pos, mean, marker="D", s=45, color=color,
            edgecolors="#333333", linewidths=0.8, zorder=5,
        )
        ax.plot([x0, x_axis], [med, med], color=color, linestyle="-", linewidth=1.3, alpha=0.85)
        ax.plot([x0, x_axis], [mean, mean], color=color, linestyle="--", linewidth=1.3, alpha=0.85)
        ax.scatter(x_axis, med, marker=">", s=45, color=color, zorder=5)
        ax.scatter(x_axis, mean, marker="D", s=35, color=color, edgecolors="#333333", zorder=5)
        legend_handles.append(Line2D(
            [0], [0], color=color, linewidth=1.5, linestyle="-",
            label=f"{lbl} — median ({med:.1f} phút)",
        ))
        legend_handles.append(Line2D(
            [0], [0], marker="D", color="w", markerfacecolor=color,
            markeredgecolor="#333333", markersize=7, linestyle="--",
            linewidth=1.3, label=f"{lbl} — mean ({mean:.1f} phút)",
        ))

    ax.set_xticks(positions)
    ax.set_xticklabels(xlabels)
    ax.set_xlim(0.38, max(positions) + 0.55)
    ax.set_ylim(0, xmax)
    ax.set_ylabel("Thời lượng chuyến đi (phút)")
    ax.set_title(f"{system_name} — Box plot thời lượng{title_suffix} (0–{xmax} phút)")
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        fontsize=8,
        frameon=True,
        framealpha=0.92,
    )
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_duration_box_by_bike(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int = 120,
) -> None:
    """Box plot thời lượng — classic vs e-bike (Q1, median, Q3, whisker Tukey)."""
    stats = load_duration_box_stats_by_bike(parquet_path, xmax=xmax)
    _plot_duration_box(
        stats, "rideable_type", BIKE_ORDER, BIKE_LABELS, DURATION_BIKE_COLORS,
        system_name, " — classic vs e-bike",
        xmax=xmax,
    )


def plot_duration_box_by_user(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int = 120,
) -> None:
    """Box plot thời lượng — member vs casual (Q1, median, Q3, whisker Tukey)."""
    stats = load_duration_box_stats_by_user(parquet_path, xmax=xmax)
    _plot_duration_box(
        stats, "member_casual", ["member", "casual"], USER_LABELS, USER_COLORS,
        system_name, " — member vs casual",
        xmax=xmax,
    )


def load_hourly_demand_by_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT rideable_type, hour_of_day, COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).fetchdf()


def _plot_hourly_demand_by_bike(
    parquet_path: str | Path,
    system_name: str,
    *,
    as_pct: bool,
) -> None:
    df = load_hourly_demand_by_bike(parquet_path)
    hours = np.arange(24)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axvspan(7, 9, alpha=0.18, color="#f1c40f", label="Cao điểm sáng 7–9h")
    ax.axvspan(16, 18, alpha=0.18, color="#e67e22", label="Cao điểm chiều 16–18h")

    for bike in BIKE_ORDER:
        sub = df[df["rideable_type"] == bike].set_index("hour_of_day")["n"]
        n_vals = np.array([sub.get(h, 0) for h in hours], dtype=float)
        if as_pct:
            y_vals = n_vals / float(sub.sum()) * 100 if sub.sum() else n_vals
        else:
            y_vals = n_vals
        ax.plot(
            hours, y_vals,
            color=BIKE_COLORS[bike],
            linewidth=2, marker="o", markersize=4,
            label=BIKE_LABELS[bike],
        )

    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 2))
    ax.set_xlabel("Giờ bắt đầu chuyến (0–24)")
    if as_pct:
        ax.set_ylabel("Tỷ lệ chuyến trong từng loại xe (%)")
        suffix = " (chuẩn hóa theo loại xe)"
    else:
        ax.set_ylabel("Số chuyến")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
        suffix = ""
    ax.set_title(f"{system_name} — Nhu cầu theo giờ — classic vs e-bike{suffix}")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_hourly_demand_by_bike_type_count(parquet_path: str | Path, system_name: str) -> None:
    _plot_hourly_demand_by_bike(parquet_path, system_name, as_pct=False)


def plot_hourly_demand_by_bike_type(parquet_path: str | Path, system_name: str) -> None:
    _plot_hourly_demand_by_bike(parquet_path, system_name, as_pct=True)


def load_weekly_usage_by_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT rideable_type, day_of_week, hour_of_day, COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2, 3
        ORDER BY 1, 2, 3
    """).fetchdf()


def load_weekly_usage_by_user_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            member_casual,
            rideable_type,
            day_of_week,
            hour_of_day,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 3, 4
    """).fetchdf()


def _usage_matrix_bike(df: pd.DataFrame, bike: str) -> np.ndarray:
    return _usage_matrix(df[df["rideable_type"] == bike])


def _draw_weekly_heatmap_ax(ax, matrix: np.ndarray, title: str) -> None:
    vmax = matrix.max() if matrix.max() > 0 else 1
    ax.imshow(matrix, aspect="auto", cmap="YlOrRd", origin="upper", vmin=0, vmax=vmax)
    ax.set_xticks(range(0, 24, 4))
    ax.set_xticklabels(range(0, 24, 4), fontsize=8)
    ax.set_yticks(range(7))
    ax.set_yticklabels(DAY_LABELS, fontsize=8)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Giờ", fontsize=8)


def plot_weekly_usage_heatmap_by_bike_type(parquet_path: str | Path, system_name: str) -> None:
    """Heatmap giờ × ngày — classic | e-bike."""
    df = load_weekly_usage_by_bike(parquet_path)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, bike in zip(axes, BIKE_ORDER):
        matrix = _usage_matrix_bike(df, bike)
        _draw_weekly_heatmap_ax(ax, matrix, BIKE_LABELS[bike])
        fig.colorbar(
            ax.images[0], ax=ax, fraction=0.046, pad=0.04, label="Số chuyến",
        )

    fig.suptitle(
        f"Thời gian sử dụng trong tuần theo loại xe — {system_name}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    plt.show()


def plot_weekly_usage_heatmap_user_bike_grid(parquet_path: str | Path, system_name: str) -> None:
    """Heatmap 2×2: member×classic, member×e-bike, casual×classic, casual×e-bike."""
    df = load_weekly_usage_by_user_bike(parquet_path)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    for ax, (user, bike) in zip(axes.flat, USER_BIKE_SEGMENTS):
        sub = df[(df["member_casual"] == user) & (df["rideable_type"] == bike)]
        matrix = _usage_matrix(sub)
        title = f"{USER_LABELS[user]} — {BIKE_LABELS[bike]}"
        _draw_weekly_heatmap_ax(ax, matrix, title)
        fig.colorbar(
            ax.images[0], ax=ax, fraction=0.046, pad=0.04, label="Số chuyến",
        )

    fig.suptitle(
        f"Thời gian sử dụng — 4 nhóm (người dùng × loại xe) — {system_name}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    plt.show()


def _minute_bins(xmax: float, bin_width: int = 1) -> np.ndarray:
    """Cạnh bin: 0, 1, 2, … (mỗi cột = bin_width phút)."""
    upper = int(np.ceil(xmax / bin_width) * bin_width)
    return np.arange(0, upper + bin_width, bin_width)


def _duration_hist_panel(
    ax,
    minutes: np.ndarray,
    *,
    xmax: float | None,
    title: str,
    mean: float,
    median: float,
    skew: float,
    kurt: float,
    bin_width: int = 1,
) -> None:
    if xmax is None:
        xmax = float(np.max(minutes))
        data = minutes
    else:
        data = minutes[minutes <= xmax]

    bins = _minute_bins(xmax, bin_width)
    ax.hist(
        data,
        bins=bins,
        color="#f4b4c4",
        edgecolor="#666666",
        linewidth=0.5,
        density=False,
    )
    ax.axvline(mean, color="red", linestyle="--", linewidth=1.5, label=f"Mean ({mean:.1f})")
    ax.axvline(median, color="#2c3e50", linestyle="-", linewidth=1.5, label=f"Median ({median:.1f})")
    ax.set_xlabel("Thời lượng chuyến đi (phút)")
    ax.set_ylabel("Số chuyến")
    ax.set_title(f"{title}\n(Skewness={skew:.2f}, Kurtosis={kurt:.2f})")
    ax.legend(loc="upper right", fontsize=9)
    if xmax is not None:
        ax.set_xlim(0, xmax)


def plot_duration_distribution(
    parquet_path: str | Path,
    system_name: str,
    *,
    zoom_max: int = 120,
    bin_width: int = 1,
) -> None:
    """Histogram số chuyến theo phút (bin cố định): toàn bộ + phóng to ~2 giờ."""
    minutes = load_duration_minutes(parquet_path)
    mean = float(np.mean(minutes))
    median = float(np.median(minutes))
    skew = float(pd.Series(minutes).skew())
    kurt = float(pd.Series(minutes).kurtosis())

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        f"Phân phối thời lượng chuyến — {system_name}",
        fontsize=13,
        fontweight="bold",
    )

    _duration_hist_panel(
        axes[0], minutes, xmax=None, title="Toàn bộ",
        mean=mean, median=median, skew=skew, kurt=kurt, bin_width=bin_width,
    )
    _duration_hist_panel(
        axes[1], minutes, xmax=zoom_max, title=f"Phóng to 0–{zoom_max} phút",
        mean=mean, median=median, skew=skew, kurt=kurt, bin_width=bin_width,
    )

    plt.tight_layout()
    plt.show()


def load_duration_by_user_stats(parquet_path: str | Path, xmax: int = 120) -> tuple[pd.DataFrame, pd.DataFrame]:
    path = str(parquet_path).replace("\\", "/")
    con = duckdb.connect()
    counts = con.execute(f"""
        SELECT
            member_casual,
            CAST(duration_minutes AS INTEGER) AS m,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
          AND duration_minutes <= {xmax}
        GROUP BY 1, 2
    """).fetchdf()
    summary = con.execute(f"""
        SELECT
            member_casual,
            COUNT(*) AS n,
            quantile_cont(duration_minutes, 0.5)
                FILTER (WHERE duration_minutes <= {xmax}) AS med,
            avg(duration_minutes)
                FILTER (WHERE duration_minutes <= {xmax}) AS mean,
            SUM(CASE WHEN duration_minutes <= 30 THEN 1 ELSE 0 END) AS le30,
            SUM(CASE WHEN duration_minutes > {xmax} THEN 1 ELSE 0 END) AS gt_xmax
        FROM read_parquet('{path}')
        WHERE duration_minutes > 0
        GROUP BY 1
    """).fetchdf()
    return counts, summary


def _plot_duration_by_user_group(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int,
    as_pct: bool,
) -> None:
    counts, summary = load_duration_by_user_stats(parquet_path, xmax=xmax)
    minutes = np.arange(0, xmax)

    fig, ax = plt.subplots(figsize=(12, 6))

    for user in ("member", "casual"):
        sub = counts[counts["member_casual"] == user].set_index("m")["n"]
        n_vals = np.array([sub.get(m, 0) for m in minutes], dtype=float)
        if as_pct:
            n_total = int(summary.loc[summary["member_casual"] == user, "n"].iloc[0])
            y_vals = n_vals / n_total * 100
        else:
            y_vals = n_vals
        ax.bar(
            minutes + 0.5,
            y_vals,
            width=1.0,
            alpha=0.55,
            color=USER_COLORS[user],
            edgecolor="#333333",
            linewidth=0.4,
            label=USER_LABELS[user],
            align="center",
        )

    _draw_duration_centroid_vlines(
        ax, summary, "member_casual", ["member", "casual"],
        USER_COLORS, USER_LABELS,
    )

    ax.set_xlim(0, xmax)
    ax.set_xlabel("Thời lượng chuyến đi (phút)")
    if as_pct:
        ax.set_ylabel("Tỷ lệ chuyến trong từng nhóm (%)")
        suffix = " (chuẩn hóa theo nhóm)"
    else:
        ax.set_ylabel("Số chuyến")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
        suffix = ""
    ax.set_title(f"{system_name} — Phân phối thời lượng theo nhóm người dùng{suffix}")
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    plt.show()


def plot_duration_by_user_group(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int = 120,
) -> None:
    """Histogram chồng: số chuyến theo phút (member vs casual), 0–xmax phút."""
    _plot_duration_by_user_group(
        parquet_path, system_name,
        xmax=xmax, as_pct=False,
    )


def plot_duration_by_user_group_pct(
    parquet_path: str | Path,
    system_name: str,
    *,
    xmax: int = 120,
) -> None:
    """Histogram chồng: % chuyến trong từng nhóm — so sánh hành vi member vs casual."""
    _plot_duration_by_user_group(
        parquet_path, system_name,
        xmax=xmax, as_pct=True,
    )


def load_hourly_demand_by_user(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT member_casual, hour_of_day, COUNT(*) AS n
        FROM read_parquet('{path}')
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).fetchdf()


def _plot_hourly_demand_by_user(
    parquet_path: str | Path,
    system_name: str,
    *,
    as_pct: bool,
) -> None:
    df = load_hourly_demand_by_user(parquet_path)
    hours = np.arange(24)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axvspan(7, 9, alpha=0.18, color="#f1c40f", label="Cao điểm sáng 7–9h")
    ax.axvspan(16, 18, alpha=0.18, color="#e67e22", label="Cao điểm chiều 16–18h")

    for user in ("member", "casual"):
        sub = df[df["member_casual"] == user].set_index("hour_of_day")["n"]
        n_vals = np.array([sub.get(h, 0) for h in hours], dtype=float)
        if as_pct:
            y_vals = n_vals / float(sub.sum()) * 100
        else:
            y_vals = n_vals
        ax.plot(
            hours,
            y_vals,
            color=USER_COLORS[user],
            linewidth=2,
            marker="o",
            markersize=4,
            label=USER_LABELS[user],
        )

    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 2))
    ax.set_xlabel("Giờ bắt đầu chuyến (0–24)")
    if as_pct:
        ax.set_ylabel("Tỷ lệ chuyến trong từng nhóm (%)")
        suffix = " (chuẩn hóa theo nhóm)"
    else:
        ax.set_ylabel("Số chuyến")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
        suffix = ""
    ax.set_title(f"{system_name} — So sánh nhu cầu thuê xe theo giờ trong ngày{suffix}")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_hourly_demand_by_user_count(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: số chuyến theo giờ bắt đầu — member vs casual."""
    _plot_hourly_demand_by_user(parquet_path, system_name, as_pct=False)


def plot_hourly_demand_by_user(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: % chuyến theo giờ bắt đầu — member vs casual trên cùng biểu đồ."""
    _plot_hourly_demand_by_user(parquet_path, system_name, as_pct=True)


def load_monthly_demand_by_user(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            member_casual,
            strftime(started_at::TIMESTAMP, '%Y/%m') AS ym,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE started_at::DATE >= DATE '{ANALYSIS_START}'
          AND started_at::DATE <= DATE '{ANALYSIS_END}'
        GROUP BY 1, 2
        ORDER BY 2, 1
    """).fetchdf()


def _shade_seasonal_months(ax, months: list[str]) -> None:
    for i, ym in enumerate(months):
        mm = int(ym.split("/")[1])
        if mm in (6, 7, 8):
            ax.axvspan(i - 0.5, i + 0.5, alpha=0.18, color="#fdebd0", zorder=0)
        elif mm in (12, 1, 2):
            ax.axvspan(i - 0.5, i + 0.5, alpha=0.18, color="#d6eaf8", zorder=0)


def _plot_monthly_demand_by_user(
    parquet_path: str | Path,
    system_name: str,
    *,
    as_pct: bool,
) -> None:
    df = load_monthly_demand_by_user(parquet_path)
    months = ANALYSIS_MONTHS
    x = np.arange(len(months))

    fig, ax = plt.subplots(figsize=(12, 5))
    _shade_seasonal_months(ax, months)

    for user in ("member", "casual"):
        sub = df[df["member_casual"] == user].set_index("ym")["n"]
        n_vals = np.array([sub.get(m, 0) for m in months], dtype=float)
        if as_pct:
            n_total = float(df.loc[df["member_casual"] == user, "n"].sum())
            y_vals = n_vals / n_total * 100
        else:
            y_vals = n_vals
        ax.plot(
            x,
            y_vals,
            color=USER_COLORS[user],
            linewidth=2,
            marker="o",
            markersize=5,
            label=USER_LABELS[user],
            zorder=2,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.set_xlabel("Tháng")
    if as_pct:
        ax.set_ylabel("Tỷ lệ chuyến trong từng nhóm (%)")
        suffix = " (chuẩn hóa theo nhóm)"
    else:
        ax.set_ylabel("Số chuyến")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
        suffix = ""
    ax.set_title(
        f"{system_name} — Xu hướng nhu cầu theo tháng (04/2025–04/2026){suffix}"
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3, zorder=1)
    plt.tight_layout()
    plt.show()


def plot_monthly_demand_by_user_count(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: số chuyến theo tháng — member vs casual."""
    _plot_monthly_demand_by_user(parquet_path, system_name, as_pct=False)


def plot_monthly_demand_by_user(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: % chuyến theo tháng trong từng nhóm — member vs casual."""
    _plot_monthly_demand_by_user(parquet_path, system_name, as_pct=True)


def load_weekday_demand_by_user(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT member_casual, day_of_week, COUNT(*) AS n
        FROM read_parquet('{path}')
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).fetchdf()


def load_weekday_demand_by_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT rideable_type, day_of_week, COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).fetchdf()


def _shade_weekend(ax) -> None:
    ax.axvspan(4.5, 6.5, alpha=0.15, color="#e8daef", zorder=0, label="Cuối tuần (T7–CN)")


def plot_weekday_demand_by_user(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: số chuyến theo ngày trong tuần — member vs casual."""
    df = load_weekday_demand_by_user(parquet_path)
    x = np.arange(7)

    fig, ax = plt.subplots(figsize=(12, 5))
    _shade_weekend(ax)

    for user in ("member", "casual"):
        sub = df[df["member_casual"] == user].set_index("day_of_week")["n"]
        y_vals = np.array([sub.get(d, 0) for d in DAY_ORDER], dtype=float)
        ax.plot(
            x, y_vals,
            color=USER_COLORS[user],
            linewidth=2, marker="o", markersize=5,
            label=USER_LABELS[user], zorder=2,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(DAY_LABELS)
    ax.set_xlabel("Ngày trong tuần")
    ax.set_ylabel("Số chuyến")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_title(f"{system_name} — Nhu cầu theo ngày trong tuần — member vs casual")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3, zorder=1)
    plt.tight_layout()
    plt.show()


def plot_weekday_demand_by_bike_type(parquet_path: str | Path, system_name: str) -> None:
    """Line chart: số chuyến theo ngày trong tuần — classic vs e-bike."""
    df = load_weekday_demand_by_bike(parquet_path)
    x = np.arange(7)

    fig, ax = plt.subplots(figsize=(12, 5))
    _shade_weekend(ax)

    for bike in BIKE_ORDER:
        sub = df[df["rideable_type"] == bike].set_index("day_of_week")["n"]
        y_vals = np.array([sub.get(d, 0) for d in DAY_ORDER], dtype=float)
        ax.plot(
            x, y_vals,
            color=DURATION_BIKE_COLORS[bike],
            linewidth=2, marker="o", markersize=5,
            label=BIKE_LABELS[bike], zorder=2,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(DAY_LABELS)
    ax.set_xlabel("Ngày trong tuần")
    ax.set_ylabel("Số chuyến")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_title(f"{system_name} — Nhu cầu theo ngày trong tuần — classic vs e-bike")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3, zorder=1)
    plt.tight_layout()
    plt.show()


def load_weekly_usage_counts(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            member_casual,
            day_of_week,
            hour_of_day,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        GROUP BY 1, 2, 3
        ORDER BY 1, 2, 3
    """).fetchdf()


def _usage_matrix(sub: pd.DataFrame) -> np.ndarray:
    if sub.empty:
        return np.zeros((7, 24), dtype=float)
    pivot = (
        sub.pivot(index="day_of_week", columns="hour_of_day", values="n")
        .reindex(DAY_ORDER)
        .fillna(0)
    )
    for h in range(24):
        if h not in pivot.columns:
            pivot[h] = 0
    pivot = pivot[sorted(pivot.columns)]
    return pivot.to_numpy(dtype=float)


def _weekly_usage_matrix(df: pd.DataFrame, user: str) -> np.ndarray:
    return _usage_matrix(df[df["member_casual"] == user])


def plot_weekly_usage_heatmap(parquet_path: str | Path, system_name: str) -> None:
    """Heatmap giờ × ngày — member | casual."""
    df = load_weekly_usage_counts(parquet_path)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, user in zip(axes, ("member", "casual")):
        matrix = _weekly_usage_matrix(df, user)
        _draw_weekly_heatmap_ax(ax, matrix, USER_LABELS[user])
        fig.colorbar(
            ax.images[0], ax=ax, fraction=0.046, pad=0.04, label="Số chuyến",
        )

    fig.suptitle(
        f"Thời gian sử dụng trong tuần — {system_name}",
        fontsize=13, fontweight="bold",
    )
    plt.tight_layout()
    plt.show()


def load_monthly_weekly_usage_counts(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            strftime(started_at::TIMESTAMP, '%Y/%m') AS ym,
            member_casual,
            day_of_week,
            hour_of_day,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE started_at::DATE >= DATE '{ANALYSIS_START}'
          AND started_at::DATE <= DATE '{ANALYSIS_END}'
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 3, 4
    """).fetchdf()


def load_monthly_weekly_usage_by_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            strftime(started_at::TIMESTAMP, '%Y/%m') AS ym,
            rideable_type,
            day_of_week,
            hour_of_day,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE started_at::DATE >= DATE '{ANALYSIS_START}'
          AND started_at::DATE <= DATE '{ANALYSIS_END}'
          AND rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 3, 4
    """).fetchdf()


def load_monthly_weekly_usage_by_user_bike(parquet_path: str | Path) -> pd.DataFrame:
    path = str(parquet_path).replace("\\", "/")
    return duckdb.connect().execute(f"""
        SELECT
            strftime(started_at::TIMESTAMP, '%Y/%m') AS ym,
            member_casual,
            rideable_type,
            day_of_week,
            hour_of_day,
            COUNT(*) AS n
        FROM read_parquet('{path}')
        WHERE started_at::DATE >= DATE '{ANALYSIS_START}'
          AND started_at::DATE <= DATE '{ANALYSIS_END}'
          AND rideable_type IN ('classic_bike', 'electric_bike')
        GROUP BY 1, 2, 3, 4, 5
        ORDER BY 1, 2, 3, 4, 5
    """).fetchdf()


def _draw_monthly_heatmap_cell(
    ax,
    matrix: np.ndarray,
    title: str,
    *,
    show_ylabel: bool,
    show_xlabel: bool,
) -> None:
    vmax = matrix.max() if matrix.max() > 0 else 1
    ax.imshow(matrix, aspect="auto", cmap="YlOrRd", origin="upper", vmin=0, vmax=vmax)
    ax.set_title(title, fontsize=9)
    if show_ylabel:
        ax.set_yticks(range(7))
        ax.set_yticklabels(DAY_LABELS, fontsize=7)
    else:
        ax.set_yticklabels([])
    if show_xlabel:
        ax.set_xticks(range(0, 24, 4))
        ax.set_xticklabels(range(0, 24, 4), fontsize=7)
        ax.set_xlabel("Giờ", fontsize=8)
    else:
        ax.set_xticks([])


def _plot_monthly_usage_heatmaps(
    df: pd.DataFrame,
    system_name: str,
    panels: list[tuple],
    suptitle: str,
) -> None:
    """panels: [(filter_fn(sub_df), title_label), ...] — filter_fn nhận df đã lọc theo tháng."""
    n_months = len(ANALYSIS_MONTHS)
    n_cols = len(panels)
    fig, axes = plt.subplots(
        n_months, n_cols,
        figsize=(3.2 * n_cols + 3, 2.3 * n_months),
    )
    axes = np.atleast_2d(axes)
    if n_cols == 1:
        axes = axes.reshape(n_months, 1)

    for i, ym in enumerate(ANALYSIS_MONTHS):
        month_df = df[df["ym"] == ym]
        for j, (filter_fn, label) in enumerate(panels):
            ax = axes[i, j]
            sub = filter_fn(month_df)
            matrix = _usage_matrix(sub)
            _draw_monthly_heatmap_cell(
                ax, matrix, f"{ym} — {label}",
                show_ylabel=(j == 0),
                show_xlabel=(i == n_months - 1),
            )

    fig.suptitle(suptitle, fontsize=13, fontweight="bold", y=1.002)
    plt.tight_layout()
    plt.show()


def plot_monthly_usage_heatmaps(parquet_path: str | Path, system_name: str) -> None:
    """Lưới heatmap: mỗi tháng × (member | casual), giờ × ngày trong tuần."""
    df = load_monthly_weekly_usage_counts(parquet_path)
    panels = [
        (lambda d, u="member": d[d["member_casual"] == u], USER_LABELS["member"]),
        (lambda d, u="casual": d[d["member_casual"] == u], USER_LABELS["casual"]),
    ]
    _plot_monthly_usage_heatmaps(
        df, system_name, panels,
        f"Thời gian sử dụng theo tháng (04/2025–04/2026) — {system_name}",
    )


def plot_monthly_usage_heatmaps_by_bike_type(parquet_path: str | Path, system_name: str) -> None:
    """Lưới heatmap: mỗi tháng × (classic | e-bike), giờ × ngày trong tuần."""
    df = load_monthly_weekly_usage_by_bike(parquet_path)
    panels = [
        (lambda d, b="classic_bike": d[d["rideable_type"] == b], BIKE_LABELS["classic_bike"]),
        (lambda d, b="electric_bike": d[d["rideable_type"] == b], BIKE_LABELS["electric_bike"]),
    ]
    _plot_monthly_usage_heatmaps(
        df, system_name, panels,
        f"Thời gian sử dụng theo tháng theo loại xe — {system_name}",
    )


def _plot_monthly_usage_heatmaps_user_by_bike(
    parquet_path: str | Path,
    system_name: str,
    user: str,
) -> None:
    df = load_monthly_weekly_usage_by_user_bike(parquet_path)
    panels = [
        (
            lambda d, u=user, b="classic_bike": d[
                (d["member_casual"] == u) & (d["rideable_type"] == b)
            ],
            BIKE_LABELS["classic_bike"],
        ),
        (
            lambda d, u=user, b="electric_bike": d[
                (d["member_casual"] == u) & (d["rideable_type"] == b)
            ],
            BIKE_LABELS["electric_bike"],
        ),
    ]
    _plot_monthly_usage_heatmaps(
        df, system_name, panels,
        f"Thời gian sử dụng theo tháng — {USER_LABELS[user]} (classic | e-bike) — {system_name}",
    )


def plot_monthly_usage_heatmaps_member_by_bike(parquet_path: str | Path, system_name: str) -> None:
    """Lưới heatmap: mỗi tháng × (classic | e-bike) — chỉ member."""
    _plot_monthly_usage_heatmaps_user_by_bike(parquet_path, system_name, "member")


def plot_monthly_usage_heatmaps_casual_by_bike(parquet_path: str | Path, system_name: str) -> None:
    """Lưới heatmap: mỗi tháng × (classic | e-bike) — chỉ casual."""
    _plot_monthly_usage_heatmaps_user_by_bike(parquet_path, system_name, "casual")
