#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weighted_graph import WeightedGraph
from algorithms.dijkstra import dijkstra

def test_dijkstra_basic():
    print("=== Testing Dijkstra's Algorithm ===\n")
    
    # Create the example from theory walkthrough
    graph = WeightedGraph()
    graph.add_node("A")
    graph.add_node("B") 
    graph.add_node("C")
    graph.add_node("D")
    
    # Add weighted edges (using directed for this example)
    graph.add_directed_edge("A", "B", 4.0)
    graph.add_directed_edge("A", "C", 2.0)
    graph.add_directed_edge("C", "D", 5.0)
    graph.add_directed_edge("B", "D", 1.0)
    
    print("Graph structure:")
    print("A --(4)-> B")
    print("|         |")
    print("(2)      (1)")
    print("|         |")
    print("v         v")
    print("C --(5)-> D")
    
    # Test from source A
    result = dijkstra(graph, "A")
    
    print(f"\nShortest distances from A:")
    for dist_info in result:
        print(f"  A -> {dist_info.node}: {dist_info.distance}")
    
    # Expected: A->A: 0, A->B: 4, A->C: 2, A->D: 5 (via A->B->D)

def test_dijkstra_complex():
    print("\n=== Testing Complex Graph ===")
    
    graph = WeightedGraph()
    nodes = ["S", "A", "B", "C", "D", "T"]
    for node in nodes:
        graph.add_node(node)
    
    # Create a more complex graph
    edges = [
        ("S", "A", 7), ("S", "B", 2), ("S", "C", 3),
        ("A", "B", 3), ("A", "D", 4),
        ("B", "D", 4), ("B", "T", 1),
        ("C", "A", 2), ("C", "T", 5),
        ("D", "T", 1)
    ]
    
    for from_node, to_node, weight in edges:
        graph.add_directed_edge(from_node, to_node, weight)
    
    result = dijkstra(graph, "S")
    
    print("Shortest distances from S:")
    for dist_info in sorted(result, key=lambda x: x.distance):
        print(f"  S -> {dist_info.node}: {dist_info.distance}")

def test_error_cases():
    print("\n=== Testing Error Cases ===")
    
    graph = WeightedGraph()
    graph.add_node("A")
    
    # Test invalid source
    result = dijkstra(graph, "X")
    print(f"Invalid source result: {len(result)} nodes")
    
    # Test disconnected graph
    graph.add_node("B")  # B is disconnected from A
    result = dijkstra(graph, "A")
    print("Disconnected graph distances:")
    for dist_info in result:
        print(f"  A -> {dist_info.node}: {dist_info.distance}")

if __name__ == "__main__":
    test_dijkstra_basic()
    test_dijkstra_complex()
    test_error_cases()
    print("\n✅ All tests completed!")
