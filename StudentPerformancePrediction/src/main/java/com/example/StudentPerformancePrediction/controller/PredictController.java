package com.example.StudentPerformancePrediction.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpEntity;
import org.springframework.http.MediaType;
import java.util.HashMap;
import java.util.Map;

@Controller
public class PredictController {

    // Nơi mở cửa dẫn ban giám khảo vào trang Web lúc bắt đầu
    @GetMapping("/")
    public String showForm() {
        return "index";
    }

    // Khi người dùng bấm nút Dự Đoán, luồng thông tin sẽ nhảy vào đây
    @PostMapping("/predict")
    public String predictScore(@RequestParam("studytime") double studytime,
                               @RequestParam("g1") double g1,
                               @RequestParam("g2") double g2,
                               Model model) {
        try {
            // URL của API Mạng Nơron Python (Cần đảm bảo file python api_server.py đang bật)
            String pythonApiUrl = "http://localhost:5000/api/predict_score";

            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // Đóng gói thông tin thành một bưu kiện JSON để Java ném sang góc sân Python
            Map<String, Object> map = new HashMap<>();
            map.put("studytime", studytime);
            map.put("G1", g1);
            map.put("G2", g2);

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(map, headers);

            // Bắn thông tin và Ép Python phải ngồi tính và nhả Điểm Số ra
            ResponseEntity<Map> response = restTemplate.postForEntity(pythonApiUrl, request, Map.class);
            Map<String, Object> responseBody = response.getBody();

            // Nhận kết quả và chuyển ra Mặt tiền Web báo cáo
            if (responseBody != null && responseBody.containsKey("estimated_score")) {
                model.addAttribute("score", responseBody.get("estimated_score"));
            } else {
                model.addAttribute("error", "Lỗi dữ liệu JSON trả về từ Python.");
            }
        } catch (Exception e) {
            model.addAttribute("error", "Đường dây với API Python bị đứt! (Quên bật Port 5000 do lỡ tay tắt VS Code chăng?)");
        }
        return "index";
    }
}
