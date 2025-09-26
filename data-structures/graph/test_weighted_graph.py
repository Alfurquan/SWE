#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weighted_graph import WeightedGraph
from graph import WeightedEdge

def test_weighted_graph():
    print("=== Testing Weighted Graph Implementation ===\n")
    
    # Create a simple weighted graph
    graph = WeightedGraph()
    
    # Add nodes
    graph.add_node("A")
    graph.add_node("B") 
    graph.add_node("C")
    graph.add_node("D")
    
    # Add undirected weighted edges
    graph.add_undirected_edge("A", "B", 5.0)
    graph.add_undirected_edge("B", "C", 3.0)
    graph.add_undirected_edge("A", "C", 10.0)
    
    # Add directed weighted edge
    graph.add_directed_edge("C", "D", 2.0)
    
    print("Graph structure:")
    for node in graph.get_nodes():
        print(f"Node {node.label}:")
        for edge in node.get_edges():
            if isinstance(edge, WeightedEdge):
                print(f"  -> {edge.to_node.label} (weight: {edge.weight})")
            else:
                print(f"  -> {edge.to_node.label} (unweighted)")
    
    print("\n=== Testing Edge Cases ===")
    
    # Test invalid nodes
    graph.add_undirected_edge("A", "X", 1.0)  # Should print error
    graph.add_directed_edge("Y", "A", 1.0)    # Should print error
    
    print("\n=== Testing Default Weights ===")
    graph.add_node("E")
    graph.add_undirected_edge("D", "E")  # Should use default weight 1.0
    
    print("Node D connections:")
    d_node = graph.get_node_by_label("D")
    for edge in d_node.get_edges():
        if isinstance(edge, WeightedEdge):
            print(f"  -> {edge.to_node.label} (weight: {edge.weight})")

def test_directed_vs_undirected():
    print("\n=== Testing Directed vs Undirected Edges ===")
    
    graph = WeightedGraph()
    graph.add_node("X")
    graph.add_node("Y")
    graph.add_node("Z")
    
    # Undirected edge (both directions)
    graph.add_undirected_edge("X", "Y", 7.0)
    
    # Directed edge (one direction only)
    graph.add_directed_edge("Y", "Z", 4.0)
    
    print("Undirected edge X<->Y:")
    x_node = graph.get_node_by_label("X")
    y_node = graph.get_node_by_label("Y")
    
    print(f"X's edges: {len(x_node.get_edges())}")
    print(f"Y's edges: {len(y_node.get_edges())}")
    
    print("\nDirected edge Y->Z:")
    z_node = graph.get_node_by_label("Z")
    print(f"Y can reach Z: {any(edge.to_node.label == 'Z' for edge in y_node.get_edges())}")
    print(f"Z can reach Y: {any(edge.to_node.label == 'Y' for edge in z_node.get_edges())}")

if __name__ == "__main__":
    test_weighted_graph()
    test_directed_vs_undirected()
    print("\n✅ All tests completed!")
