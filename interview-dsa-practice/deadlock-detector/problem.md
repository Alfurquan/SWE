# Problem: Detect a Deadlock in Task Dependencies
You're building a task scheduler. There are n tasks labeled 0 to n - 1. You're given a list deps where deps[i] = [a, b] means task a must run before task b (a directed edge a → b).

A deadlock exists if the dependencies form a cycle (a task transitively depends on itself). Return True if the dependency graph contains a cycle, False otherwise.

Example 1
```
Input:  n = 4, deps = [[0,1],[1,2],[2,3]]
Output: False
```

Example 2
```
Input:  n = 4, deps = [[0,1],[1,2],[2,0],[2,3]]
Output: True
```

## Solution

For this problem, I would model the dependencies as a graph where tasks represents nodes and the dependencies relation are represent by directed edges between the tasks.

In order to detect a cycle, there are two ways we can do it

- Using coloring and DFS
- Using Kahn's algorithm and BFS

I will go ahead and use coloring and DFS approach here.

The concept of coloring is as follows

- Each node will be colored thrice during the DFS traversal stages
    - WHITE: node has not been visited or traversed
    - GRAY: node has been visited, its edges have not been traversed yet
    - BLACK: node and all its edges have been traversed.
- If during traversal, we find a neighbouring node for a node which has color as GRAY, then it denotes a cycle.

Here is the high level algorithm of the approach. I will go with kahn's algorithm here.

- Initialize an adj_list: Dict[int, List[int]] = {}
- Initialize a color: Dict[int, int] = {}
- Initialize a queue: Deque[int] = deque()
- Initialize a in_degree: Dict[int, int] = {i : 0 for i in range(n)}
- Initialize a topo_order: List[int] = []
- Fill up adj_list from the relation list
- for each node i in 0..n - 1
    - for each neighbor in adj_list[i]
        - in_degree[neighbor] += 1
- for each node i in 0..n - 1
    - if in_degree[i] == 0
        - push i to the queue
- while queue
    - pop node from queue
    - add node to topo_order
    - for neighbor in adj_list[node]
        - in_degree[neighbor] -= 1
        - if in_degree[neighbor] == 0
            - push neighbor to queue
- return True if len(top_order) != n else False

## Time complexity

- Since each node and edge is traversed exactly once, time complexity is O(V + E), where V = no of nodes, E = no of edges

## Space complexity

- O(V + E), for adj_list and O(V) for the queue

## Kahns Algorithm

In kahn's algorithm, we store the order in which the node would be traversed. If after traversing the order does not include all the nodes, then it would mean that there is a cycle in the graph.
