# Divvy (Chicago)

**Khu vực:** Chicago, IL · **Vận hành:** Lyft (Divvy)  
**Raw:** [`divvy-tripdata`](https://divvy-tripdata.s3.amazonaws.com/index.html) · **Policy:** [data-license](https://www.divvybikes.com/data-license-agreement)  
**Notebook:** `1.statistic/overview_divvybike.ipynb` · **Clean:** `dataclean/divvybike_cleaned.parquet`

Quy tắc chung: [`cleaning_rules.md`](cleaning_rules.md)

---

## Nguồn & ghi nhận

Ghi mỗi chuyến mượn–trả, xuất theo tháng trên S3.

**Đặc điểm vận hành:** Classic **chỉ** trả dock. E-bike trả dock **hoặc** khóa cáp tại rack/cột ([quy tắc đỗ](https://divvybikes.com/how-it-works/parking)) → ~20% chuyến thiếu tên trạm nhưng **còn GPS** (K1/K2).

---

## Kết quả clean (04/2025–04/2026)

| | Số chuyến |
|---|-----------|
| Raw | 6,068,796 |
| Giữ | 5,899,156 (97,21%) |
| Bỏ | 169,640 (2,80%) |

| Mã | Lý do | Bỏ (tuần tự) |
|----|-------|--------------|
| E1 | < 60 giây | 163,279 |
| E2 | > 24 giờ | 6,133 |
| E4 | Mất hết end | 228 |
| E3/E5–E7 | Khác | 0 / ≤29 |

E1 chiếm phần lớn — raw vẫn còn chuyến <60s dù Lyft đã lọc một phần trên system-data.

---

## Missing trước / sau clean

### Trước clean

| Cột | Tổng thiếu | % |
|-----|------------|---|
| start name/id | 1,286,941 | 21,21% |
| end name/id | 1,353,498 | 22,30% |
| start lat/lng | 0 | 0% |
| end lat/lng | 6,146 | 0,10% |

TH1 = 1,286,941 · TH2 = 1,353,498 · TH3 = 613,301 · TH5 = 6,146

### Sau clean

| Cột | Tổng thiếu | % |
|-----|------------|---|
| start name/id | 1,187,949 | 20,14% |
| end name/id | 1,225,604 | 20,78% |
| lat/lng (cả hai đầu) | **0** | 0% |

TH4–TH7 = **0**. TH5: 6,146 → 0 (E4).

---

## Pattern giữ (K1–K6)

| Mã | Sau clean | Ghi chú |
|----|-----------|---------|
| K1 | 1,187,949 (20,1%) | E-bike, có GPS start |
| K2 | 1,225,604 (20,8%) | E-bike rack, có GPS end |
| K3 | 518,838 (8,8%) | Thiếu tên cả hai đầu |
| K5 | 79,9% đủ tên start | |
| K6 | 79,2% đủ tên end | |

Classic: **TH1 = 0** (luôn có tên trạm đi). E-bike: ~32% thiếu tên đi, **100% có GPS**.

---

## Ghi chú phân tích

- **Giờ, member/casual, heatmap:** full clean.
- **Bản đồ tọa độ:** full clean (0% thiếu geo).
- **OD / xếp hạng theo tên trạm:** lọc `has_start_station = 1` AND `has_end_station = 1` (~78%).
- ~20% thiếu tên **không nên impute** — chuyến đỗ rack hợp lệ.

**JSON thống kê raw:** [`data/divvy_raw_stats.json`](data/divvy_raw_stats.json)
