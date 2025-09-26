from graph import Graph, Node
from typing import List, Dict, Deque
from collections import deque
from algorithms.node_state import NodeState

def bfs(graph: Graph, start_node_label) -> List[Node]:
    node_states: Dict[Node, NodeState] = {}
    nodes = graph.get_nodes()
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
        
    queue: Deque[Node] = deque()
    traversal_order: List[Node] = []
    
    start_node = graph.get_node_by_label(start_node_label)
    
    if start_node == None:
        print(f"Node with label {start_node_label} not found")
        return
    
    queue.append(start_node)
    node_states[start_node] = NodeState.VISITING
    
    while queue:
        node = queue.popleft()
        
        traversal_order.append(node)
        node_states[node] = NodeState.VISITED
        
        for edge in node.get_edges():
            to_node = edge.to_node
            if node_states[to_node] == NodeState.NOT_STARTED:
                node_states[to_node] = NodeState.VISITING
                queue.append(to_node)
                
    
    return traversal_order