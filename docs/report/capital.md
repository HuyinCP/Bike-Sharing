# Capital Bikeshare (DC metro)

**Khu vực:** Washington D.C., Maryland, Virginia · **Vận hành:** Capital Bikeshare  
**Raw:** `[capitalbikeshare-data](https://s3.amazonaws.com/capitalbikeshare-data/index.html)` · **Policy:** [data-license](https://capitalbikeshare.com/data-license-agreement)  
**Notebook:** `1.statistic/overview_capitalbike.ipynb` · **Clean:** `dataclean/capitalbike_cleaned.parquet`

Quy tắc chung: `[cleaning_rules.md](cleaning_rules.md)`

---

## Nguồn & ghi nhận

Ghi mỗi chuyến, xuất theo tháng. Pattern e-bike tương tự Divvy.

**Đặc điểm vận hành:** Classic bắt buộc dock. E-bike dock hoặc cáp rack ([how-it-works](https://capitalbikeshare.com/how-it-works), [ebike parking](https://capitalbikeshare.com/blog/ebike_parking_for_members)).

**Khác schema:** `start_station_id` / `end_station_id` kiểu **BIGINT** — thiếu = `Null`; tên trạm thiếu = chuỗi rỗng.

---

## Kết quả clean (04/2025–04/2026)


|     | Số chuyến          |
| --- | ------------------ |
| Raw | 6,984,778          |
| Giữ | 6,821,490 (97,66%) |
| Bỏ  | 163,288 (2,34%)    |



| Mã       | Lý do       | Bỏ (tuần tự) |
| -------- | ----------- | ------------ |
| E1       | < 60 giây   | 158,098      |
| E2       | > 24 giờ    | 5,105        |
| E4       | Mất hết end | 85           |
| E3/E5–E7 | Khác        | 0 / ≤35      |


---

## Missing trước / sau clean

### Trước clean


| Cột             | Tổng thiếu | %      |
| --------------- | ---------- | ------ |
| start name      | 1,392,097  | 19,93% |
| start id (Null) | 1,392,097  | 19,93% |
| end name        | 1,445,098  | 20,69% |
| end id (Null)   | 1,447,251  | 20,72% |
| start lat/lng   | 0          | 0%     |
| end lat/lng     | 4,969      | 0,07%  |


TH1 = 1,392,097 · TH2 = 1,445,098 · TH3 = 801,665 · TH5 = 4,969

### Sau clean


| Cột           | Tổng thiếu | %      |
| ------------- | ---------- | ------ |
| start name/id | 1,294,984  | 18,98% |
| end name/id   | 1,319,549  | 19,34% |
| lat/lng       | **0**      | 0%     |


TH4–TH7 = **0**. TH5: 4,969 → 0 (E4).

---

## Pattern giữ (K1–K6)


| Mã  | Sau clean          | Ghi chú              |
| --- | ------------------ | -------------------- |
| K1  | 1,294,984 (19,0%)  | Có GPS start         |
| K2  | 1,319,549 (19,3%)  | Có GPS end           |
| K3  | 710,148 (10,4%)    | Thiếu tên cả hai đầu |
| K5  | 81,0% đủ tên start |                      |
| K6  | 80,7% đủ tên end   |                      |


Classic: không TH1. E-bike ~31% thiếu tên đi, có GPS.

---

## Ghi chú phân tích

- **Giờ, heatmap, member/casual:** full clean.
- **Bản đồ:** full clean.
- **OD theo tên trạm:** lọc `has_*_station = 1` (~80%).
- So sánh % missing với Divvy — cùng mô hình Lyft e-bike rack, **không** phải file “dơ” hơn Citi.

**JSON thống kê raw:** `[data/capital_raw_stats.json](data/capital_raw_stats.json)`