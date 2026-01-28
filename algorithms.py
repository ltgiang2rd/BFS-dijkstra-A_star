"""
Các thuật toán tìm đường đi ngắn nhất
- BFS (Breadth-First Search): Baseline cho đồ thị không trọng số
- Dijkstra: Thuật toán phổ biến cho đồ thị có trọng số
- A* (A-star): Thuật toán tối ưu với heuristic
"""

import heapq
import math
from collections import deque
from typing import Dict, List, Tuple, Set, Optional


def euclidean_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Tính khoảng cách Euclidean giữa 2 điểm (heuristic cho A*)"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def bfs(graph: Dict[int, List[Tuple[int, float]]], 
        start: int, 
        goal: int) -> Tuple[Optional[List[int]], int]:
    """
    Thuật toán BFS (Breadth-First Search)
    
    Args:
        graph: Dict với key là node, value là list các (neighbor, weight)
        start: Node bắt đầu
        goal: Node đích
    
    Returns:
        (path, nodes_explored): Đường đi và số nodes đã duyệt
    """
    if start == goal:
        return [start], 1
    
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    nodes_explored = 0
    
    while queue:
        current = queue.popleft()
        nodes_explored += 1
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_explored
        
        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None, nodes_explored


def dijkstra(graph: Dict[int, List[Tuple[int, float]]], 
             start: int, 
             goal: int) -> Tuple[Optional[List[int]], float, int]:
    """
    Thuật toán Dijkstra
    
    Args:
        graph: Dict với key là node, value là list các (neighbor, weight)
        start: Node bắt đầu
        goal: Node đích
    
    Returns:
        (path, distance, nodes_explored): Đường đi, khoảng cách và số nodes đã duyệt
    """
    if start == goal:
        return [start], 0.0, 1
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    distances = {start: 0}
    parent = {start: None}
    visited = set()
    nodes_explored = 0
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        nodes_explored += 1
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], distances[goal], nodes_explored
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
            
            new_dist = current_dist + weight
            
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    return None, float('inf'), nodes_explored


def astar(graph: Dict[int, List[Tuple[int, float]]], 
          positions: Dict[int, Tuple[float, float]],
          start: int, 
          goal: int) -> Tuple[Optional[List[int]], float, int]:
    """
    Thuật toán A* (A-star) với heuristic Euclidean
    
    Args:
        graph: Dict với key là node, value là list các (neighbor, weight)
        positions: Dict với key là node, value là tọa độ (x, y)
        start: Node bắt đầu
        goal: Node đích
    
    Returns:
        (path, distance, nodes_explored): Đường đi, khoảng cách và số nodes đã duyệt
    """
    if start == goal:
        return [start], 0.0, 1
    
    # Priority queue: (f_score, g_score, node)
    # f_score = g_score + heuristic
    goal_pos = positions[goal]
    h_start = euclidean_distance(positions[start], goal_pos)
    
    pq = [(h_start, 0, start)]
    g_scores = {start: 0}
    parent = {start: None}
    visited = set()
    nodes_explored = 0
    
    while pq:
        f_score, g_score, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        nodes_explored += 1
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], g_scores[goal], nodes_explored
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
            
            new_g_score = g_score + weight
            
            if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                g_scores[neighbor] = new_g_score
                h_score = euclidean_distance(positions[neighbor], goal_pos)
                f_score = new_g_score + h_score
                parent[neighbor] = current
                heapq.heappush(pq, (f_score, new_g_score, neighbor))
    
    return None, float('inf'), nodes_explored
