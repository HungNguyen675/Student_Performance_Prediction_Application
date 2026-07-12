import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Cấu hình font chữ và giao diện để hiển thị đẹp
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 300

# Đọc dữ liệu
try:
    df = pd.read_csv('student_data.csv')
    df['Average_Score'] = (df['G1'] + df['G2'] + df['G3']) / 3
except Exception as e:
    print("Error reading file:", e)
    exit()

print("Generating charts...")

# 1. Phân phối điểm số (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(df['Average_Score'], bins=20, kde=True, color='teal')
plt.title('Phân phối Điểm Trung Bình Cả Năm (Average_Score)', fontsize=16, pad=15)
plt.xlabel('Điểm Trung Bình (Thang 10)', fontsize=14)
plt.ylabel('Số lượng học sinh', fontsize=14)
plt.savefig('score_distribution.png', bbox_inches='tight')
print("Created score_distribution.png")
plt.close()

# 2. Phân tích tương quan Pearson (Heatmap)
numeric_features = ['G1', 'G2', 'studytime', 'failures', 'absences', 'freetime', 'goout', 'Average_Score']
corr_matrix = df[numeric_features].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, 
            annot_kws={"size": 12})
plt.title('Ma trận tương quan Pearson giữa các đặc trưng số', fontsize=18, pad=15)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.savefig('correlation_heatmap.png', bbox_inches='tight')
print("Created correlation_heatmap.png")
plt.close()

# 3. Đánh giá định lượng hiệu năng mô hình (Actual vs Predicted)
try:
    model = joblib.load('ensemble_model.pkl')
    selected_features = [
        'G1', 'G2', 'studytime', 'failures', 'absences', 'schoolsup', 'famsup', 
        'paid', 'higher', 'internet', 'freetime', 'goout'
    ]
    X = df[selected_features]
    y = df['Average_Score']
    
    y_pred = model.predict(X)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(y, y_pred, alpha=0.6, color='indigo', s=50)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='Perfect Prediction') # Đường chéo y=x
    plt.title('Đánh giá Mô hình: Điểm Thực tế vs Dự đoán', fontsize=16, pad=15)
    plt.xlabel('Điểm Thực tế (Actual Average Score)', fontsize=14)
    plt.ylabel('Điểm Dự đoán (Predicted Average Score)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('actual_vs_predicted.png', bbox_inches='tight')
    print("Created actual_vs_predicted.png")
    plt.close()
except Exception as e:
    print("Error loading model:", e)

print("DONE!")
