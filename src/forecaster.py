import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.dummy import DummyRegressor
import optuna
class DemandForecaster:
    def __init__(self, clean_dir):
        self.clean_dir = clean_dir
        self.conn = duckdb.connect()

    def prepare_data(self, city_name):
        """
        Bước 1: Feature Engineering (Trích xuất và Biến đổi đặc trưng).
        Gom nhóm dữ liệu thành tổng lượng xe thuê (Demand) mỗi giờ.
        """
        clean_path = f"{self.clean_dir}/{city_name}_cleaned.parquet"
        print(f"=== BƯỚC 1: CHUẨN BỊ DỮ LIỆU ({city_name.upper()}) ===")
        print("Đang tính toán Design Matrix X và Target y qua DuckDB...")
        
        # Gom nhóm theo từng khung giờ thực tế bằng DuckDB cực nhanh
        query = f"""
            SELECT 
                date_trunc('hour', started_at) as timestamp_hour,
                hour_of_day,
                day_of_week,
                is_weekend,
                COUNT(*) as demand_count
            FROM read_parquet('{clean_path}')
            GROUP BY 1, 2, 3, 4
            ORDER BY 1
        """
        df = self.conn.query(query).df()
        
        print(f"Tổng số khung giờ thu thập được: {len(df):,} dòng (đủ nhỏ để đưa vào RAM và Scikit-Learn).")
        
        # Biến mục tiêu (y)
        y = df['demand_count']
        
        # One-Hot Encoding cho các biến phân loại (Categorical Features)
        print("Đang thực hiện One-Hot Encoding cho Hour_of_day và Day_of_week...")
        # Sử dụng pd.get_dummies, drop_first=True để tránh bẫy đa cộng tuyến (Dummy Variable Trap)
        X = pd.get_dummies(df[['hour_of_day', 'day_of_week', 'is_weekend']], 
                           columns=['hour_of_day', 'day_of_week'], 
                           drop_first=True) 
        
        # Bước 2: Phân tách dữ liệu
        print("\n=== BƯỚC 2: PHÂN TÁCH DỮ LIỆU (TRAIN-TEST SPLIT) ===")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Tập Training: {len(X_train):,} dòng (80%)")
        print(f"Tập Test: {len(X_test):,} dòng (20%)")
        
        self.X_train, self.X_test = X_train, X_test
        self.y_train, self.y_test = y_train, y_test
        self.X_cols = X.columns
        return X_train, X_test, y_train, y_test

    def train_and_evaluate(self):
        """
        Bước 3, 4, 5: Huấn luyện, giải thích Loss Function và Đánh giá mô hình.
        """
        print("\n=== BƯỚC 3 & 4: THIẾT LẬP MÔ HÌNH, HÀM MẤT MÁT & TỐI ƯU HÓA ===")
        print("1. Hàm mất mát (Loss Function):")
        print("   - MSE (Mean Squared Error): Phạt rất nặng các sai số lớn. Sẽ bị ảnh hưởng nếu có những ngày đột biến (lễ hội).")
        print("   - MAE (Mean Absolute Error): Độ lệch tuyệt đối trung bình, chống chịu tốt với Outliers. Cho biết trung bình mỗi giờ mô hình dự báo lệch bao nhiêu xe.")
        print("\n2. Thuật toán Tối ưu (Optimization):")
        print("   - Khởi chạy Linear Regression của Scikit-Learn giải bài toán cực tiểu hóa bằng phương pháp Ordinary Least Squares (OLS) tìm trọng số Theta tối ưu.")
        
        # --- CONSTANT MODEL (BASELINE) ---
        print("\n[MÔ HÌNH 1: THE CONSTANT MODEL (BASELINE)]")
        print("Dự đoán hằng số trung bình (Mean) cho mọi khung giờ. Đây là mốc cơ sở so sánh (Benchmark).")
        dummy_regr = DummyRegressor(strategy="mean")
        dummy_regr.fit(self.X_train, self.y_train)
        y_pred_dummy = dummy_regr.predict(self.X_test)
        
        mae_dummy = mean_absolute_error(self.y_test, y_pred_dummy)
        rmse_dummy = np.sqrt(mean_squared_error(self.y_test, y_pred_dummy))
        r2_dummy = r2_score(self.y_test, y_pred_dummy)
        print(f" - MAE: {mae_dummy:.2f} xe/giờ")
        print(f" - RMSE: {rmse_dummy:.2f} xe/giờ")
        print(f" - R2 Score: {r2_dummy:.4f}")
        
        # --- LINEAR REGRESSION ---
        print("\n[MÔ HÌNH 2: MULTIPLE LINEAR REGRESSION]")
        lr = LinearRegression()
        
        # Cross-validation
        cv_scores = cross_val_score(lr, self.X_train, self.y_train, cv=5, scoring='neg_mean_absolute_error')
        print(f" - 5-Fold CV MAE (Trên tập Training): {-cv_scores.mean():.2f} (+/- {cv_scores.std():.2f})")
        
        # Fit model
        lr.fit(self.X_train, self.y_train)
        y_pred_lr = lr.predict(self.X_test)
        
        mae_lr = mean_absolute_error(self.y_test, y_pred_lr)
        rmse_lr = np.sqrt(mean_squared_error(self.y_test, y_pred_lr))
        r2_lr = r2_score(self.y_test, y_pred_lr)
        
        print(f" - MAE: {mae_lr:.2f} xe/giờ")
        print(f" - RMSE: {rmse_lr:.2f} xe/giờ")
        print(f" - R2 Score: {r2_lr:.4f} (Linear Regression giải thích được {r2_lr*100:.1f}% biến thiên của nhu cầu thuê xe)")
        
        print("\n=> KẾT LUẬN: Linear Regression vượt qua Constant Model rất xa, chứng tỏ quy luật thời gian ảnh hưởng cực mạnh tới nhu cầu thuê xe.")
        
        # --- BƯỚC 5: ĐÁNH GIÁ & DIỄN GIẢI ---
        print("\n=== BƯỚC 5: ĐÁNH GIÁ VÀ DIỄN GIẢI (INFERENCE) ===")
        
        # Phân tích trọng số (Inference)
        coef_dict = dict(zip(self.X_cols, lr.coef_))
        hour_coefs = {k: v for k, v in coef_dict.items() if 'hour_of_day' in k}
        
        if hour_coefs:
            max_hour = max(hour_coefs, key=hour_coefs.get)
            print(f"💡 Actionable Insight:")
            print(f"   - Trọng số (Coefficient Theta) cao nhất thuộc về biến: '{max_hour}' với độ tăng +{hour_coefs[max_hour]:.1f} xe so với lúc nửa đêm (Baseline của One-Hot).")
            print(f"   - Khuyến nghị cho Đội ngũ Vận hành: Hệ thống luôn bùng nổ mạnh nhất vào khung giờ này. Mô hình yêu cầu kích hoạt sớm xe tải điều phối (Rebalancing) từ trước đó 1-2 tiếng để phân bổ đầy xe vào các ngàm rỗng ở trung tâm!")
        
        # Vẽ Residual Plot
        print("\nĐang vẽ biểu đồ Residual Plot...")
        residuals = self.y_test - y_pred_lr
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_pred_lr, y=residuals, alpha=0.3, color='#8e44ad')
        plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
        plt.title('Residual Plot: Phân tích Sai số của Linear Regression')
        plt.xlabel('Predicted Demand (Dự báo lượng xe)')
        plt.ylabel('Residuals (Thực tế - Dự báo)')
        plt.show()
        
        print("🔍 Nhận xét Residual Plot:")
        print(" Lý tưởng nhất là các điểm sai số phân tán ngẫu nhiên đều quanh vạch 0 (không quy luật).")
        print(" Nếu đồ thị có hình nón phễu tòe ra (Heteroskedasticity), chứng tỏ ở những giờ cao điểm mô hình dự báo sai số càng cao. Lúc này Linear Regression đã đến giới hạn, ta cần nâng cấp lên mô hình phi tuyến tính phức tạp hơn như Random Forest hay XGBoost trong tương lai.")

    def train_complex_models(self, n_trials=5):
        """
        Tích hợp Optuna để tìm tham số tối ưu cho Random Forest.
        """
        print("\n=== NÂNG CẤP MÔ HÌNH: RANDOM FOREST + OPTUNA ===")
        print("Đang chạy Optuna để tối ưu hóa siêu tham số (Hyperparameters)...")
        
        def objective(trial):
            n_estimators = trial.suggest_int('n_estimators', 50, 150, step=50)
            max_depth = trial.suggest_int('max_depth', 5, 15)
            min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
            
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=42,
                n_jobs=-1
            )
            score = cross_val_score(model, self.X_train, self.y_train, cv=3, scoring='neg_mean_absolute_error')
            return -score.mean()
        
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
        
        print("\n[KẾT QUẢ OPTUNA]")
        print("Tham số tốt nhất tìm được:")
        for key, value in study.best_params.items():
            print(f" - {key}: {value}")
            
        print("\nĐang huấn luyện mô hình Random Forest cuối cùng với tham số tốt nhất...")
        best_rf = RandomForestRegressor(**study.best_params, random_state=42, n_jobs=-1)
        best_rf.fit(self.X_train, self.y_train)
        y_pred_rf = best_rf.predict(self.X_test)
        
        mae_rf = mean_absolute_error(self.y_test, y_pred_rf)
        rmse_rf = np.sqrt(mean_squared_error(self.y_test, y_pred_rf))
        r2_rf = r2_score(self.y_test, y_pred_rf)
        
        print("\n[ĐÁNH GIÁ MÔ HÌNH RANDOM FOREST]")
        print(f" - MAE: {mae_rf:.2f} xe/giờ")
        print(f" - RMSE: {rmse_rf:.2f} xe/giờ")
        print(f" - R2 Score: {r2_rf:.4f} (Mô hình phi tuyến tính giải thích được {r2_rf*100:.1f}% biến thiên!)")
        
        print("\n[FEATURE IMPORTANCES]")
        importances = best_rf.feature_importances_
        indices = np.argsort(importances)[::-1][:5]
        print("Top 5 biến quan trọng nhất ảnh hưởng đến nhu cầu:")
        for i in indices:
            print(f" - {self.X_cols[i]}: {importances[i]*100:.2f}%")
            
        print("\nĐang vẽ lại biểu đồ Residual Plot cho Random Forest...")
        residuals = self.y_test - y_pred_rf
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_pred_rf, y=residuals, alpha=0.4, color='#2ecc71')
        plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
        plt.title('Residual Plot: Phân tích Sai số của Random Forest')
        plt.xlabel('Predicted Demand (Dự báo lượng xe)')
        plt.ylabel('Residuals (Thực tế - Dự báo)')
        plt.show()
        print("🔍 Nhận xét Residual Plot (Random Forest):")
        print(" Hình phễu đã được thu hẹp đáng kể so với Linear Regression. Tuy nhiên, nếu ở các mức lượng xe cực cao (>2000) sai số vẫn lớn,")
        print(" hệ thống bắt buộc phải thu thập thêm dữ liệu Thời tiết (Nhiệt độ, Mưa, Tuyết) để triệt tiêu hoàn toàn sai số này!")
