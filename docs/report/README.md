# Final Project — Data Science · Báo cáo bike-share

Kỳ phân tích: **04/2025 – 04/2026** · Ba hệ: Citi Bike · Divvy · Capital Bikeshare

## Chung

| File | Nội dung |
|------|----------|
| [`overview.md`](overview.md) | Câu hỏi nghiên cứu, schema 14 cột, phạm vi thời gian |
| [`cleaning_rules.md`](cleaning_rules.md) | Quy tắc E1–E7 / K1–K6, Q&A, reproduce |

## Theo từng bộ dữ liệu

| Hệ | Thống kê clean | Nghiệp vụ & quy tắc | JSON raw |
|----|----------------|---------------------|----------|
| Citi Bike (NYC) | [`citibike.md`](citibike.md) | [`citibike_operations.md`](citibike_operations.md) | [`data/citibike_raw_stats.json`](data/citibike_raw_stats.json) |
| Divvy (Chicago) | [`divvy.md`](divvy.md) | [`divvy_operations.md`](divvy_operations.md) | [`data/divvy_raw_stats.json`](data/divvy_raw_stats.json) |
| Capital (DC) | [`capital.md`](capital.md) | [`capital_operations.md`](capital_operations.md) | [`data/capital_raw_stats.json`](data/capital_raw_stats.json) |

**Mã nguồn:** `src/clean_rules.py` · `src/data_cleaner.py` · `scripts/run_clean_all.py` · `1.statistic/overview_*.ipynb`
