"""
File chính để chạy thử nghiệm và so sánh các thuật toán
BFS, Dijkstra, A* trên các test cases khác nhau
"""

import time
import os
from typing import Dict, List, Tuple, Optional

from algorithms import bfs, dijkstra, astar
from graph_generator import (
    generate_small_graph,
    generate_medium_graph,
    generate_dense_graph,
    generate_disconnected_graph,
    generate_complete_graph
)
from visualizer import (
    visualize_graph_with_path,
    plot_comparison,
    visualize_all_paths
)


def run_algorithm(algorithm_name: str,
                 graph: Dict[int, List[Tuple[int, float]]],
                 positions: Dict[int, Tuple[float, float]],
                 start: int,
                 goal: int) -> Dict:
    """
    Chạy một thuật toán và đo thời gian
    
    Returns:
        Dict chứa kết quả: path, distance, nodes_explored, time
    """
    start_time = time.time()
    
    if algorithm_name == "BFS":
        path, nodes_explored = bfs(graph, start, goal)
        distance = None  # BFS không tính khoảng cách
    elif algorithm_name == "Dijkstra":
        path, distance, nodes_explored = dijkstra(graph, start, goal)
    elif algorithm_name == "A*":
        path, distance, nodes_explored = astar(graph, positions, start, goal)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return {
        'path': path,
        'distance': distance,
        'nodes_explored': nodes_explored,
        'time': elapsed_time
    }


def print_results(algorithm_name: str, result: Dict, verbose: bool = True):
    """In kết quả của một thuật toán"""
    print(f"\n{'='*60}")
    print(f"Thuật toán: {algorithm_name}")
    print(f"{'='*60}")
    
    if result['path'] is None:
        print("❌ Không tìm thấy đường đi!")
    else:
        print(f"✓ Tìm thấy đường đi!")
        if verbose and len(result['path']) <= 20:
            print(f"  Đường đi: {' → '.join(map(str, result['path']))}")
        print(f"  Độ dài đường đi: {len(result['path'])} nodes")
        
        if result['distance'] is not None:
            print(f"  Khoảng cách: {result['distance']:.2f}")
    
    print(f"  Số nodes đã duyệt: {result['nodes_explored']}")
    print(f"  Thời gian thực thi: {result['time']*1000:.4f} ms")


def run_test_case(test_name: str,
                 graph: Dict[int, List[Tuple[int, float]]],
                 positions: Dict[int, Tuple[float, float]],
                 start: int,
                 goal: int,
                 output_dir: str = "outputs"):
    """
    Chạy tất cả các thuật toán trên một test case
    """
    print("\n" + "="*80)
    print(f"TEST CASE: {test_name}")
    print("="*80)
    print(f"Số nodes: {len(graph)}")
    print(f"Start: {start} → Goal: {goal}")
    
    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    # Chạy các thuật toán
    algorithms = ["BFS", "Dijkstra", "A*"]
    results = {}
    paths = {}
    
    for alg in algorithms:
        result = run_algorithm(alg, graph, positions, start, goal)
        results[alg] = result
        paths[alg] = result['path']
        print_results(alg, result, verbose=(len(graph) <= 20))
    
    # So sánh kết quả
    print(f"\n{'='*60}")
    print("SO SÁNH KẾT QUẢ")
    print(f"{'='*60}")
    
    # So sánh số nodes đã duyệt
    print("\nSố nodes đã duyệt:")
    for alg in algorithms:
        if results[alg]['path']:
            print(f"  {alg:12s}: {results[alg]['nodes_explored']:5d} nodes")
    
    # So sánh thời gian
    print("\nThời gian thực thi:")
    for alg in algorithms:
        if results[alg]['path']:
            print(f"  {alg:12s}: {results[alg]['time']*1000:8.4f} ms")
    
    # Tính hiệu suất A* so với Dijkstra
    if results['A*']['path'] and results['Dijkstra']['path']:
        improvement_nodes = (1 - results['A*']['nodes_explored'] / 
                           results['Dijkstra']['nodes_explored']) * 100
        improvement_time = (1 - results['A*']['time'] / 
                          results['Dijkstra']['time']) * 100
        
        print(f"\n📊 Hiệu suất A* so với Dijkstra:")
        print(f"  - Giảm {improvement_nodes:.1f}% số nodes đã duyệt")
        print(f"  - Giảm {improvement_time:.1f}% thời gian thực thi")
    
    # Visualization
    print(f"\n📊 Đang tạo visualization...")
    
    # Vẽ so sánh đường đi
    visualize_all_paths(
        graph, positions, paths, start, goal,
        test_name,
        filename=f"{output_dir}/{test_name.replace(' ', '_')}_paths.png"
    )
    
    # Vẽ biểu đồ so sánh (chỉ với các thuật toán tìm được đường đi)
    valid_results = {alg: res for alg, res in results.items() if res['path']}
    if valid_results:
        plot_comparison(
            valid_results,
            test_name,
            filename=f"{output_dir}/{test_name.replace(' ', '_')}_comparison.png"
        )
    
    return results


