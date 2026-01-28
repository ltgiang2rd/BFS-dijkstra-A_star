Về quy chuẩn chung cho cả 3 bài toán:

- [ ] Tiêu chuẩn Code: 

        - Ngôn ngữ: Python 3.10+. (dùng môi trường conda htkh hiện tại)
        - Phải có file requirements.txt và README.md hướng dẫn chạy (hiện chỉ có mô tả bài toán).
        - Sử dụng time.time() để đo thời gian thực thi chính xác của mỗi thuật toán.

- [ ] Dữ liệu kiểm thử (Test Cases):
        - Case 1: Đồ thị nhỏ (5-10 đỉnh) để kiểm chứng tính đúng đắn.
        - Case 2: Đồ thị trung bình (50-100 đỉnh) để so sánh hiệu suất giữa các phương pháp.
        - Case 3 (Edge case): Đồ thị rời rạc hoặc đồ thị đầy đủ (Complete Graph).

- [ ] Báo cáo thành phần:

        - Phải có mục Phân tích độ phức tạp thời gian (O) cho mỗi thuật toán đã cài đặt.
        - Trực quan hóa kết quả bằng đồ thị (vẽ bằng networkx và matplotlib).
        - Tài liệu tham khảo: Yêu cầu trích dẫn ít nhất 1 nguồn từ sách Discrete Mathematics and Its Applications (Kenneth H. Rosen).