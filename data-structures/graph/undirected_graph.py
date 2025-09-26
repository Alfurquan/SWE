from collections import deque
from typing import List, Deque
from graph import Graph, Node, Edge, NodeState

class UndirectedGraph(Graph):
    def add_node(self, label: str):
        node = Node(label)
        self.nodes[label] = node
        self.node_states[node] = NodeState.NOT_STARTED
        
    def add_edge(self, from_node_label: str, to_node_label: str):
        from_node = self.nodes.get(from_node_label, None)
        to_node = self.nodes.get(to_node_label, None)
        
        if from_node == None:
            print(f"Node with label {from_node_label} not found")
            return
        
        if to_node == None:
            print(f"Node with label {to_node_label} not found")
            return
        
        from_node.add_edge(Edge(to_node))
        to_node.add_edge(Edge(from_node))     
    
    def reset_node_state(self):
        for node in self.nodes.values():
            self.node_states[node] = NodeState.NOT_STARTED
            
    def detect_cycle(self) -> bool:
        self.reset_node_state()
        for node in self.nodes.values():
            if self.node_states[node] == NodeState.NOT_STARTED:
                if self._is_cycle_present(node, None):
                    return True
                
        return False
    
    def _is_cycle_present(self, node: Node, parent_node: Node) -> bool:
        self.node_states[node] = NodeState.VISITING
        
        for edge in node.get_edges():
            to_node = edge.to_node
            if to_node == parent_node:
                continue
        
            if self.node_states[to_node] == NodeState.VISITING:
                return True
        
            if self.node_states[to_node] == NodeState.NOT_STARTED:
                if self._is_cycle_present(to_node, node):
                    return True

        self.node_states[node] = NodeState.VISITED
        return False
        
    def create_transpose(self):
        pass