def main():
    """Chạy tất cả các test cases"""
    print("\n" + "🚀"*40)
    print("HỆ THỐNG ĐỊNH TUYẾN GIAO THÔNG")
    print("So sánh thuật toán: BFS vs Dijkstra vs A*")
    print("🚀"*40)
    
    # Test Case 1: Đồ thị nhỏ
    print("\n" + "📌"*40)
    print("CASE 1: Đồ thị nhỏ (10 nodes)")
    print("📌"*40)
    graph1, pos1, start1, goal1 = generate_small_graph()
    run_test_case("Case 1 - Đồ thị nhỏ", graph1, pos1, start1, goal1)
    
    # Test Case 2: Đồ thị trung bình
    print("\n" + "📌"*40)
    print("CASE 2: Đồ thị trung bình (50 nodes)")
    print("📌"*40)
    graph2, pos2, start2, goal2 = generate_medium_graph(50)
    run_test_case("Case 2 - Đồ thị trung bình (50 nodes)", graph2, pos2, start2, goal2)
    
    # Test Case 3: Đồ thị lớn hơn
    print("\n" + "📌"*40)
    print("CASE 3: Đồ thị lớn (100 nodes)")
    print("📌"*40)
    graph3, pos3, start3, goal3 = generate_medium_graph(100)
    run_test_case("Case 3 - Đồ thị lớn (100 nodes)", graph3, pos3, start3, goal3)
    
    # Test Case 4: Đồ thị dày đặc (giờ cao điểm)
    print("\n" + "📌"*40)
    print("CASE 4: Đồ thị dày đặc - Giờ cao điểm (30 nodes)")
    print("📌"*40)
    graph4, pos4, start4, goal4 = generate_dense_graph(30)
    run_test_case("Case 4 - Đồ thị dày đặc", graph4, pos4, start4, goal4)
    
    # Edge Case 1: Đồ thị rời rạc
    print("\n" + "📌"*40)
    print("EDGE CASE 1: Đồ thị rời rạc (không có đường đi)")
    print("📌"*40)
    graph5, pos5, start5, goal5 = generate_disconnected_graph()
    run_test_case("Edge Case - Đồ thị rời rạc", graph5, pos5, start5, goal5)
    
    # Edge Case 2: Đồ thị đầy đủ
    print("\n" + "📌"*40)
    print("EDGE CASE 2: Đồ thị đầy đủ (Complete Graph - 10 nodes)")
    print("📌"*40)
    graph6, pos6, start6, goal6 = generate_complete_graph(10)
    run_test_case("Edge Case - Đồ thị đầy đủ", graph6, pos6, start6, goal6)
    
    # Kết luận
    print("\n" + "="*80)
    print("✅ HOÀN THÀNH TẤT CẢ CÁC TEST CASES")
    print("="*80)
    print("\n📁 Kết quả đã được lưu vào thư mục 'outputs/'")
    print("   - Hình ảnh so sánh đường đi: *_paths.png")
    print("   - Biểu đồ so sánh hiệu suất: *_comparison.png")
    print("\n💡 Quan sát:")
    print("   - BFS: Đơn giản nhưng không tối ưu cho đồ thị có trọng số")
    print("   - Dijkstra: Tìm đường đi ngắn nhất chính xác")
    print("   - A*: Nhanh hơn Dijkstra nhờ heuristic, số nodes duyệt ít hơn")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
