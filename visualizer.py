"""
Trực quan hóa đồ thị và kết quả tìm đường đi
Sử dụng networkx và matplotlib
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional


def visualize_graph_with_path(graph: Dict[int, List[Tuple[int, float]]], 
                               positions: Dict[int, Tuple[float, float]],
                               path: Optional[List[int]],
                               start: int,
                               goal: int,
                               title: str,
                               filename: str = None):
    """
    Vẽ đồ thị và đường đi tìm được
    
    Args:
        graph: Đồ thị dạng adjacency list
        positions: Tọa độ của các nodes
        path: Đường đi tìm được (None nếu không tìm thấy)
        start: Node bắt đầu
        goal: Node đích
        title: Tiêu đề đồ thị
        filename: Tên file để lưu (không lưu nếu None)
    """
    # Tạo đồ thị networkx
    G = nx.Graph()
    
    # Thêm các edges
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            if node < neighbor:  # Tránh thêm cạnh trùng lặp
                G.add_edge(node, neighbor, weight=weight)
    
    plt.figure(figsize=(12, 8))
    
    # Vẽ tất cả các edges
    nx.draw_networkx_edges(G, positions, alpha=0.3, width=1)
    
    # Highlight đường đi nếu tìm thấy
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, positions, edgelist=path_edges, 
                               edge_color='red', width=3, alpha=0.8)
    
    # Vẽ nodes
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append('green')
        elif node == goal:
            node_colors.append('red')
        elif path and node in path:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')
    
    nx.draw_networkx_nodes(G, positions, node_color=node_colors, 
                          node_size=300, alpha=0.9)
    
    # Vẽ labels
    nx.draw_networkx_labels(G, positions, font_size=8)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Đã lưu hình ảnh: {filename}")
    
    plt.close()


def plot_comparison(results: Dict[str, Dict[str, any]], 
                   test_case_name: str,
                   filename: str = None):
    """
    Vẽ biểu đồ so sánh số nodes đã duyệt và thời gian thực thi
    
    Args:
        results: Dict chứa kết quả của các thuật toán
                 Format: {'BFS': {'nodes_explored': X, 'time': Y}, ...}
        test_case_name: Tên test case
        filename: Tên file để lưu
    """
    algorithms = list(results.keys())
    nodes_explored = [results[alg]['nodes_explored'] for alg in algorithms]
    times = [results[alg]['time'] * 1000 for alg in algorithms]  # Chuyển sang ms
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Biểu đồ số nodes đã duyệt
    bars1 = ax1.bar(algorithms, nodes_explored, color=['blue', 'orange', 'green'], alpha=0.7)
    ax1.set_ylabel('Số nodes đã duyệt', fontsize=11)
    ax1.set_title('So sánh số nodes đã duyệt', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Thêm giá trị lên các cột
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    # Biểu đồ thời gian thực thi
    bars2 = ax2.bar(algorithms, times, color=['blue', 'orange', 'green'], alpha=0.7)
    ax2.set_ylabel('Thời gian (ms)', fontsize=11)
    ax2.set_title('So sánh thời gian thực thi', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Thêm giá trị lên các cột
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10)
    
    fig.suptitle(f'Kết quả so sánh - {test_case_name}', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Đã lưu biểu đồ so sánh: {filename}")
    
    plt.close()


def visualize_all_paths(graph: Dict[int, List[Tuple[int, float]]], 
                        positions: Dict[int, Tuple[float, float]],
                        paths: Dict[str, Optional[List[int]]],
                        start: int,
                        goal: int,
                        test_case_name: str,
                        filename: str = None):
    """
    Vẽ tất cả các đường đi của 3 thuật toán cạnh nhau
    
    Args:
        graph: Đồ thị
        positions: Tọa độ nodes
        paths: Dict chứa đường đi của các thuật toán
               Format: {'BFS': path, 'Dijkstra': path, 'A*': path}
        start: Node bắt đầu
        goal: Node đích
        test_case_name: Tên test case
        filename: Tên file để lưu
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    algorithms = ['BFS', 'Dijkstra', 'A*']
    colors = ['blue', 'orange', 'green']
    
    for idx, (alg, color) in enumerate(zip(algorithms, colors)):
        ax = axes[idx]
        
        # Tạo đồ thị networkx
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors:
                if node < neighbor:
                    G.add_edge(node, neighbor, weight=weight)
        
        # Vẽ edges
        nx.draw_networkx_edges(G, positions, alpha=0.2, width=1, ax=ax)
        
        # Highlight đường đi
        path = paths.get(alg)
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, positions, edgelist=path_edges, 
                                   edge_color=color, width=3, alpha=0.8, ax=ax)
        
        # Vẽ nodes
        node_colors = []
        for node in G.nodes():
            if node == start:
                node_colors.append('green')
            elif node == goal:
                node_colors.append('red')
            elif path and node in path:
                node_colors.append(color)
            else:
                node_colors.append('lightgray')
        
        nx.draw_networkx_nodes(G, positions, node_color=node_colors, 
                              node_size=200, alpha=0.8, ax=ax)
        
        # Labels cho đồ thị nhỏ
        if len(G.nodes()) <= 20:
            nx.draw_networkx_labels(G, positions, font_size=7, ax=ax)
        
        ax.set_title(f'{alg}', fontsize=12, fontweight='bold')
        ax.axis('off')
    
    fig.suptitle(f'So sánh đường đi - {test_case_name}', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Đã lưu so sánh đường đi: {filename}")
    
    plt.close()
