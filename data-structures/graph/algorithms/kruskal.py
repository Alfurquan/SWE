from typing import Dict, List
from union_find import UnionFind
from graph import Graph, WeightedEdge

def kruskal(graph: Graph) -> List[WeightedEdge]:
    nodes = graph.get_nodes()
    node_to_index: Dict = {node: i for i, node in enumerate(nodes)}
    union_find = UnionFind(len(nodes))

    edges: List[WeightedEdge] = []

    for node in nodes:
        for edge in node.get_edges():
            edges.append(edge)

    edges.sort(key=lambda edge: edge.weight)

    mst = []
    for edge in edges:
        from_idx = node_to_index[edge.from_node]
        to_idx = node_to_index[edge.to_node]
        if union_find.find(from_idx) != union_find.find(to_idx):
            union_find.union(from_idx, to_idx)
            mst.append(edge)
            if len(mst) == len(nodes) - 1:
                break
    return mst
