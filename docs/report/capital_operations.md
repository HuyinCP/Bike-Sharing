# Capital Bikeshare (DC metro) — Quy tắc nghiệp vụ & dữ liệu

**Khu vực:** Washington D.C., Maryland, Virginia (Alexandria, Arlington, Montgomery, Fairfax, Prince George's, Falls Church…)  
**Vận hành:** Lyft (Capital Bikeshare) — dữ liệu thuộc Member Jurisdictions  
**Nguồn chính thức:** [system-data](https://capitalbikeshare.com/system-data) · [data-license](https://capitalbikeshare.com/data-license-agreement) · [how-it-works](https://capitalbikeshare.com/how-it-works) · [ebike parking members](https://capitalbikeshare.com/blog/ebike_parking_for_members) · [pricing](https://capitalbikeshare.com/pricing)

Báo cáo thống kê clean: `[capital.md](capital.md)` · Quy tắc clean chung: `[cleaning_rules.md](cleaning_rules.md)`

---

## 1. Quy trình sử dụng (How it works)


| Bước          | Hành động                            | Chi tiết                            |
| ------------- | ------------------------------------ | ----------------------------------- |
| **1. Unlock** | Quét QR                              | App Capital Bikeshare hoặc Lyft     |
| **2. Ride**   | Đạp xe                               | Classic hoặc e-bike                 |
| **3. Park**   | Dock trạm **hoặc** khóa cáp (e-bike) | Đèn dock xanh = kết thúc (nếu dock) |


**Quy mô (2026):** 800+ trạm, ~8.000 xe.

**Kiosk:** Single ride classic không cần smartphone — mua tại kiosk bất kỳ.

**Chương trình đặc biệt:** Adaptive Bike Pilot (đặt trước qua Achilles International).

---

## 2. Quy tắc đỗ / trả xe — chi tiết theo loại xe

### Classic bike — **chỉ dock**


| Quy tắc      | Nội dung                                              |
| ------------ | ----------------------------------------------------- |
| **Điểm trả** | Bất kỳ Capital Bikeshare docking station có chỗ trống |
| **Cấm**      | Đỗ rack, cable lock — **luôn** phải trong dock        |
| **Xác nhận** | Đèn dock xanh                                         |


→ Classic **không** tạo pattern thiếu tên trạm (TH1 classic = 0).

### E-bike — **dock HOẶC public bike rack (cable lock)**


| Phương thức                                            | Phí thêm                          |
| ------------------------------------------------------ | --------------------------------- |
| **Dock tại trạm**                                      | Không                             |
| **Cable lock tại public bike rack** trong service area | **$3** (casual) / **$2** (member) |


Nguồn: [how-it-works](https://capitalbikeshare.com/how-it-works) — *"If you're on an ebike, you can also park at any public bike rack within the service area."*

### Member perk — đỗ miễn phí gần trạm đầy

Áp dụng **annual member** và **Capital Bikeshare for All**:


| Điều kiện   | Chi tiết                              |
| ----------- | ------------------------------------- |
| Trạm “đầy”  | **≤ 3 dock trống** tại thời điểm khóa |
| Khoảng cách | Trong **40 mét** (~131 ft) từ trạm    |
| Cách khóa   | **Bắt buộc** dùng cable lock          |
| Điểm neo    | Public bike rack hoặc vật cố định     |
| Classic     | **Không** áp dụng — vẫn phải dock     |


**Phí bad parking** vẫn áp dụng tại vùng cấm (shaded trên app).

Nguồn: [ebike_parking_for_members](https://capitalbikeshare.com/blog/ebike_parking_for_members)

---

## 3. So sánh loại “trạm / điểm trả”


| Loại điểm                               | Classic    | E-bike                                   | Ghi trong trip data                      |
| --------------------------------------- | ---------- | ---------------------------------------- | ---------------------------------------- |
| **Dock station** (kiosk + dock điện tử) | ✅ Bắt buộc | ✅                                        | `station_name` + `station_id` (BIGINT)   |
| **Public bike rack** (cable lock)       | ❌          | ✅ (+phí hoặc free nếu member + trạm đầy) | Thường **thiếu** tên/id trạm, **có GPS** |
| **E-station riêng** (như Divvy)         | ❌ Không có | ❌ Không có hệ riêng                      | —                                        |


**Khác Divvy:**


| Tiêu chí                 | Capital                   | Divvy                      |
| ------------------------ | ------------------------- | -------------------------- |
| E-station riêng          | Không                     | Có (500+ rack + e-station) |
| Rack approved miễn phí   | Không (trừ waiver member) | Có 500+ rack free          |
| Bán kính trạm đầy        | **40 m** (member free)    | **130 ft** mọi user        |
| Phí rack e-bike (member) | $2                        | $1.20                      |
| Scooter                  | Không                     | Có                         |


**Khác Citi Bike:**


| Tiêu chí          | Capital                   | Citi (NYC)           |
| ----------------- | ------------------------- | -------------------- |
| E-bike rack NYC   | ✅ Có                      | ❌ Không              |
| Overflow geofence | Không (chỉ rack + waiver) | Chỉ JC/Hoboken pilot |


---

## 4. Bảng giá (Pricing)

### Gói chính


| Gói             | Giá       | Unlock | Classic                               | E-bike     |
| --------------- | --------- | ------ | ------------------------------------- | ---------- |
| **Single ride** | $1 + phút | $1     | $0.15/phút                            | $0.35/phút |
| **Day pass**    | $10/ngày  | Free   | 45′ free/chuyến/24h; quá → $0.05/phút | $0.15/phút |
| **Annual**      | $120/năm  | Free   | 45′ free/chuyến; quá → $0.05/phút     | $0.15/phút |


### Member-only perks

- **Bike Angels:** Điểm thưởng khi di chuyển xe từ trạm đông → trạm trống.
- **Free parking near full stations:** E-bike trong 40 m khi ≤3 dock (xem mục 2).
- Reserve-ahead, 5 free unlocks cho bạn bè, early access.

### Gói ưu đãi

- **Capital Bikeshare for All:** $5/năm cho cư dân đủ điều kiện.
- **Bikes for Business:** Gói doanh nghiệp.

Nguồn: [capitalbikeshare.com/pricing](https://capitalbikeshare.com/pricing)

---

## 5. Quy tắc công bố dữ liệu (System Data & License)

### Dữ liệu đã lọc trước khi publish

Theo [system-data](https://capitalbikeshare.com/system-data):


| #   | Quy tắc lọc                                   | Lý do                  |
| --- | --------------------------------------------- | ---------------------- |
| 1   | Chuyến **< 60 giây**                          | False start / re-dock  |
| 2   | Chuyến **staff** bảo trì/kiểm tra             | Không phải người dùng  |
| 3   | Chuyến **đến/từ trạm test** tại kho/warehouse | Trạm thử nghiệm nội bộ |


### Cột mỗi chuyến (mô tả chính thức)

`duration`, `start_date`, `end_date`, `start_station` (name + number), `end_station`, `bike_number`, `member_type`

**Schema file mới (Lyft):** tương thích 14 cột chuẩn dự án; `station_id` kiểu **BIGINT**, thiếu = `Null`, tên thiếu = chuỗi rỗng.

### Member type (mô tả system-data)


| Nhóm           | Loại                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------- |
| **registered** | Annual, 30-Day, Day Key Member                                                           |
| **casual**     | Single Trip, 24-Hour Pass, 3-Day Pass, 5-Day Pass *(5-Day thay bằng 3-Day từ Fall 2011)* |


Trong file mới: gộp thành `member` / `casual`.

### Data License

- Dữ liệu thuộc **Member Jurisdictions** (DC, Alexandria, Montgomery, Fairfax, Arlington, Prince George's, Falls Church).  
- Điều khoản AS IS, cấm correlate danh tính.  
- Luật District of Columbia; forum Washington D.C.

### Ánh xạ pipeline clean


| Quy tắc Lyft                 | Mã dự án            | Thực tế raw (04/2025–04/2026)    |
| ---------------------------- | ------------------- | -------------------------------- |
| < 60s                        | **E1**              | Vẫn còn **~158.098** chuyến <60s |
| Staff + test station         | —                   | Đã lọc phía Lyft                 |
| Thiếu tên + có GPS           | **K1/K2** — **giữ** | ~20% — rack e-bike hợp lệ        |
| `station_id` Null + tên rỗng | Cùng pattern Divvy  | Không đồng nghĩa lỗi dữ liệu     |


---

## 6. Luật đường phố

- Khuyến khích mũ bảo hiểm; đèn đỏ/dừng; cùng chiều giao thông; làn xe; không vỉa hè.

---

## 7. Tóm tắt khác biệt then chốt (vs Citi / Divvy)


| Tiêu chí          | Capital                                           |
| ----------------- | ------------------------------------------------- |
| Classic đỗ rack   | ❌                                                 |
| E-bike đỗ rack    | ✅ (phí hoặc free member gần trạm đầy)             |
| E-station riêng   | ❌                                                 |
| Scooter           | ❌                                                 |
| Waiver trạm đầy   | Member only, ≤3 dock, **40 m**                    |
| % thiếu tên trạm  | **~20%** — giống Divvy (cùng mô hình Lyft e-bike) |
| Lọc test station  | ✅ (giống Citi)                                    |
| Lọc <60s trên raw | Vẫn còn nhiều (~97% loại bỏ là E1)                |


