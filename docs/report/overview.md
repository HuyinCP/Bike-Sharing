# Tổng quan đề tài

## Câu hỏi nghiên cứu

- Nhu cầu thay đổi theo giờ / ngày trong tuần thế nào?
- Giờ đi làm vs cuối tuần có khác không?
- Member vs casual khác nhau ra sao?
- Trạm nào bận, tuyến nào phổ biến, chuyến đi ngắn hay dài?

Phân tích trên **ba hệ bike-share** ở Hoa Kỳ, kỳ **04/2025 – 04/2026** (13 tháng).

## Ba bộ dữ liệu

| Hệ | Vùng | Báo cáo riêng |
|----|------|---------------|
| Citi Bike | New York City | [`citibike.md`](citibike.md) |
| Divvy | Chicago | [`divvy.md`](divvy.md) |
| Capital Bikeshare | DC + MD + VA | [`capital.md`](capital.md) |

**Schema chung:** 14 cột, mỗi dòng = một chuyến (`ride_id`, thời gian, trạm/tọa độ, `rideable_type`, `member_casual`, `data_month`). Chi tiết cột xem từng file city.

**File clean:** `dataclean/*_cleaned.parquet` · **Notebook:** `1.statistic/overview_<city>.ipynb` · **Quy tắc chung:** [`cleaning_rules.md`](cleaning_rules.md)

## Phạm vi thời gian

| | Citi | Divvy | Capital |
|---|------|-------|---------|
| Raw công khai | 2013–nay | 2013–nay | 2010–nay |
| Nhóm phân tích | 04/2025–04/2026 | 04/2025–04/2026 | 04/2025–04/2026 |

Kho gốc: Amazon S3 (tripdata / divvy-tripdata / capitalbikeshare-data). Nhóm gom full kỳ thành Parquet — không lấy mẫu ngẫu nhiên.
