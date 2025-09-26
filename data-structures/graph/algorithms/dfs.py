from graph import Graph, Node
from typing import List, Dict
from algorithms.node_state import NodeState
    
def dfs(graph: Graph) -> List[Node]:
    node_states: Dict[Node, NodeState] = {}
    order: List[Node] = []
    nodes = graph.get_nodes()
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
        
    for node in nodes:
        if node_states[node] == NodeState.NOT_STARTED:
            _dfs_rec(node, node_states, order)
            
    return order

def _dfs_rec(node: Node, node_states: Dict[Node, NodeState], order: List[Node]):
    node_states[node] = NodeState.VISITING
    order.append(node)
    
    for edge in node.get_edges():
        to_node = edge.to_node
        if node_states[to_node] == NodeState.NOT_STARTED:
            _dfs_rec(to_node, node_states, order)
    
    node_states[node] = NodeState.VISITED