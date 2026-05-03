from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

print("🧠 Đang nạp Não AI...")
with open("math_ai_model.pkl", "rb") as f:
    model = pickle.load(f)
print("✅ Nạp Não AI thành công!")

# Route trang chủ: Xử lý cả việc hiển thị Web (GET) và Phân tích điểm (POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    score = None # Mặc định ban đầu chưa có điểm
    
    # Nếu người dùng bấm nút Submit
    if request.method == 'POST':
        try:
            # Lấy 4 thông số từ Giao diện HTML gửi về
            studytime = float(request.form['studytime'])
            absences = float(request.form['absences'])
            Diem_Kiem_Tra_1 = float(request.form['Diem_Kiem_Tra_1'])
            Diem_Kiem_Tra_2 = float(request.form['Diem_Kiem_Tra_2'])
            
            # Gói vào DataFrame
            input_data = pd.DataFrame([[studytime, absences, Diem_Kiem_Tra_1, Diem_Kiem_Tra_2]], 
                                      columns=['studytime', 'absences', 'Diem_Kiem_Tra_1', 'Diem_Kiem_Tra_2'])
            
            # Kêu AI dự đoán
            predicted_score = model.predict(input_data)[0]
            
            # Ép điểm không được lố quá 10 hoặc rớt dưới 0
            predicted_score = max(0.0, min(10.0, predicted_score))
            score = round(predicted_score, 2)
            
        except Exception as e:
            score = "Lỗi"
            
    # Trả giao diện HTML về kèm theo điểm số (nếu có)
    return render_template('index.html', score=score)

if __name__ == '__main__':
    print("🚀 Giao diện Web đang chạy tại: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
