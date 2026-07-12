import React, { useState } from 'react';
import axios from 'axios';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import './App.css';

const formFields = [
  { section: 'Hồ sơ Học sinh', fields: [
    { name: 'studentId', label: 'Mã định danh (Mã HS)', type: 'text' },
    { name: 'studentName', label: 'Họ và tên', type: 'text' }
  ]},
  { section: 'Điểm số & Học tập', fields: [
    { name: 'G1', label: 'Điểm Kỳ 1 (Thang 10)', type: 'number', min: 0, max: 10, step: 0.1 },
    { name: 'G2', label: 'Điểm Kỳ 2 (Thang 10)', type: 'number', min: 0, max: 10, step: 0.1 },
    { name: 'studytime', label: 'Thời gian tự học/tuần', type: 'select', options: [{val:1, lbl:'<2 giờ'}, {val:2, lbl:'2-5 giờ'}, {val:3, lbl:'5-10 giờ'}, {val:4, lbl:'>10 giờ'}] },
    { name: 'failures', label: 'Số môn từng rớt', type: 'number', min: 0, max: 4, step: 1 },
    { name: 'absences', label: 'Số ngày nghỉ học', type: 'number', min: 0, max: 93, step: 1 },
    { name: 'schoolsup', label: 'Hỗ trợ học tập từ trường', type: 'select', options: [{val:'yes', lbl:'Có'}, {val:'no', lbl:'Không'}] },
    { name: 'famsup', label: 'Hỗ trợ học tập từ gia đình', type: 'select', options: [{val:'yes', lbl:'Có'}, {val:'no', lbl:'Không'}] },
    { name: 'paid', label: 'Đi học thêm (có trả phí)', type: 'select', options: [{val:'yes', lbl:'Có'}, {val:'no', lbl:'Không'}] },
    { name: 'higher', label: 'Muốn học lên đại học', type: 'select', options: [{val:'yes', lbl:'Có'}, {val:'no', lbl:'Không'}] },
  ]},
  { section: 'Lối sống & Thói quen', fields: [
    { name: 'internet', label: 'Có Internet ở nhà', type: 'select', options: [{val:'yes', lbl:'Có'}, {val:'no', lbl:'Không'}] },
    { name: 'freetime', label: 'Thời gian rảnh rỗi', type: 'select', options: [{val:1, lbl:'Rất ít (1)'}, {val:2, lbl:'Ít (2)'}, {val:3, lbl:'Trung bình (3)'}, {val:4, lbl:'Nhiều (4)'}, {val:5, lbl:'Rất nhiều (5)'}] },
    { name: 'goout', label: 'Mức độ đi chơi', type: 'select', options: [{val:1, lbl:'Rất ít (1)'}, {val:2, lbl:'Ít (2)'}, {val:3, lbl:'Trung bình (3)'}, {val:4, lbl:'Nhiều (4)'}, {val:5, lbl:'Rất nhiều (5)'}] },
  ]}
];

