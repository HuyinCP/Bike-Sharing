# Divvy (Chicago) — Quy tắc nghiệp vụ & dữ liệu

**Khu vực:** Chicago, Evanston (Chicagoland)  
**Vận hành:** Lyft (Divvy) — dữ liệu thuộc City of Chicago  
**Nguồn chính thức:** [system-data](https://divvybikes.com/system-data) · [data-license](https://www.divvybikes.com/data-license-agreement) · [how-it-works](https://divvybikes.com/how-it-works) · [parking](https://divvybikes.com/how-it-works/parking) · [pricing](https://divvybikes.com/pricing)

Báo cáo thống kê clean: [`divvy.md`](divvy.md) · Quy tắc clean chung: [`cleaning_rules.md`](cleaning_rules.md)

---

## 1. Quy trình sử dụng (How it works)

| Bước | Hành động | Chi tiết |
|------|-----------|----------|
| **1. Unlock** | Quét QR | App Divvy hoặc Lyft |
| **2. Ride** | Đạp / scoot | Classic bike, e-bike, hoặc **scooter** |
| **3. Park** | Dock **hoặc** khóa cáp (e-bike/scooter) | Đèn dock xanh = kết thúc (nếu dock) |

**Kiosk không smartphone:** Single ride classic có thể mua tại **một số** kiosk Divvy.

---

## 2. Quy tắc đỗ / trả xe — chi tiết theo loại xe

### Classic bike — **chỉ dock**

| Quy tắc | Nội dung |
|---------|----------|
| **Điểm trả** | Bất kỳ trạm Divvy có dock trống |
| **Cách dock** | Căn tam giác đầu xe với dock; đẩy vừa đủ, **không đập mạnh** |
| **Xác nhận** | Đèn dock **xanh**; kéo tay lái kiểm tra |
| **Cấm** | Không để xe không giám sát; **không** đỗ rack/e-station |

→ Mọi classic **luôn có** `start_station` / `end_station` trong dữ liệu (TH1 classic = 0).

### E-bike — **dock HOẶC cable lock** (không làm cả hai)

| Phương thức | Điều kiện | Phí thêm |
|--------------|----------|----------|
| **Dock tại trạm Divvy** | Dock trống | Không |
| **Cable lock tại e-station** | Chỉ e-bike | Không |
| **Cable lock tại rack công cộng được duyệt** | 500+ rack Divvy-approved | Không |
| **Cable lock rack/cột/đèn/biển/đồng hồ đỗ xe công cộng khác** | Trong service area | **$2.40** (casual) / **$1.20** (member) |
| **Trạm đầy — đỗ gần trạm** | Trong **130 ft (~40 m)** của trạm đầy | Theo loại rack (app **không** báo nếu ra ngoài bán kính) |

**Cách khóa cáp:** Lấy cáp từ giá → quấn rack → cắm pin → **beep** + LED xanh rồi nhấp nháy trắng = kết thúc chuyến.

**Cấm:** Khóa vào chính xe, tài sản tư, cây; chắn lối đi/vỉa hè/ramps.

Nguồn: [divvybikes.com/how-it-works/parking](https://divvybikes.com/how-it-works/parking)

### E-station (trạm chỉ e-bike)

| Quy tắc | Nội dung |
|---------|----------|
| **Mục đích** | Tăng chỗ đỗ e-bike, giữ thành phố gọn |
| **Ai được đỗ** | **Chỉ e-bike** Divvy (cable lock) |
| **Cấm** | Classic bike, xe cá nhân |

→ Khác **dock station** thông thường: không có khe cắm dock điện tử cho classic; chỉ điểm neo cáp cho e-bike.

### Scooter

| Quy tắc | Nội dung |
|---------|----------|
| **Đỗ** | Dock trạm **hoặc** khóa tại 600+ rack/post được duyệt (**miễn phí**) |
| **Đỗ vị trí công cộng hợp pháp khác** | +$3.00 (non-member) / +$2.00 (member) |

Nguồn: [how-it-works](https://divvybikes.com/how-it-works)

---

## 3. So sánh loại “trạm / điểm trả”

| Loại điểm | Classic | E-bike | Scooter | Ghi trong trip data |
|-----------|---------|--------|---------|---------------------|
| **Dock station** (kiosk + dock) | ✅ | ✅ | ✅ | `station_name` + `station_id` |
| **E-station** (chỉ khóa cáp e-bike) | ❌ | ✅ free | ❌ | Thường **thiếu** tên trạm, **có GPS** |
| **Approved public rack** | ❌ | ✅ free | ✅ free | Thiếu tên trạm, **có GPS** |
| **Rack/cột khác (có phí)** | ❌ | ✅ | ✅ | Thiếu tên trạm, **có GPS** |
| **130 ft khi trạm đầy** | ❌ (phải tìm trạm khác) | ✅ | — | Thiếu tên trạm, **có GPS** |

**Dock station vs E-station:**

| | Dock station | E-station |
|---|--------------|-----------|
| Cơ chế | Khe cắm vật lý + khóa điện tử | Khóa cáp trên giá đỗ |
| Classic | ✅ | ❌ |
| E-bike | ✅ (dock) hoặc rack gần đó | ✅ (cable only) |
| Dữ liệu | Đủ tên/id trạm | End = GPS, không tên dock |

---

## 4. Bảng giá (Pricing)

### Gói chính

| Gói | Giá | Classic | E-bike | Scooter |
|-----|-----|---------|--------|---------|
| **Single ride** | $1 unlock + phút | $0.20/phút | $0.44/phút | $0.44/phút |
| **Day pass** | $19.90/ngày | 3 giờ free/chuyến/24h; quá → $0.20/phút | Free unlock + $0.44/phút | Free unlock + $0.44/phút |
| **Divvy Annual** | $143.90/năm (*$99 promo member mới*) | 45′ free/chuyến; quá → $0.20/phút | Free unlock + $0.20/phút (phút 31–45 cap $6) | Free unlock + $0.34/phút |
| **Lyft Pink** | $199/năm | 45′ free/chuyến | Free unlock + $0.20/phút | Free unlock + $0.34/phút |

### Gói ưu đãi

- **Divvy for Everyone (D4E):** $5/năm cho cư dân đủ điều kiện (Chicago + Evanston).
- **Bike for Business:** Gói doanh nghiệp — divvyforbusiness@lyft.com

Nguồn: [divvybikes.com/pricing](https://divvybikes.com/pricing)

---

## 5. Quy tắc công bố dữ liệu (System Data & License)

### Dữ liệu đã lọc trước khi publish

Theo [system-data](https://divvybikes.com/system-data):

| # | Quy tắc lọc | Lý do |
|---|-------------|-------|
| 1 | Chuyến **< 60 giây** | False start / re-dock |
| 2 | Chuyến **staff** bảo trì/kiểm tra | Không phải người dùng |

**Không** lọc trạm test (khác Capital/Citi).

### Cột mỗi chuyến

- Thời gian bắt đầu / kết thúc  
- Trạm bắt đầu / kết thúc (tên + id khi dock)  
- `member_casual` → trong mô tả: **Member, Single Ride, Day Pass**  
- `rideable_type`: classic_bike, electric_bike, …  
- Tọa độ lat/lng (luôn có trên raw gần như 100%)

### Data License

- Dữ liệu thuộc **City of Chicago**; trademark DIVVY của thành phố.  
- Điều khoản tương tự Citi/Capital: AS IS, cấm correlate danh tính, không bán dataset độc lập.  
- Luật Illinois; tranh chấp tại NYC (theo agreement).

### Ánh xạ pipeline clean

| Quy tắc Lyft | Mã dự án | Thực tế raw (04/2025–04/2026) |
|--------------|----------|-------------------------------|
| < 60s | **E1** | Vẫn còn **~163.279** chuyến <60s — lọc publish **không đủ** |
| Staff | — | Đã lọc phía Lyft |
| Thiếu tên trạm + có GPS | **K1/K2/K3** — **giữ** | ~20% end/start thiếu tên — **hợp lệ** (rack/e-station) |

---

## 6. Member type trong dữ liệu

| Cột `member_casual` | Ý nghĩa nghiệp vụ |
|---------------------|-------------------|
| `member` | Annual, Lyft Pink, D4E… |
| `casual` | Single Ride, Day Pass |

---

## 7. Luật đường phố

- Khuyến khích đội mũ; tuân thủ luật giao thông; dùng làn xe; không vỉa hè.

---

## 8. Tóm tắt khác biệt then chốt (vs Citi / Capital)

| Tiêu chí | Divvy |
|----------|-------|
| Classic đỗ rack | ❌ Chỉ dock |
| E-bike đỗ rack/cáp | ✅ Rộng nhất (e-station, 500+ rack, 130 ft khi đầy) |
| Scooter | ✅ Có |
| Phí rack e-bike (member) | $1.20 (rẻ hơn Capital $2) |
| Bán kính trạm đầy | **130 ft** (rộng hơn Capital 40 m) |
| % thiếu tên trạm | **~20%** — pattern rack hợp lệ |
| Lọc <60s trên raw | Vẫn còn nhiều (~2,7% tổng loại bỏ là E1) |
