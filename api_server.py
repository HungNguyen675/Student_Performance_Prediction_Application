import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===============================================
# QUAN TRỌNG: KHAI BÁO CLASS THUẬT TOÁN ĐỂ ĐỌC ĐƯỢC NÃO
# ===============================================
class SinhVienLinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = None 
        self.bias = None    
        self.loss_history = [] 
    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

# Tải NÃO BỘ lên bộ nhớ
with open('student_model.pkl', 'rb') as file:
    thung_hang = pickle.load(file)

my_model = thung_hang['model_loi']
x_mean = thung_hang['gia_tri_mean']
x_std = thung_hang['gia_tri_std']
ten_cac_cot = thung_hang['ten_cac_cot']

# ===============================================
# GIAO TIẾP VỚI JAVA SPRING BOOT
# ===============================================
@app.route('/api/predict_score', methods=['POST'])
def predict_score():
    try:
        data_tu_java = request.json
        print("📥 Mới nhận được thông tin từ trang Web Java:", data_tu_java)
        
        thoi_gian_hoc = float(data_tu_java.get('studytime', 2.0))
        diem_g1 = float(data_tu_java.get('G1', 10.0))
        diem_g2 = float(data_tu_java.get('G2', 10.0))
        
        student_data = np.copy(x_mean) 
        
        idx_studytime = ten_cac_cot.index('studytime')
        idx_g1 = ten_cac_cot.index('G1')
        idx_g2 = ten_cac_cot.index('G2')
        
        student_data[idx_studytime] = thoi_gian_hoc
        student_data[idx_g1] = diem_g1
        student_data[idx_g2] = diem_g2
        
        X_moi = np.array([student_data])
        X_moi_scaled = (X_moi - x_mean) / x_std 
        
        diem_du_doan = my_model.predict(X_moi_scaled)
        diem_chot = min(max(diem_du_doan[0], 0), 20)
        
        return jsonify({
            'status': 'Thành công',
            'estimated_score': round(diem_chot, 2),
            'message': 'Đã dùng lõi Gradient Descent để phân tích'
        })
        
    except Exception as e:
        return jsonify({'error_message': str(e)}), 400

if __name__ == '__main__':
    print("🚀 SERVER LÕI PYTHON AI ĐANG CHẠY CHÌM TẠI CỔNG 5000...")
    # Bật server chìm Python ở cổng 5000
    app.run(port=5000, debug=True, use_reloader=False)