function App() {
  const [formData, setFormData] = useState({
    studentId: '', studentName: '',
    G1: 7.5, G2: 8.0, studytime: 2, failures: 0, absences: 0, schoolsup: 'no', famsup: 'yes',
    paid: 'no', higher: 'yes', internet: 'yes', freetime: 3, goout: 3
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let parsedValue = value;
    if (type === 'number' || e.target.tagName.toLowerCase() === 'select') {
      if (!isNaN(value) && value !== '') {
        parsedValue = parseFloat(value);
      }
    }
    setFormData({ ...formData, [name]: parsedValue });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);
    try {
      const response = await axios.post('http://localhost:8000/predict', formData);
      setPrediction(response.data);
    } catch (err) {
      setError('Không thể kết nối đến AI Backend. Hãy chắc chắn Backend đang chạy trên cổng 8000.');
    } finally {
      setLoading(false);
    }
  };

  const getRadarData = () => {
    // Chuẩn hóa dữ liệu về thang 10
    const study = (formData.studytime / 4) * 10;
    const grades = (formData.G1 + formData.G2) / 2;
    const discipline = Math.max(10 - (formData.absences / 20) * 10, 0);
    const freetime = (formData.freetime / 5) * 10;
    const social = (formData.goout / 5) * 10;
    const family = formData.famsup === 'yes' ? 10 : 4;

    return [
      { subject: 'Điểm số', A: grades, fullMark: 10 },
      { subject: 'Học tập', A: study, fullMark: 10 },
      { subject: 'Kỷ luật', A: discipline, fullMark: 10 },
      { subject: 'Gia đình', A: family, fullMark: 10 },
      { subject: 'Giải trí', A: freetime, fullMark: 10 },
      { subject: 'Giao lưu', A: social, fullMark: 10 },
    ];
  };

  return (
    <div className="app-container">
      <div className="bg-shape shape-1"></div>
      <div className="bg-shape shape-2"></div>
      <div className="bg-shape shape-3"></div>

      <header className="header glass">
        <h1>Student Performance Predictor</h1>
        <p className="subtitle">Hệ thống AI dự đoán Điểm Trung Bình Cả Năm & Xếp loại Học tập</p>
        
        <div className="explanation-box">
          <strong>💡 Ứng dụng này dự đoán điều gì?</strong>
          <p>
            Mô hình Trí tuệ Nhân tạo (Ensemble Machine Learning) phân tích <b>Điểm Kỳ 1 (G1)</b>, <b>Điểm Kỳ 2 (G2)</b> kết hợp cùng <b>Thái độ học tập và Lối sống</b> hiện tại của học sinh. Từ đó, AI có khả năng "nhìn trước tương lai" và dự đoán chính xác <b>Điểm Tổng kết Trung Bình Cả Năm</b> mà học sinh đó sẽ đạt được, giúp nhà trường có biện pháp can thiệp sớm.
          </p>
        </div>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="prediction-form glass">
          <div className="form-sections">
            {formFields.map((section, idx) => (
              <div key={idx} className="form-section">
                <h2>{section.section}</h2>
                <div className="grid">
                  {section.fields.map((field) => (
                    <div key={field.name} className="input-group">
                      <label htmlFor={field.name}>{field.label}</label>
                      {field.type === 'select' ? (
                        <select
                          id={field.name}
                          name={field.name}
                          value={formData[field.name]}
                          onChange={handleChange}
                        >
                          {field.options.map(opt => (
                            <option key={opt.val} value={opt.val}>{opt.lbl}</option>
                          ))}
                        </select>
                      ) : (
                        <input
                          id={field.name}
                          name={field.name}
                          type={field.type}
                          min={field.min}
                          max={field.max}
                          step={field.step}
                          value={formData[field.name]}
                          onChange={handleChange}
                          required
                        />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="submit-container">
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? <span className="loader"></span> : 'Bắt đầu dự đoán'}
            </button>
          </div>
          {error && <div className="error-message">{error}</div>}
        </form>

        {prediction && (
          <div className="result-card glass fade-in">
            <h2>Kết quả Dự đoán từ AI</h2>
            {(formData.studentName || formData.studentId) && (
              <h3 style={{color: '#cbd5e1', marginBottom: '1.5rem', fontWeight: 500}}>
                Học sinh: <span style={{color: '#fff'}}>{formData.studentName}</span> {formData.studentId ? `(${formData.studentId})` : ''}
              </h3>
            )}
            
            <div className="dashboard-grid">
              <div className="main-result">
                <div className={`rank-badge rank-${prediction.prediction}`}>
                  {prediction.score} Điểm
                </div>
                <p className="result-desc">
                  Dựa trên dữ liệu cung cấp, Hệ thống AI dự đoán học sinh đạt mức <strong>{prediction.score}/10 điểm</strong> tương đương xếp loại <strong>{prediction.rank}</strong>.
                </p>
                <div className="accuracy-info">
                  🎯 Độ chính xác của mô hình (R² Score): <strong>96.79%</strong> | Sai số (RMSE): <strong>±0.34 điểm</strong>
                </div>
              </div>
              
              <div className="radar-chart-container">
                <h4 style={{color: '#cbd5e1', marginBottom: '1rem', fontWeight: 500}}>Biểu đồ Năng lực & Lối sống</h4>
                <ResponsiveContainer width="100%" height={260}>
                  <RadarChart cx="50%" cy="50%" outerRadius="65%" data={getRadarData()}>
                    <PolarGrid stroke="#475569" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#cbd5e1', fontSize: 13 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 10]} tick={false} axisLine={false} />
                    <Radar name="Học sinh" dataKey="A" stroke="#818cf8" fill="#818cf8" fillOpacity={0.6} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
