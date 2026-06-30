from typing import List, Dict, Set

class Node:
    def __init__(self, label: int):
        self.label = label
        self.edges: List['Edge'] = []

    def add_edge(self, edge: 'Edge'):
        self.edges.append(edge)

    def get_edges(self) -> List['Edge']:
        return self.edges

class Edge:
    def __init__(self, from_node: Node, to_node: Node):
        self.from_node = from_node
        self.to_node = to_node

class Graph:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}

    def add_node(self, label: int):
        self.nodes[label] = Node(label)

    def add_edge(self, from_label: int, to_label: int):
        from_node = self.nodes.get(from_label, None)
        to_node = self.nodes.get(to_label, None)

        if from_node is None or to_node is None:
            return

        from_node.add_edge(Edge(from_node, to_node))
        to_node.add_edge(Edge(to_node, from_node))

    def get_critical_connections(self) -> List[List[int]]:
        low: Dict[Node, int] = {node : 0 for node in self.nodes.values()}
        disc: Dict[Node, int] = {node : 0 for node in self.nodes.values()}

        self.time = 0

        visited: Set[Node] = set()

        critical_connections: List[List[int]] = []

        for node in self.nodes.values():
            if node not in visited:
                self._traverse(node, None, low, disc, critical_connections, visited)

        return critical_connections
    
    def _traverse(self, node: Node, parent: Node, low: Dict[Node, int], disc: Dict[Node, int], critical_connections: List[List[int]], visited: Set[Node]):
        visited.add(node)

        low[node] = self.time
        disc[node] = self.time
        self.time += 1

        for edge in node.get_edges():
            to_node = edge.to_node

            if to_node == parent:
                continue

            if to_node not in visited:
                self._traverse(to_node, node, low, disc, critical_connections, visited)

                low[node] = min(low[node], low[to_node])

                if low[to_node] > disc[node]:
                    critical_connections.append([node.label, to_node.label])   
            else:
                low[node] = min(low[node], disc[to_node])

class Solution:
    def get_single_points_of_failures(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        graph = self._build_graph(n, connections)

        return graph.get_critical_connections()

    def _build_graph(self, n: int, connections: List[List[int]]) -> Graph:
        graph = Graph()

        for node in range(n):
            graph.add_node(node)

        for connection in connections:
            graph.add_edge(connection[0], connection[1])
        
        return graph
