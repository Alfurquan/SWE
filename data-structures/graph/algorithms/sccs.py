from graph import Graph, Node
from typing import List, Dict
from algorithms.node_state import NodeState

def find_scss(graph: Graph) -> List[List[str]]:
    finish_order = _find_finish_order(graph)
    transpose_graph = graph.create_transpose()
    return _find_sccs_in_transpose(transpose_graph, finish_order)
            
def _find_finish_order(graph: Graph) -> List[Node]:
    result: List[Node] = []
    nodes = graph.get_nodes()
    
    node_states: Dict[Node, NodeState] = {}
    nodes = graph.get_nodes()
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
    
    for node in nodes:
        if node_states[node] == NodeState.NOT_STARTED:
            _record_finish_order(node, node_states,  result)
            
    return result

def _find_sccs_in_transpose(graph: Graph, order: List[Node]) -> List[List[str]]:
    node_states: Dict[Node, NodeState] = {}
    nodes = graph.get_nodes()
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
    
    result: List[List[str]] = []
    scc: List[str] = []
    
    for node in reversed(order):
       scc = []
       transpose_node = graph.nodes[node.label]
       if node_states[transpose_node] == NodeState.NOT_STARTED:
           _dfs_rec(transpose_node, node_states, scc)
           result.append(scc)
           
    return result 

def _dfs_rec(node: Node, node_states: Dict[Node, NodeState], order: List[Node]):
    node_states[node] = NodeState.VISITING
    order.append(node.label)
    
    for edge in node.get_edges():
        to_node = edge.to_node
        if node_states[to_node] == NodeState.NOT_STARTED:
            _dfs_rec(to_node, node_states, order)
    
    node_states[node] = NodeState.VISITED

def _record_finish_order(node: Node, node_states: Dict[Node, NodeState], order: List[Node]):
    node_states[node] = NodeState.VISITING
    
    for edge in node.get_edges():
        to_node = edge.to_node
        if node_states[to_node] == NodeState.NOT_STARTED:
            _record_finish_order(to_node, node_states, order)
    
    order.append(node)
    node_states[node] = NodeState.VISITED