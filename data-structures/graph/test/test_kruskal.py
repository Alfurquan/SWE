#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weighted_graph import WeightedGraph
from algorithms.kruskal import kruskal

def test_kruskal():
    print("=== Testing Kruskal's Algorithm ===\n")
    
    # Create the example from theory walkthrough
    graph = WeightedGraph()
    graph.add_node("A")
    graph.add_node("B") 
    graph.add_node("C")
    graph.add_node("D")
    graph.add_node("E")
    graph.add_node("F")
    
    graph.add_edge("A", "B", 5.0)
    graph.add_edge("A", "C", 2.0)
    graph.add_edge("C", "D", 3.0)
    graph.add_edge("B", "D", 1.0)
    graph.add_edge("C", "E", 4.0)
    graph.add_edge("E", "F", 7.0)
    graph.add_edge("F", "D", 6.0)
    
    print("Graph structure:")
    print("A --(5)-> B")
    print("|         |")
    print("(2)      (1)")
    print("|         |")
    print("v         v")
    print("C --(3)-> D")
    print("|         |")
    print("(4)     (6)")
    print("|         |")
    print("v         v")
    print("E --(7)-> F")

    result = kruskal(graph)

    print(f"\nMinimum Spanning Tree (MST):")
    for edge in result:
        print(f"  {edge.from_node} --({edge.weight})-> {edge.to_node}")


if __name__ == "__main__":
    test_kruskal()
    print("\n✅ All tests completed!")
