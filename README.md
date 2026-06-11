# Final Project — Data Science

Phân tích và so sánh ba hệ bike-share tại Hoa Kỳ: **Citi Bike** (NYC), **Divvy** (Chicago), **Capital Bikeshare** (DC).  
Kỳ dữ liệu: **04/2025 – 04/2026** (13 tháng).

## Cấu trúc repo

| Thư mục | Nội dung |
|---------|----------|
| [`1.statistic/`](1.statistic/) | Notebook thống kê tổng quan theo từng city |
| [`2.visualize/`](2.visualize/) | Notebook trực quan hóa |
| [`src/`](src/) | Pipeline làm sạch, quy tắc, vẽ biểu đồ |
| [`scripts/`](scripts/) | Script chạy batch (clean all, generate notebook, …) |
| [`docs/`](docs/) | Báo cáo, slide lớp, sách tham khảo |
| `dataraw/` · `dataclean/` | Parquet gốc & đã làm sạch *(local, không đẩy Git)* |

## Báo cáo

Xem [`docs/report/README.md`](docs/report/README.md) — overview, quy tắc E1–E7, số liệu & nghiệp vụ từng hệ.

## Chạy nhanh

```bash
pip install -r requirements.txt
python scripts/run_clean_all.py
```
