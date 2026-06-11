# Quy tắc làm sạch (chung 3 hệ)

**Mã:** `src/clean_rules.py` · **Chạy:** `python scripts/run_clean_all.py` · **Minh chứng:** `1.statistic/overview_*.ipynb`

Số liệu từng thành phố: [`citibike.md`](citibike.md) · [`divvy.md`](divvy.md) · [`capital.md`](capital.md)

---

## Nguyên tắc

| Loại | Tiêu chí |
|------|----------|
| **Bỏ E1–E7** | Chuyến không phân tích được: thời lượng sai, mất hết thông tin một đầu, tọa độ lỗi |
| **Giữ K1–K6** | Còn GPS hoặc tên/id trạm; e-bike thiếu tên dock nhưng có GPS = hợp lệ |

**Thiếu trên raw:** `NULL`, `""`, hoặc chỉ khoảng trắng. Sau clean: chuỗi rỗng trạm → `NULL`.

**SQL giữ:** `KEEP_SQL = NOT(E1) AND … AND NOT(E7)` trong `clean_rules.py`.

---

## E1–E7 (loại bỏ)

| Mã | Quy tắc | Lý do |
|----|---------|-------|
| E1 | Thời lượng **< 60 giây** | False start / re-dock |
| E2 | Thời lượng **> 24 giờ** | Giữ xe quá hạn |
| E3 | Mất **hết** start (name, id, lat, lng) | Không biết điểm đi |
| E4 | Mất **hết** end | Không biết điểm đến |
| E5 | lat/lng = 0 | Sentinel |
| E6 | Thiếu `ride_id`, thời gian, `rideable_type`, `member_casual` | Thiếu tối thiểu |
| E7 | `ended_at < started_at` | Timestamp lỗi |

Không bỏ khi chỉ thiếu **một phần** metadata (vd. thiếu tên nhưng còn GPS).

---

## K1–K6 (vẫn giữ)

| Mã | Pattern |
|----|---------|
| K1 | TH1: thiếu tên/id trạm **start**, còn GPS |
| K2 | TH2: thiếu tên/id trạm **end**, còn GPS |
| K3 | TH1 ∧ TH2, còn GPS cả hai đầu |
| K5/K6 | Đủ tên trạm start / end |

**Cột phái sinh:** `has_start_station`, `has_end_station`, `duration_minutes`, `hour_of_day`, `day_of_week`, `is_weekend`.

---

## Quy trình đánh giá missing

1. Đếm missing từng cột trên `dataraw/*_merged.parquet`
2. Đếm TH1–TH7 (nhóm thiếu đồng thời)
3. Áp E1–E7 → `dataclean/`
4. Lặp bước 1–2 trên file clean

---

## Q&A chung

**Sao không bỏ TH1/TH2?** — E-bike đỗ rack (Chicago/DC): thiếu tên dock, vẫn có GPS. Bỏ = mất ~20% chuyến thật.

**Sao Citi sạch hơn?** — NYC bắt mọi xe trả tại dock; không có đỗ rack như Divvy/Capital.

**Phân tích OD theo tên trạm?** — Citi: gần full. Divvy/Capital: lọc `has_start_station = 1` và `has_end_station = 1` (~78–80%).

---

## Reproduce

```bash
python scripts/gen_overview_notebooks.py
python scripts/run_clean_all.py
python scripts/collect_exclusion_stats.py
```
