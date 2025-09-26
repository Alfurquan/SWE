from graph import Graph, Node
from typing import List, Dict, Set
from algorithms.node_state import NodeState

def find_articulation_points(graph: Graph) -> List[str]:
    node_states: Dict[Node, NodeState] = {}
    disc: Dict[Node, int] = {}
    low: Dict[Node, int] = {}
    
    nodes = graph.get_nodes()
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
    
    result: Set[str] = set()
    
    for node in nodes:
        if node_states[node] == NodeState.NOT_STARTED:
            _dfs(node, node_states, disc, low, 0, result, None)
        
    return list(result)

def _dfs(node: Node,
         node_states: Dict[Node, NodeState],
         disc: Dict[Node, int],
         low: Dict[Node, int],
         time: int,
         result: Set[str],
         parent: Node):
    
    node_states[node] = NodeState.VISITING
    low[node] = time
    disc[node] = time
    
    children = 0
    for edge in node.get_edges():
        to_node = edge.to_node
        
        if to_node == parent:
            continue
        
        if node_states[to_node] == NodeState.NOT_STARTED:
            children += 1
            _dfs(to_node, node_states, disc, low, time + 1, result, node)
            
            low[node] = min(low[node], low[to_node])
            
            if parent is None and children > 1:
                result.add(node.label)
            elif parent is not None and low[to_node] >= disc[node]:
                result.add(node.label)
                
        elif node_states[to_node] == NodeState.VISITING:
            low[node] = min(low[node], low[to_node])
            
    node_states[node] = NodeState.VISITED