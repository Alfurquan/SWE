from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
import heapq
from graph import Graph, Node

@dataclass
class ShortestDistance:
    node: str
    distance: float

def dijkstra(graph: Graph, source: str) -> List[ShortestDistance]:
    nodes = graph.get_nodes()
    
    source_node = graph.get_node_by_label(source)
    if source_node == None:
        print(f"Node with the label {source} does not exist in the graph")
        return []
    
    result: List[ShortestDistance] = []
    distance: Dict[Node, float] = {}
    for node in nodes:
        distance[node] = float('inf')
        
    distance[source_node] = 0
    queue: List[Tuple[float, Node]] = [(0, source_node)]
    visited: Set[Node] = set()
    
    while queue:
        dist, node = heapq.heappop(queue)
        
        if node in visited:
            continue
        
        visited.add(node)
            
        for edge in node.get_edges():
            to_node = edge.to_node
            if dist + edge.weight < distance[to_node]:
                distance[to_node] = dist + edge.weight
                heapq.heappush(queue, (dist + edge.weight, to_node))
                
    for node in nodes:
        if node == source_node:
            continue
        result.append(ShortestDistance(node.label, distance[node]))
    
    return result
        
        