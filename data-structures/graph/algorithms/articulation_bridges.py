from graph import Graph, Node
from typing import List, Dict
from algorithms.node_state import NodeState

def find_bridges(graph: Graph) -> List[List[str]]:
    node_states: Dict[Node, NodeState] = {}
    nodes = graph.get_nodes()
    bridges: List[List[str]] = []
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
        
    disc: Dict[Node, int] = {} # Discovery time for a node in DFS
    low: Dict[Node, int] = {} # The lowest discovery time reachable from u without going through the parent
    
    for node in nodes:
        if node_states[node] == NodeState.NOT_STARTED:
            _dfs(node, node_states, disc, low, 1, None, bridges)
            
    return bridges

def _dfs(node: Node, 
         node_states: Dict[Node, NodeState], 
         disc:Dict[Node, int], 
         low: Dict[Node, int], 
         curr_time: int,
         parent: Node,
         bridges: List[List[str]]):
    
    node_states[node] = NodeState.VISITING
    disc[node] = curr_time
    low[node] = curr_time
    next_time = curr_time + 1
    for edge in node.get_edges():
        to_node = edge.to_node
        
        if to_node == parent:
            continue
        
        if node_states[to_node] == NodeState.NOT_STARTED:
            _dfs(to_node, node_states, disc, low, next_time, node, bridges)
        
            low[node] = min(low[node], low[to_node])
        
            if low[to_node] > disc[node]:
                bridges.append([node.label, to_node.label])
        else:
            low[node] = min(low[node], low[to_node])
            
    node_states[node] = NodeState.VISITED
            
    
