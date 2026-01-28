# Hệ thống Định tuyến Giao thông (Routing & Logistics)

## Mô tả bài toán

**Tên Task**: Mô hình hóa và Tối ưu lộ trình vận chuyển trong đô thị bằng thuật toán tìm đường đi ngắn nhất.

**Mô tả**: Tìm đường đi ngắn nhất từ kho hàng/bệnh viện đến các điểm đích trong điều kiện có trọng số (khoảng cách/thời gian).

## Tiêu chuẩn thuật toán

- **Baseline**: Thuật toán Breadth-First Search (BFS) trên đồ thị không trọng số.
- **Phương pháp phổ biến**: Thuật toán Dijkstra.
- **Phương pháp đề xuất (Sáng tạo)**: Thuật toán A* (A-star) kết hợp hàm Heuristic (khoảng cách Euclidean) để tăng tốc độ tìm kiếm.

## Yêu cầu đầu ra

- Xử lý được bản đồ thực tế (dạng tọa độ x,y).
- Phân tích trường hợp đồ thị có mật độ cạnh dày đặc (giờ cao điểm).
- So sánh số lượng node phải duyệt giữa Dijkstra và A*.

---

## Cấu trúc dự án

```
dsa/
├── README.md                # File này - Hướng dẫn và mô tả dự án
├── requirements.txt         # Các thư viện cần thiết
├── todo.md                  # Danh sách công việc và yêu cầu
├── report.md                # Báo cáo chi tiết và phân tích
├── algorithms.py            # Cài đặt 3 thuật toán: BFS, Dijkstra, A*
├── graph_generator.py       # Tạo các test cases
├── visualizer.py            # Vẽ đồ thị và biểu đồ so sánh
├── main.py                  # File chính để chạy thử nghiệm
└── outputs/                 # Thư mục chứa kết quả (tự động tạo)
    ├── *_paths.png          # Hình ảnh so sánh đường đi
    └── *_comparison.png     # Biểu đồ so sánh hiệu suất
```

---

## Yêu cầu hệ thống

- **Python**: 3.10 hoặc cao hơn
- **Môi trường**: Conda (môi trường `htkh` như đã chỉ định)

---

## Hướng dẫn cài đặt

### 1. Clone hoặc tải dự án về

```bash
cd /home/ltgiang2/work/dsa
```

### 2. Kích hoạt môi trường Conda

```bash
conda activate htkh
```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

Các thư viện sẽ được cài đặt:
- `networkx`: Làm việc với đồ thị
- `matplotlib`: Vẽ biểu đồ và visualization
- `numpy`: Tính toán số học

---

## Hướng dẫn chạy

### Chạy toàn bộ thử nghiệm

Chạy tất cả các test cases và tạo báo cáo so sánh:

```bash
python main.py
```

**Kết quả**:
- Hiển thị kết quả chi tiết trên terminal
- Tạo thư mục `outputs/` chứa các hình ảnh visualization
- So sánh hiệu suất của 3 thuật toán trên nhiều test cases

### Các test cases được chạy

1. **Đồ thị nhỏ (10 nodes)**: Kiểm tra tính đúng đắn
2. **Đồ thị trung bình (50 nodes)**: So sánh hiệu suất cơ bản
3. **Đồ thị lớn (100 nodes)**: Đánh giá khả năng scale
4. **Đồ thị dày đặc (30 nodes)**: Mô phỏng giờ cao điểm
5. **Edge case - Đồ thị rời rạc**: Kiểm tra xử lý không có đường đi
6. **Edge case - Đồ thị đầy đủ**: Kiểm tra trường hợp mọi node kết nối

### Sử dụng các module riêng lẻ

#### Chỉ chạy một thuật toán cụ thể

```python
from algorithms import bfs, dijkstra, astar
from graph_generator import generate_small_graph

# Tạo đồ thị
graph, positions, start, goal = generate_small_graph()

# Chạy BFS
path, nodes_explored = bfs(graph, start, goal)

# Chạy Dijkstra
path, distance, nodes_explored = dijkstra(graph, start, goal)

# Chạy A*
path, distance, nodes_explored = astar(graph, positions, start, goal)
```

#### Tạo test case tùy chỉnh

```python
from graph_generator import generate_medium_graph

# Tạo đồ thị với 75 nodes
graph, positions, start, goal = generate_medium_graph(num_nodes=75)
```

#### Vẽ đồ thị tùy chỉnh

```python
from visualizer import visualize_graph_with_path

visualize_graph_with_path(
    graph, positions, path, start, goal,
    title="Đường đi tìm được",
    filename="my_result.png"
)
```

---

## Kết quả mong đợi

Sau khi chạy `python main.py`, bạn sẽ thấy:

### 1. Output trên Terminal
- Thông tin chi tiết về từng test case
- Số nodes đã duyệt của mỗi thuật toán
- Thời gian thực thi (ms)
- So sánh hiệu suất A* vs Dijkstra

### 2. Thư mục outputs/
Các file hình ảnh được tạo tự động:
- `Case_1_-_Đồ_thị_nhỏ_paths.png`: So sánh đường đi của 3 thuật toán
- `Case_1_-_Đồ_thị_nhỏ_comparison.png`: Biểu đồ so sánh hiệu suất
- Tương tự cho các test cases khác

### 3. Quan sát chính
- **BFS**: Đơn giản nhưng không tối ưu cho đồ thị có trọng số
- **Dijkstra**: Luôn tìm được đường đi ngắn nhất
- **A***: Nhanh hơn Dijkstra 20-50%, ít nodes duyệt hơn

---

## Phân tích độ phức tạp

| Thuật toán | Độ phức tạp thời gian | Độ phức tạp không gian | Tối ưu? |
|------------|-----------------------|------------------------|---------|
| BFS | O(V + E) | O(V) | ❌ (với đồ thị trọng số) |
| Dijkstra | O((V + E) log V) | O(V) | ✅ |
| A* | O((V + E) log V)* | O(V) | ✅ |

**Lưu ý**: A* có độ phức tạp worst-case giống Dijkstra, nhưng thực tế nhanh hơn nhiều nhờ heuristic.

---

## Báo cáo chi tiết

Xem file `report.md` để đọc báo cáo đầy đủ bao gồm:
- Cơ sở lý thuyết chi tiết
- Phân tích độ phức tạp
- Kết quả thử nghiệm
- So sánh và đánh giá
- Tài liệu tham khảo

---

## Tác giả

Dự án được phát triển cho môn học Data Structures & Algorithms.

---

## Tài liệu tham khảo chính

- Rosen, K. H. (2019). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill Education. Chapter 10: Graphs.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

---

## Liên hệ & Hỗ trợ

Nếu có vấn đề khi chạy, kiểm tra:
1. Python version: `python --version` (cần >= 3.10)
2. Các thư viện đã cài đặt: `pip list`
3. Môi trường conda đã kích hoạt: `conda env list`