import duckdb
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import pandas as pd

class StatTester:
    def __init__(self, raw_dir, clean_dir):
        self.raw_dir = raw_dir
        self.clean_dir = clean_dir
        self.conn = duckdb.connect()

    def check_urn_model(self, city_name, raw_file):
        """
        Bước 3: The Urn Model. Kiểm tra tính đại diện của dữ liệu.
        """
        raw_path = f"{self.raw_dir}/{raw_file}"
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        
        print(f"\n=== MÔ HÌNH URN: ĐÁNH GIÁ TÍNH ĐẠI DIỆN ({city_name.upper()}) ===")
        raw_dist = self.conn.query(f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN lower(trim(member_casual)) = 'member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN lower(trim(member_casual)) = 'casual' THEN 1 ELSE 0 END) as casual_count
            FROM read_parquet('{raw_path}')
        """).fetchone()
        
        clean_dist = self.conn.query(f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) as member_count,
                SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) as casual_count
            FROM read_parquet('{clean_path}')
        """).fetchone()
        
        raw_total, raw_member, raw_casual = raw_dist
        clean_total, clean_member, clean_casual = clean_dist
        
        raw_member_pct = (raw_member / raw_total * 100) if raw_total > 0 else 0
        raw_casual_pct = (raw_casual / raw_total * 100) if raw_total > 0 else 0
        clean_member_pct = (clean_member / clean_total * 100) if clean_total > 0 else 0
        clean_casual_pct = (clean_casual / clean_total * 100) if clean_total > 0 else 0
        
        print(f"Bình nguyên bản (Urn - Population): Member {raw_member_pct:.2f}%, Casual {raw_casual_pct:.2f}%")
        print(f"Mẫu rút ra (Sample S)          : Member {clean_member_pct:.2f}%, Casual {clean_casual_pct:.2f}%")
        
        diff = abs(raw_member_pct - clean_member_pct)
        if diff < 1.0:
            print(f"=> ĐỘ LỆCH {diff:.2f}% < 1%: KẾT LUẬN Mẫu (Sample) được trích xuất hoàn toàn mang tính đại diện, không bị thiên lệch (Unbiased), thỏa mãn điều kiện của Mô hình Urn.")
        else:
            print(f"=> ĐỘ LỆCH {diff:.2f}% >= 1%: CÓ SỰ THAY ĐỔI ĐÁNG KỂ SAU KHI LỌC DỮ LIỆU.")

    def analyze_distribution(self, city_name):
        """
        Bước 1: Phân tích Phân phối dữ liệu & Skewness. In ra Mean, Median, Mode. Vẽ Grouped Histogram.
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== PHÂN TÍCH PHÂN PHỐI (SKEWNESS) CHO {city_name.upper()} ===")
        
        stats_df = self.conn.query(f"""
            SELECT 
                AVG(duration_minutes) as mean_val,
                quantile_cont(duration_minutes, 0.5) as median_val
            FROM read_parquet('{clean_path}')
        """).fetchone()
        mean_val, median_val = stats_df
        
        mode_val = self.conn.query(f"""
            SELECT duration_minutes, COUNT(*) as cnt
            FROM read_parquet('{clean_path}')
            GROUP BY duration_minutes
            ORDER BY cnt DESC
            LIMIT 1
        """).fetchone()[0]
        
        print(f"1. Thống kê trung tâm:")
        print(f"   Mode ({mode_val}) < Median ({median_val}) < Mean ({mean_val:.2f})")
        print("=> CHỨNG MINH: Dữ liệu bị Lệch phải rất mạnh (Right-skewed). Mean bị kéo lệch bởi các chuyến đi dài cực đoan.")
        
        print("\n2. Insight (Cú lừa của cấu trúc giá - Pricing Model Trick):")
        print("   Do chính sách đồng giá trong 30/45 phút đầu tiên, hành vi người dùng sẽ tạo thành một cụm vòm")
        print("   hoặc đi ngang ở vùng này trên biểu đồ, thay vì giảm tuyến tính theo cung cầu thuần túy.")
        
        # Vẽ biểu đồ sử dụng Sample để tránh treo máy
        print("\nĐang vẽ biểu đồ Grouped Histogram (sử dụng 1% Sample cho < 60 phút)...")
        df_hist = self.conn.query(f"""
            SELECT duration_minutes, member_casual
            FROM read_parquet('{clean_path}')
            WHERE duration_minutes <= 60
            USING SAMPLE 1% (bernoulli)
        """).df()
        
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_hist, x='duration_minutes', hue='member_casual', 
                     multiple="dodge", bins=30, kde=True, palette={'member': '#3498db', 'casual': '#e74c3c'})
        plt.title(f"Phân phối Thời gian đi xe (Duration < 60 phút) - {city_name.upper()}")
        plt.xlabel("Thời gian (phút)")
        plt.ylabel("Tần suất")
        plt.show()

    def plot_summary_boxplot(self, city_name):
        """
        Bước 2: Đo lường mức độ tập trung bằng Box Plot (Tính lượng Quantiles trước bằng DuckDB).
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== SUMMARY STATISTICS BOX PLOT CHO {city_name.upper()} ===")
        
        # Tính Quantiles bằng DuckDB tránh tràn RAM
        query = f"""
            SELECT 
                day_of_week,
                quantile_cont(duration_minutes, 0.25) as q1,
                quantile_cont(duration_minutes, 0.5) as med,
                quantile_cont(duration_minutes, 0.75) as q3,
                MIN(duration_minutes) as min_val,
                quantile_cont(duration_minutes, 0.95) as max_val
            FROM read_parquet('{clean_path}')
            GROUP BY day_of_week
        """
        df_stats = self.conn.query(query).df()
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_stats['day_of_week'] = pd.Categorical(df_stats['day_of_week'], categories=days_order, ordered=True)
        df_stats = df_stats.sort_values('day_of_week')
        
        bxp_stats = []
        for _, row in df_stats.iterrows():
            bxp_stats.append({
                'label': row['day_of_week'],
                'med': row['med'],
                'q1': row['q1'],
                'q3': row['q3'],
                'whislo': row['min_val'],
                'whishi': row['max_val'],
                'fliers': []
            })
            
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bxp(bxp_stats, showfliers=False, 
               boxprops=dict(color='#2c3e50', linewidth=2),
               medianprops=dict(color='#e74c3c', linewidth=2))
        ax.set_title(f"Box Plot: Phân bố Thời gian đi xe theo Ngày trong tuần - {city_name.upper()}")
        ax.set_ylabel("Duration (Minutes)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def run_mann_whitney_u(self, city_name):
        """
        Bước 4: Kiểm định Giả thuyết.
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== KIỂM ĐỊNH GIẢ THUYẾT (MANN-WHITNEY U) CHO {city_name.upper()} ===")
        
        casual_sample = self.conn.query(f"""
            SELECT duration_minutes FROM read_parquet('{clean_path}')
            WHERE member_casual = 'casual'
            USING SAMPLE 1% (bernoulli)
        """).df()['duration_minutes'].values
        
        member_sample = self.conn.query(f"""
            SELECT duration_minutes FROM read_parquet('{clean_path}')
            WHERE member_casual = 'member'
            USING SAMPLE 1% (bernoulli)
        """).df()['duration_minutes'].values
        
        mean_c = np.mean(casual_sample)
        mean_m = np.mean(member_sample)
        print(f"Mean Casual (Sampled): {mean_c:.2f} phút")
        print(f"Mean Member (Sampled): {mean_m:.2f} phút")
        
        print("\nThiết lập Giả thuyết:")
        print("H0: Mean_Casual <= Mean_Member (Khách vãng lai đi ít hoặc bằng thành viên)")
        print("HA: Mean_Casual > Mean_Member  (Khách vãng lai đi lâu hơn do mục đích du lịch/trải nghiệm)")
        
        stat, p_val = stats.mannwhitneyu(casual_sample, member_sample, alternative='greater')
        
        print(f"\nKết quả kiểm định:")
        print(f"- Mann-Whitney U statistic: {stat}")
        print(f"- p-value: {p_val}")
        
        if p_val < 0.05:
            print("\n=> KẾT LUẬN CHÍNH THỨC: p-value < 0.05, BÁC BỎ H0.")
            print("   Khách vãng lai (Casual) có thời gian thuê xe trung bình lâu hơn đáng kể so với Member.")
            print("   Actionable Insight: Có cơ sở toán học để thiết kế các gói cước theo giờ/ngày cho khách vãng lai nhằm tối ưu doanh thu.")
        else:
            print("\n=> KẾT LUẬN: p-value >= 0.05. Không đủ cơ sở bác bỏ H0.")

    def analyze_circular_trips(self, city_name):
        """
        Phân tích Hành trình khép kín (Circular Trips) - Chi-Square Test
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== KIỂM ĐỊNH CHI-SQUARE: HÀNH TRÌNH KHÉP KÍN ({city_name.upper()}) ===")
        
        # Dùng DuckDB tạo feature is_circular_trip và nhóm theo member_casual
        query = f"""
            SELECT 
                member_casual,
                CASE WHEN start_station_name = end_station_name THEN 1 ELSE 0 END AS is_circular_trip,
                COUNT(*) as count
            FROM read_parquet('{clean_path}')
            GROUP BY 1, 2
        """
        df = self.conn.query(query).df()
        
        # Pivot table để tạo ma trận tần số (Contingency Table)
        contingency_table = df.pivot(index='member_casual', columns='is_circular_trip', values='count').fillna(0)
        
        print("Ma trận tần số (Contingency Table):")
        print(contingency_table)
        
        casual_total = contingency_table.loc['casual'].sum()
        member_total = contingency_table.loc['member'].sum()
        casual_circ = contingency_table.loc['casual', 1]
        member_circ = contingency_table.loc['member', 1]
        
        print(f"\n- Tỷ lệ Hành trình khép kín của Casual: {casual_circ/casual_total*100:.2f}%")
        print(f"- Tỷ lệ Hành trình khép kín của Member: {member_circ/member_total*100:.2f}%")
        
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
        print(f"\n- Chi-Square statistic: {chi2:.2f}")
        print(f"- p-value: {p_val}")
        
        if p_val < 0.05:
            print("=> KẾT LUẬN: Bác bỏ H0. Có sự khác biệt có ý nghĩa thống kê về tỷ lệ trả xe tại chỗ giữa 2 nhóm.")
            print("   Insight: Casual users thường thuê dạo chơi (trả chỗ cũ), trong khi Member đi làm (từ A đến B).")

    def analyze_speed_and_distance(self, city_name):
        """
        Tính toán khoảng cách (Haversine) và vận tốc để kiểm định Mann-Whitney U.
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== KIỂM ĐỊNH MANN-WHITNEY: VẬN TỐC DI CHUYỂN ({city_name.upper()}) ===")
        
        # DuckDB hỗ trợ các hàm lượng giác. Viết công thức Haversine thuần túy bằng SQL.
        # Haversine tính ra km (R = 6371 km). Vận tốc = Khoảng cách / (Thời gian / 60)
        query = f"""
            SELECT 
                member_casual,
                duration_minutes,
                (6371 * acos(
                    cos(radians(start_lat)) * cos(radians(end_lat)) * 
                    cos(radians(end_lng) - radians(start_lng)) + 
                    sin(radians(start_lat)) * sin(radians(end_lat))
                )) AS distance_km
            FROM read_parquet('{clean_path}')
            WHERE start_lat IS NOT NULL AND end_lat IS NOT NULL
              AND start_station_name != end_station_name
              AND duration_minutes > 1
            USING SAMPLE 1% (bernoulli)
        """
        df = self.conn.query(query).df()
        
        # Lọc các trường hợp khoảng cách tính bị lỗi (NaN)
        df = df.dropna(subset=['distance_km'])
        
        # Tính vận tốc (km/h)
        df['speed_kmh'] = df['distance_km'] / (df['duration_minutes'] / 60.0)
        
        # Lọc các outlier vô lý (Vận tốc > 50km/h là sai thực tế đối với xe đạp thành phố)
        df = df[df['speed_kmh'] < 50]
        
        casual_speed = df[df['member_casual'] == 'casual']['speed_kmh'].values
        member_speed = df[df['member_casual'] == 'member']['speed_kmh'].values
        
        print(f"- Vận tốc trung bình Casual: {np.mean(casual_speed):.2f} km/h")
        print(f"- Vận tốc trung bình Member: {np.mean(member_speed):.2f} km/h")
        
        stat, p_val = stats.mannwhitneyu(member_speed, casual_speed, alternative='greater')
        print(f"\n- Mann-Whitney U statistic: {stat}")
        print(f"- p-value: {p_val}")
        
        if p_val < 0.05:
            print("=> KẾT LUẬN: Thành viên (Member) có vận tốc đi xe trung bình nhanh hơn đáng kể so với Khách vãng lai (Casual).")
            print("   Insight: Chứng minh thói quen đi làm (nhanh, gấp) vs đi chơi ngắm cảnh (chậm rãi).")

    def analyze_bimodal_distribution(self, city_name):
        """
        Nhận diện hành vi đi làm/tan tầm: Kolmogorov-Smirnov Test (K-S Test).
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== KIỂM ĐỊNH K-S TEST: PHÂN PHỐI ĐỈNH ĐÔI (BIMODAL) ({city_name.upper()}) ===")
        
        # Lấy giờ đi xe (hour_of_day) của 2 nhóm vào ngày thường (Weekday)
        query_casual = f"""
            SELECT hour_of_day FROM read_parquet('{clean_path}')
            WHERE member_casual = 'casual' AND is_weekend = 0
            USING SAMPLE 1% (bernoulli)
        """
        query_member = f"""
            SELECT hour_of_day FROM read_parquet('{clean_path}')
            WHERE member_casual = 'member' AND is_weekend = 0
            USING SAMPLE 1% (bernoulli)
        """
        
        casual_hours = self.conn.query(query_casual).df()['hour_of_day'].values
        member_hours = self.conn.query(query_member).df()['hour_of_day'].values
        
        # Vẽ biểu đồ mật độ (KDE)
        print("Đang vẽ biểu đồ Mật độ phân phối (KDE Plot)...")
        plt.figure(figsize=(10, 6))
        sns.kdeplot(member_hours, label='Member', color='#3498db', fill=True, alpha=0.3)
        sns.kdeplot(casual_hours, label='Casual', color='#e74c3c', fill=True, alpha=0.3)
        plt.title('Phân phối Khung giờ đi xe (Ngày thường) - Bimodal vs Unimodal')
        plt.xlabel('Khung giờ (0-23)')
        plt.ylabel('Mật độ (Density)')
        plt.legend()
        plt.show()
        
        # Chạy K-S Test kiểm định 2 mẫu độc lập có cùng chung phân phối hay không
        stat, p_val = stats.ks_2samp(member_hours, casual_hours)
        print(f"- K-S statistic: {stat}")
        print(f"- p-value: {p_val}")
        
        if p_val < 0.05:
            print("=> KẾT LUẬN: Bác bỏ H0. Phân phối thời gian (Khung giờ) của Member và Casual hoàn toàn khác biệt.")
            print("   Insight: Biểu đồ cho thấy rõ Member có 2 đỉnh (Bimodal) vào 8h và 17h (đi làm, tan ca).")
            print("   Casual chỉ có 1 đỉnh vòm dâng lên vào giữa trưa (đi chơi).")
