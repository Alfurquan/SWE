from abc import ABC, abstractmethod
from typing import List, Dict
from enum import Enum

class NodeState(Enum):
    NOT_STARTED = 'Not Started'
    VISITING = 'Visiting'
    VISITED = 'Visited'
    
class Node:
    def __init__(self, label: str):
        self.label = label
        self.edges: List['Edge'] = []
    
    def add_edge(self, edge: 'Edge'):
        self.edges.append(edge)
        
    def get_edges(self) -> List['Edge']:
        return self.edges
    
    def __repr__(self) -> str:
        return self.label
    
    def __eq__(self, value) -> bool:
        return isinstance(value, Node) and self.label == value.label
    
    def __hash__(self):
        return hash(self.label)
    
    def __lt__(self, other):
        """Enable Node comparison for priority queues"""
        if not isinstance(other, Node):
            return NotImplemented
        return self.label < other.label
        
class Edge:
    def __init__(self, to_node: Node):
        self.to_node = to_node
        
class WeightedEdge(Edge):
    def __init__(self, from_node: Node, to_node: Node, weight: float):
        super().__init__(to_node)
        self.weight = weight
        self.from_node = from_node

class Graph(ABC):
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.node_states: Dict[Node, NodeState] = {}
    
    def add_node(self, label: str):
        node = Node(label)
        self.nodes[label] = node    
    
    def get_nodes(self) -> List[Node]:
        return self.nodes.values()
    
    def get_node_by_label(self, label: str) -> Node:
        return self.nodes.get(label, None)
    
    @abstractmethod
    def add_edge(self, from_label: str, to_label: str):
        pass

    @abstractmethod
    def detect_cycle(self) -> bool:
        pass
    
    @abstractmethod
    def create_transpose(self) -> 'Graph':
        pass

    def reset_node_state(self):
        for node in self.nodes.values():
            self.node_states[node] = NodeState.NOT_STARTED