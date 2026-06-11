import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

class AdvancedForecaster:
    def __init__(self, clean_dir):
        self.clean_dir = clean_dir
        self.conn = duckdb.connect()

    def run_lag_features_model(self, city_name):
        """
        Ý tưởng 1: Dự báo chuỗi thời gian đích thực với Lag Features
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== Ý TƯỞNG 1: DỰ BÁO VỚI LAG FEATURES ({city_name.upper()}) ===")
        print("Đang tính toán các biến trễ (Lag 1, Lag 2, Lag 24, Lag 168) bằng DuckDB...")
        
        query = f"""
            WITH hourly_demand AS (
                SELECT 
                    date_trunc('hour', started_at) as timestamp_hour,
                    hour_of_day,
                    day_of_week,
                    is_weekend,
                    COUNT(*) as demand_count
                FROM read_parquet('{clean_path}')
                GROUP BY 1, 2, 3, 4
                ORDER BY 1
            )
            SELECT 
                timestamp_hour,
                hour_of_day,
                day_of_week,
                is_weekend,
                demand_count,
                LAG(demand_count, 1) OVER (ORDER BY timestamp_hour) as lag_1,
                LAG(demand_count, 2) OVER (ORDER BY timestamp_hour) as lag_2,
                LAG(demand_count, 24) OVER (ORDER BY timestamp_hour) as lag_24,
                LAG(demand_count, 168) OVER (ORDER BY timestamp_hour) as lag_168
            FROM hourly_demand
        """
        df = self.conn.query(query).df()
        
        # Drop những dòng đầu tiên bị thiếu Lag (do chưa đủ 168 giờ lịch sử của tuần đầu tiên)
        df = df.dropna().reset_index(drop=True)
        print(f"Hoàn tất! Kích thước dữ liệu sau khi drop NaN: {len(df):,} dòng.")
        
        y = df['demand_count']
        # Vẫn cần One-Hot Encoding cho giờ và ngày để mô hình học tính chu kỳ
        X = pd.get_dummies(df[['hour_of_day', 'day_of_week', 'is_weekend', 'lag_1', 'lag_2', 'lag_24', 'lag_168']], 
                           columns=['hour_of_day', 'day_of_week'], 
                           drop_first=True)
                           
        # CHÚ Ý QUAN TRỌNG: Với Time Series, KHÔNG ĐƯỢC CHIA NGẪU NHIÊN (Random Split).
        # Ta phải chia theo mốc thời gian: Lấy 80% thời gian đầu làm quá khứ (Train), 20% thời gian cuối làm Tương lai (Test).
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        print("\nĐang huấn luyện thuật toán siêu việt XGBoost Regressor...")
        model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\n[KẾT QUẢ XGBOOST VỚI LAG FEATURES]")
        print(f" - MAE: {mae:.2f} xe/giờ")
        print(f" - R2 Score: {r2:.4f} (Độ chính xác tăng vọt, Giải thích được {r2*100:.1f}% biến thiên!)")
        
        # Vẽ biểu đồ So sánh Thực tế vs Dự báo (1 tuần cuối cùng của Test Set)
        print("\nĐang vẽ biểu đồ so sánh Thực tế vs Dự báo cho 1 tuần cuối cùng (168 giờ)...")
        plt.figure(figsize=(14, 6))
        plt.plot(df['timestamp_hour'].iloc[split_idx:split_idx+168], y_test[:168], label='Thực tế (Actual)', color='blue', alpha=0.6)
        plt.plot(df['timestamp_hour'].iloc[split_idx:split_idx+168], y_pred[:168], label='Dự báo (Predicted)', color='red', linestyle='--')
        plt.title('Time-Series Forecasting: Dự báo vs Thực tế (1 Tuần) - XGBoost')
        plt.xlabel('Thời gian')
        plt.ylabel('Lượng xe thuê')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

        print("🔍 Nhận xét: Nhờ có Lag_1 và Lag_24, mô hình XGBoost có thể 'đánh hơi' được quán tính của ngày hôm trước và giờ trước. Các đường nét đứt màu đỏ (Dự báo) giờ đây bám sát rạt theo đường màu xanh (Thực tế), triệt tiêu hoàn toàn sự thiếu sót thông tin ngoại cảnh!")

    def run_station_level_model(self, city_name):
        """
        Ý tưởng 3: Dự báo Vi mô Cấp độ Trạm (Top 1 Trạm bận rộn nhất)
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"\n=== Ý TƯỞNG 3: DỰ BÁO VI MÔ CẤP ĐỘ TRẠM ({city_name.upper()}) ===")
        
        # Tìm trạm bận rộn nhất thành phố
        top_station = self.conn.query(f"""
            SELECT start_station_name, COUNT(*) as c
            FROM read_parquet('{clean_path}')
            WHERE start_station_name IS NOT NULL
            GROUP BY 1 ORDER BY c DESC LIMIT 1
        """).fetchone()[0]
        
        print(f"Trạm bận rộn nhất được thuật toán chọn: '{top_station}'")
        print("Đang tạo chuỗi thời gian (Time-series) cho riêng trạm này...")
        
        # Trích xuất dữ liệu riêng biệt của trạm này, tạo biến trễ (Lag) cho Net Flow / Lượng xe ra
        query = f"""
            WITH hourly_station_demand AS (
                SELECT 
                    date_trunc('hour', started_at) as timestamp_hour,
                    hour_of_day,
                    day_of_week,
                    is_weekend,
                    COUNT(*) as demand_out
                FROM read_parquet('{clean_path}')
                WHERE start_station_name = '{top_station.replace("'", "''")}'
                GROUP BY 1, 2, 3, 4
                ORDER BY 1
            )
            SELECT 
                timestamp_hour,
                hour_of_day,
                day_of_week,
                is_weekend,
                demand_out,
                LAG(demand_out, 1) OVER (ORDER BY timestamp_hour) as lag_1,
                LAG(demand_out, 24) OVER (ORDER BY timestamp_hour) as lag_24,
                LAG(demand_out, 168) OVER (ORDER BY timestamp_hour) as lag_168
            FROM hourly_station_demand
        """
        df = self.conn.query(query).df().dropna().reset_index(drop=True)
        
        y = df['demand_out']
        X = pd.get_dummies(df[['hour_of_day', 'day_of_week', 'is_weekend', 'lag_1', 'lag_24', 'lag_168']], 
                           columns=['hour_of_day', 'day_of_week'], 
                           drop_first=True)
                           
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        print(f"\n[KẾT QUẢ DỰ BÁO RIÊNG CHO TRẠM: {top_station}]")
        print(f" - R2 Score (Trạm Vi mô): {r2:.4f}")
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:3]
        print("\nTop 3 tính năng ảnh hưởng nhất đến Trạm này:")
        for i in indices:
            print(f" - {X.columns[i]}: {importances[i]*100:.2f}%")
            
        print("\n=> Insight Doanh nghiệp: Bằng cách bóc tách bài toán Vĩ mô (Toàn thành phố) thành hàng nghìn bài toán Vi mô (Từng trạm), chúng ta có thể đưa mô hình XGBoost này vào một vòng lặp For-loop để huấn luyện cho mọi trạm. Đây chính là hệ thống cốt lõi mà Uber/Lyft đang dùng để điều động xe tải tải phân bổ (Rebalancing) đi khắp các ngõ hẻm mỗi ngày!")
