from graph import Graph, Node
from typing import List, Dict
from algorithms.node_state import NodeState
    

def topological_sort(graph: Graph) -> List[Node]:
    order: List[Node] = []    
    node_states: Dict[Node, NodeState] = {}
    nodes = graph.get_nodes()
    
    if graph.detect_cycle() == True:
        print("Provided graph has a cycle, can't run topological sort")
        return order
    
    for node in nodes:
        node_states[node] = NodeState.NOT_STARTED
        
    for node in nodes:
        if node_states[node] == NodeState.NOT_STARTED:
            _topological_sort(node, node_states, order)
                
    return order
        
def _topological_sort(node: Node, node_states: Dict[Node, NodeState], order: List[Node]):
    node_states[node] = NodeState.VISITING
    
    for edge in node.get_edges():
        if node_states[edge.to_node] == NodeState.NOT_STARTED:
            _topological_sort(edge.to_node, node_states, order)
            
    order.append(node)
    node_states[node] = NodeState.VISITED