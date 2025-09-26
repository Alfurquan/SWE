"""
Week 2 - Problem 3: Graph Representation & Traversal
Difficulty: Medium | Time Limit: 40 minutes | Google L5 Graph Fundamentals

PROBLEM STATEMENT:
Implement graph data structure with traversal algorithms

OPERATIONS:
- addVertex(vertex): Add vertex to graph
- addEdge(v1, v2, weight): Add weighted edge
- bfs(start): Breadth-first search traversal
- dfs(start): Depth-first search traversal
- shortestPath(start, end): Find shortest path
- hasPath(start, end): Check if path exists

REQUIREMENTS:
- Support both directed and undirected graphs
- Handle weighted and unweighted edges
- Implement both adjacency list and matrix representations
- Detect cycles

REAL-WORLD CONTEXT:
Social networks, route planning, dependency resolution, network topology

FOLLOW-UP QUESTIONS:
- Space-time trade-offs of different representations?
- Handling very large graphs?
- Distributed graph processing?
- Real-time updates to graph structure?

EXPECTED INTERFACE:
graph = Graph(directed=False)
graph.addVertex("A")
graph.addVertex("B")
graph.addEdge("A", "B", weight=5)
path = graph.shortestPath("A", "B")
print(graph.bfs("A"))  # ["A", "B"]
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
