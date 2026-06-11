# Citi Bike (NYC) — Quy tắc nghiệp vụ & dữ liệu

**Khu vực:** Manhattan, Brooklyn, Queens, Bronx, Jersey City, Hoboken  
**Vận hành:** NYC Bike Share LLC (Lyft)  
**Nguồn chính thức:** [system-data](https://citibikenyc.com/system-data) · [data-sharing-policy](https://citibikenyc.com/data-sharing-policy) · [how-it-works](https://citibikenyc.com/how-it-works) · [pricing](https://citibikenyc.com/pricing)

Báo cáo thống kê clean: [`citibike.md`](citibike.md) · Quy tắc clean chung: [`cleaning_rules.md`](cleaning_rules.md)

---

## 1. Quy trình sử dụng (How it works)

| Bước | Hành động | Chi tiết |
|------|-----------|----------|
| **1. Unlock** | Quét QR trên xe | App Citi Bike hoặc Lyft |
| **2. Ride** | Đạp xe | Classic (tự đạp) hoặc e-bike (pedal-assist) |
| **3. Park** | Trả tại **dock trạm** | Đèn dock xanh = kết thúc chuyến |

**Nguyên tắc cốt lõi:** Mượn ở trạm A, trả ở **bất kỳ trạm nào** trong hệ thống — không cần trả đúng trạm lấy xe.

**Quy mô (2026):** ~25.000 xe, ~1.500+ trạm.

---

## 2. Quy tắc đỗ / trả xe (Docking)

### Classic bike & e-bike (khu vực NYC chính)

| Quy tắc | Nội dung |
|---------|----------|
| **Bắt buộc** | Trả tại **Citi Bike docking station** có chỗ trống |
| **Không được** | Để xe không giám sát; đỗ rack/cột/lock cáp (không có trên NYC chính) |
| **Cách dock** | Căn tam giác phía trước xe với dock; đẩy nhẹ, **giữ ≥ 5 giây**; đợi đèn xanh |
| **Xác nhận** | Kéo nhẹ tay lái nếu không chắc; dock có thể mất vài phút mới cập nhật app |

Nguồn: [How to dock a bike](https://help.citibikenyc.com/hc/en-us/articles/360032367271-How-to-dock-a-bike)

### Overflow parking (chỉ Jersey City & Hoboken — pilot e-bike)

| Quy tắc | Nội dung |
|---------|----------|
| **Khi nào** | Trạm đầy hoặc gần đầy; tìm **ghim trắng / dấu +** trên app |
| **Loại xe** | **Chỉ e-bike** (có GPS) |
| **Cách đỗ** | Trong vùng geofence đánh dấu sơn/cọc, **cạnh dock**, không chắn lối đi |
| **Phí** | **Miễn phí** nếu kết thúc chuyến đúng trong app |
| **Trạm pilot** | Bergen Ave & Sip Ave, Journal Square (JC); đối diện River St & 1st St (Hoboken) |

**Khác NYC:** Overflow là ngoại lệ duy nhất — vẫn ghi GPS, có thể thiếu `end_station` tùy cách hệ thống ghi nhận.

### Tính năng e-bike đặc thù (JC/Hoboken)

- **Pause ride:** Member có thể tạm dừng (chỉ chuyến bắt đầu tại JC/Hoboken).
- **Reserve docked e-bike:** Member đặt trước e-bike tại trạm (JC/Hoboken).

---

## 3. So sánh loại “trạm / điểm trả”

| Loại | Classic | E-bike NYC | E-bike JC/Hoboken |
|------|---------|------------|-------------------|
| **Dock station** (kiosk + dock điện tử) | ✅ Bắt buộc | ✅ Bắt buộc | ✅ Ưu tiên |
| **Overflow zone** (geofence cạnh trạm) | ❌ | ❌ | ✅ Khi trạm đầy |
| **Public rack / cable lock** | ❌ | ❌ | ❌ |

→ **Hệ quả dữ liệu:** ~100% chuyến có tên/id trạm (trừ lỗi hệ thống ~0,04% raw). Không có pattern “đỗ rack thiếu tên trạm” như Chicago/DC.

---

## 4. Bảng giá (Pricing)

### Gói chính

| Gói | Giá | Classic bike | E-bike |
|-----|-----|--------------|--------|
| **Single ride** | $4.99 / chuyến | 30 phút included, sau đó $0.41/phút | $0.41/phút |
| **Day pass** | $25/ngày | Unlimited chuyến 30 phút/24h; quá 30′ → $0.41/phút | $0.41/phút |
| **Annual (Citi Bike)** | $239/năm (~$19.92/tháng) | 45 phút free/chuyến, sau đó theo bảng | $0.27/phút |
| **Lyft Pink** | $199/năm | 45 phút free/chuyến | $0.27/phút |

### Unlock fee

| Gói | Unlock |
|-----|--------|
| Single ride | $4.99 (gộp trong giá chuyến) |
| Day pass / Annual / Lyft Pink | **Free** |

### Gói ưu đãi

- **Reduced Fare Bike Share:** $5/tháng cho cư dân NYCHA và người nhận SNAP.
- **Bike for Business:** Gói doanh nghiệp.

Nguồn: [citibikenyc.com/pricing](https://citibikenyc.com/pricing)

---

## 5. Quy tắc công bố dữ liệu (System Data & License)

### Dữ liệu đã lọc trước khi publish

Theo [system-data](https://citibikenyc.com/system-data), Lyft **đã xử lý** và loại:

| # | Quy tắc lọc | Lý do nghiệp vụ |
|---|-------------|-----------------|
| 1 | Chuyến **< 60 giây** | False start / re-dock (thử cắm lại để chắc xe khóa) |
| 2 | Chuyến **staff** bảo trì/kiểm tra hệ thống | Không phải chuyến người dùng |
| 3 | Chuyến **đến/từ trạm test** | Trạm thử nghiệm (đặc biệt 06–07/2013) |

### Schema trip history (hiện tại)

`ride_id`, `rideable_type`, `started_at`, `ended_at`, `start_station_name/id`, `end_station_name/id`, `start_lat/lng`, `end_lat/lng`, `member_casual`

**Định kỳ:** Xuất theo tháng trên S3. Tháng >1M chuyến → nhiều CSV trong cùng file nén.

### Data Sharing Policy (pháp lý)

- License: dùng hợp pháp, không bán dataset độc lập.
- Cấm correlate với danh tính khách hàng.
- Data **“AS IS”**, không bảo đảm đầy đủ/chính xác.
- Liên hệ trademark: bike-data@lyft.com

Nguồn: [data-sharing-policy](https://citibikenyc.com/data-sharing-policy)

### Ánh xạ sang pipeline clean của dự án

| Quy tắc Lyft (publish) | Quy tắc dự án (`clean_rules.py`) | Ghi chú thực tế raw |
|------------------------|-----------------------------------|---------------------|
| < 60s | **E1** — loại < 60s | Raw vẫn còn **~492** chuyến <60s (04/2025–04/2026) — lọc Lyft không 100% |
| Staff / test station | *(không có mã riêng)* | Đã lọc phía nhà vận hành |
| > 24h | **E2** | Giữ xe quá hạn / lỗi hệ thống |
| Mất metadata trạm | **E3/E4** | ~0,3% end missing raw → gần 0% sau clean |

---

## 6. Member type trong dữ liệu

| Cột | Giá trị | Ý nghĩa |
|-----|---------|---------|
| `member_casual` | `member` | Annual, Lyft Pink, Reduced Fare… |
| | `casual` | Single ride, Day pass |

*(Schema cũ có `Subscriber` / `Customer` + gender/birth year — không còn trong file mới.)*

---

## 7. Luật đường phố & an toàn

- Đội mũ bảo hiểm (bắt buộc pháp lý NJ cho người < 17).
- Tuân thủ đèn đỏ, đi cùng chiều giao thông.
- Dùng làn xe; không đi vỉa hè.

---

## 8. Tóm tắt khác biệt then chốt (vs Divvy / Capital)

| Tiêu chí | Citi Bike |
|----------|-----------|
| Classic đỗ rack | ❌ Không |
| E-bike đỗ rack (NYC) | ❌ Không |
| E-bike overflow (NJ) | ✅ Pilot, geofence |
| Scooter | ❌ |
| % thiếu tên trạm raw | **~0,3%** (lỗi, không phải nghiệp vụ rack) |
| Lọc <60s trên raw | Hầu hết đã lọc (~99,999% tuân thủ) |
