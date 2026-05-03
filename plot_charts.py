import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("📊 Đang phân tích và vẽ biểu đồ...")

# 1. Tải dữ liệu (sửa lại tên file nếu cần)
df = pd.read_csv("student_data.csv")

# 2. VIỆT HÓA - ĐỔI SANG THANG ĐIỂM 10
df['Diem_Giua_Ky'] = df['G1'] / 2.0
df['Diem_Thi_Thu'] = df['G2'] / 2.0
df['Diem_Cuoi_Ky'] = df['G3'] / 2.0
df['Thoi_Gian_Hoc'] = df['studytime']
df['So_Ngay_Nghi'] = df['absences']
df = df[df['Diem_Cuoi_Ky'] > 0]

# 3. CHUẨN BỊ GIAO DIỆN VẼ BIỂU ĐỒ (2 hàng x 2 cột)
sns.set_theme(style="whitegrid") # Giao diện xịn sò
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("PHÂN TÍCH CÁC YẾU TỐ ẢNH HƯỞNG ĐẾN ĐIỂM TOÁN CUỐI KỲ", fontsize=16, fontweight='bold')

# Biểu đồ 1: Thời gian học vs Điểm cuối kỳ
sns.regplot(ax=axes[0, 0], x='Thoi_Gian_Hoc', y='Diem_Cuoi_Ky', data=df, 
            scatter_kws={'alpha':0.5, 'color':'blue'}, line_kws={'color':'red'})
axes[0, 0].set_title('Thời Gian Tự Học vs Điểm Cuối Kỳ')
axes[0, 0].set_xlabel('Thời gian học (Mức độ)')
axes[0, 0].set_ylabel('Điểm Cuối Kỳ (Thang 10)')

# Biểu đồ 2: Số ngày nghỉ vs Điểm cuối kỳ
sns.regplot(ax=axes[0, 1], x='So_Ngay_Nghi', y='Diem_Cuoi_Ky', data=df, 
            scatter_kws={'alpha':0.5, 'color':'orange'}, line_kws={'color':'red'})
axes[0, 1].set_title('Số Buổi Nghỉ Học vs Điểm Cuối Kỳ')
axes[0, 1].set_xlabel('Số buổi nghỉ')
axes[0, 1].set_ylabel('Điểm Cuối Kỳ (Thang 10)')

# Biểu đồ 3: Điểm Giữa Kỳ vs Điểm cuối kỳ
sns.regplot(ax=axes[1, 0], x='Diem_Giua_Ky', y='Diem_Cuoi_Ky', data=df, 
            scatter_kws={'alpha':0.5, 'color':'green'}, line_kws={'color':'red'})
axes[1, 0].set_title('Điểm Giữa Kỳ vs Điểm Cuối Kỳ')
axes[1, 0].set_xlabel('Điểm Giữa Kỳ (Thang 10)')
axes[1, 0].set_ylabel('Điểm Cuối Kỳ (Thang 10)')

# Biểu đồ 4: Điểm Thi Thử vs Điểm cuối kỳ
sns.regplot(ax=axes[1, 1], x='Diem_Thi_Thu', y='Diem_Cuoi_Ky', data=df, 
            scatter_kws={'alpha':0.5, 'color':'purple'}, line_kws={'color':'red'})
axes[1, 1].set_title('Điểm Thi Thử vs Điểm Cuối Kỳ')
axes[1, 1].set_xlabel('Điểm Thi Thử (Thang 10)')
axes[1, 1].set_ylabel('Điểm Cuối Kỳ (Thang 10)')

# Hiển thị
plt.tight_layout()
plt.show()

print("✅ Đã vẽ xong! Hãy chụp ảnh màn hình các biểu đồ này để đưa vào báo cáo Word nhé.")
