# Citi Bike (NYC)

**Khu vực:** New York City · **Vận hành:** NYC Bike Share LLC  
**Raw:** [`tripdata`](https://s3.amazonaws.com/tripdata/index.html) · **Policy:** [data-sharing-policy](https://citibikenyc.com/data-sharing-policy)  
**Notebook:** `1.statistic/overview_citibike.ipynb` · **Clean:** `dataclean/citibike_nyc_cleaned.parquet`

Quy tắc chung: [`cleaning_rules.md`](cleaning_rules.md)

---

## Nguồn & ghi nhận

Mỗi chuyến mượn–trả ghi thời gian, trạm/tọa độ, loại xe, member/casual. Nhà vận hành lọc staff/test trước khi công bố.

**Đặc điểm vận hành:** Cả classic lẫn e-bike **bắt buộc trả tại dock** — không có đỗ rack như Chicago/DC ([hướng dẫn dock](https://help.citibikenyc.com/hc/en-us/articles/360032367271-How-to-dock-a-bike)).

---

## Kết quả clean (04/2025–04/2026)

| | Số chuyến |
|---|-----------|
| Raw | 48,289,058 |
| Giữ | 48,118,776 (99,65%) |
| Bỏ | 170,282 (0,35%) |

| Mã | Lý do | Bỏ |
|----|-------|-----|
| E1 | < 60 giây | 492 |
| E2 | > 24 giờ | 10,636 |
| E3 | Mất hết start | 24,006 |
| E4 | Mất hết end | 122,613 |
| E5 | Tọa độ (0,0) | 5 |
| E6/E7 | Khác | 0 / (trong E3) |

---

## Missing trước / sau clean

### Trước clean

| Cột | Tổng thiếu | % |
|-----|------------|---|
| start name/id | 24,013 | 0,05% |
| end name | 136,788 | 0,28% |
| end id | 149,399 | 0,31% |
| start lat/lng | 24,013 | 0,05% |
| end lat/lng | 149,084 | 0,31% |

TH1 = 24,013 · TH2 = 136,788 · TH5 = 149,084

### Sau clean

| Cột | Tổng thiếu | % |
|-----|------------|---|
| start (name, id, geo) | **0** | 0% |
| end lat/lng | **0** | 0% |
| end name/id | **18** | ~0% |

TH1–TH7 (trừ TH2=18): **0**. TH4–TH7 = 0.

---

## Pattern giữ (K1–K6)

| Mã | Sau clean |
|----|-----------|
| K1 | 0 |
| K2 | 18 (có GPS end) |
| K3 | 0 |
| K5/K6 | ~100% có tên trạm |

18 chuyến còn thiếu tên trạm đến — có GPS, có thể impute hoặc bỏ riêng khi phân tích OD.

---

## Ghi chú phân tích

- **Heatmap giờ, member/casual, thời lượng:** dùng full clean.
- **Bản đồ / GPS:** full clean (0% thiếu lat/lng).
- **Xếp hạng trạm, OD theo tên:** dùng được gần hết (~100%).
- E-bike thiếu tên (~0,07% raw) thường **mất cả GPS** → E3 loại, không phải đỗ rack.

**JSON thống kê raw:** [`data/citibike_raw_stats.json`](data/citibike_raw_stats.json)
