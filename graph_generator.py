"""
Tạo các test cases cho bài toán tìm đường đi ngắn nhất
- Case 1: Đồ thị nhỏ (5-10 nodes)
- Case 2: Đồ thị trung bình (50-100 nodes)
- Case 3: Edge cases (đồ thị rời rạc, đồ thị đầy đủ)
"""

import random
import math
from typing import Dict, List, Tuple


def generate_small_graph() -> Tuple[Dict[int, List[Tuple[int, float]]], 
                                     Dict[int, Tuple[float, float]], 
                                     int, int]:
    """
    Tạo đồ thị nhỏ (10 nodes) để kiểm tra tính đúng đắn
    
    Returns:
        (graph, positions, start, goal)
    """
    # Tạo tọa độ cho 10 nodes trong lưới 10x10
    positions = {
        0: (0, 0),
        1: (2, 1),
        2: (4, 0),
        3: (1, 3),
        4: (3, 3),
        5: (5, 2),
        6: (2, 5),
        7: (4, 5),
        8: (6, 4),
        9: (5, 6)
    }
    
    # Tạo cạnh với trọng số là khoảng cách Euclidean
    edges = [
        (0, 1), (0, 3),
        (1, 2), (1, 3), (1, 4),
        (2, 4), (2, 5),
        (3, 4), (3, 6),
        (4, 5), (4, 7),
        (5, 8),
        (6, 7),
        (7, 8), (7, 9),
        (8, 9)
    ]
    
    graph = {i: [] for i in range(10)}
    
    for u, v in edges:
        dist = math.sqrt((positions[u][0] - positions[v][0])**2 + 
                        (positions[u][1] - positions[v][1])**2)
        graph[u].append((v, dist))
        graph[v].append((u, dist))  # Đồ thị vô hướng
    
    return graph, positions, 0, 9  # Từ node 0 đến node 9


def generate_medium_graph(num_nodes: int = 50) -> Tuple[Dict[int, List[Tuple[int, float]]], 
                                                         Dict[int, Tuple[float, float]], 
                                                         int, int]:
    """
    Tạo đồ thị trung bình (50-100 nodes) để so sánh hiệu suất
    Mô phỏng mạng lưới đường phố với mật độ kết nối trung bình
    
    Args:
        num_nodes: Số lượng nodes (mặc định 50)
    
    Returns:
        (graph, positions, start, goal)
    """
    random.seed(42)  # Để kết quả có thể tái tạo
    
    # Tạo tọa độ ngẫu nhiên trong không gian 100x100
    positions = {
        i: (random.uniform(0, 100), random.uniform(0, 100))
        for i in range(num_nodes)
    }
    
    graph = {i: [] for i in range(num_nodes)}
    
    # Kết nối mỗi node với k nodes gần nhất (k = 5)
    k_nearest = 5
    
    for node in range(num_nodes):
        # Tính khoảng cách đến tất cả nodes khác
        distances = []
        for other in range(num_nodes):
            if other != node:
                dist = math.sqrt((positions[node][0] - positions[other][0])**2 + 
                               (positions[node][1] - positions[other][1])**2)
                distances.append((dist, other))
        
        # Sắp xếp và lấy k nodes gần nhất
        distances.sort()
        for dist, neighbor in distances[:k_nearest]:
            # Tránh thêm cạnh trùng lặp
            if neighbor not in [n for n, _ in graph[node]]:
                graph[node].append((neighbor, dist))
                graph[neighbor].append((node, dist))
    
    # Chọn start và goal ở 2 góc đối diện
    start = 0
    goal = num_nodes - 1
    
    return graph, positions, start, goal


def generate_dense_graph(num_nodes: int = 30) -> Tuple[Dict[int, List[Tuple[int, float]]], 
                                                        Dict[int, Tuple[float, float]], 
                                                        int, int]:
    """
    Tạo đồ thị dày đặc (mô phỏng giờ cao điểm với nhiều tuyến đường)
    Kết nối mỗi node với nhiều nodes khác
    
    Args:
        num_nodes: Số lượng nodes (mặc định 30)
    
    Returns:
        (graph, positions, start, goal)
    """
    random.seed(100)
    
    positions = {
        i: (random.uniform(0, 50), random.uniform(0, 50))
        for i in range(num_nodes)
    }
    
    graph = {i: [] for i in range(num_nodes)}
    
    # Kết nối với nhiều neighbors hơn (k = 10)
    k_nearest = 10
    
    for node in range(num_nodes):
        distances = []
        for other in range(num_nodes):
            if other != node:
                dist = math.sqrt((positions[node][0] - positions[other][0])**2 + 
                               (positions[node][1] - positions[other][1])**2)
                distances.append((dist, other))
        
        distances.sort()
        for dist, neighbor in distances[:k_nearest]:
            if neighbor not in [n for n, _ in graph[node]]:
                graph[node].append((neighbor, dist))
                graph[neighbor].append((node, dist))
    
    return graph, positions, 0, num_nodes - 1


def generate_disconnected_graph() -> Tuple[Dict[int, List[Tuple[int, float]]], 
                                           Dict[int, Tuple[float, float]], 
                                           int, int]:
    """
    Tạo đồ thị rời rạc (edge case) - start và goal không kết nối
    
    Returns:
        (graph, positions, start, goal)
    """
    positions = {
        0: (0, 0), 1: (2, 0), 2: (4, 0),  # Component 1
        3: (10, 0), 4: (12, 0), 5: (14, 0),  # Component 2 (rời rạc)
    }
    
    graph = {i: [] for i in range(6)}
    
    # Component 1: 0-1-2
    edges_1 = [(0, 1), (1, 2)]
    # Component 2: 3-4-5
    edges_2 = [(3, 4), (4, 5)]
    
    for u, v in edges_1 + edges_2:
        dist = math.sqrt((positions[u][0] - positions[v][0])**2 + 
                        (positions[u][1] - positions[v][1])**2)
        graph[u].append((v, dist))
        graph[v].append((u, dist))
    
    return graph, positions, 0, 5  # Không thể đi từ 0 đến 5


def generate_complete_graph(num_nodes: int = 10) -> Tuple[Dict[int, List[Tuple[int, float]]], 
                                                          Dict[int, Tuple[float, float]], 
                                                          int, int]:
    """
    Tạo đồ thị đầy đủ (edge case) - mọi node đều kết nối với nhau
    
    Args:
        num_nodes: Số lượng nodes (mặc định 10)
    
    Returns:
        (graph, positions, start, goal)
    """
    random.seed(200)
    
    positions = {
        i: (random.uniform(0, 20), random.uniform(0, 20))
        for i in range(num_nodes)
    }
    
    graph = {i: [] for i in range(num_nodes)}
    
    # Kết nối mọi cặp nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dist = math.sqrt((positions[i][0] - positions[j][0])**2 + 
                           (positions[i][1] - positions[j][1])**2)
            graph[i].append((j, dist))
            graph[j].append((i, dist))
    
    return graph, positions, 0, num_nodes - 1
