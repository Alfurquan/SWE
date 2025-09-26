from undirected_graph import UndirectedGraph
from directed_graph import DirectedGraph
from algorithms import dfs, bfs, topological_sort, find_scss

print("----------------UnDirected graph algorithms-------------------------")


graph = UndirectedGraph()
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')

graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
#graph.add_edge('B', 'D')
graph.add_edge('C', 'D')

print("DFS traversal")
print(dfs(graph))

print("BFS traversal")
print(bfs(graph, 'A'))

print("Cycle detection")
print(graph.detect_cycle())


print("----------------Directed graph algorithms-------------------------")


graph = DirectedGraph()
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')

graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('C', 'D')
graph.add_edge('B', 'D')
# graph.add_edge("D", 'A')

print("DFS traversal")
print(dfs(graph))

print("BFS traversal")
print(bfs(graph, 'A'))

print("Topological sort")
print(topological_sort(graph))

print("Strongly connected components")
print(find_scss(graph))

print("Cycle detection")
print(graph.detect_cycle())
