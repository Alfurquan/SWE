# Problem: Minimum Build Rounds

You're building a CI system. There are n tasks labeled 1 to n. Some tasks depend on others: you're given a list dependencies where dependencies[i] = [a, b] means task a must finish before task b can start.

You have unlimited parallel workers, so in a single "round" you can run every task whose dependencies are all already complete — simultaneously. Each task takes exactly one round to run.

Return the minimum number of rounds needed to complete all n tasks. If it's impossible to complete all tasks (i.e., there's a cyclic dependency), return -1.

Example 1

```
n = 3, dependencies = [[1,3],[2,3]]
Output: 2
```

Example 2

```
n = 3, dependencies = [[1,2],[2,3],[3,1]]
Output: -1
```

## Solution

This problem maps to topological sorting in graph and we use kahn's algorithm using BFS for it. However the concept of rounds tweaks the algorithm and logic a bit.

Here is my high level approach and data structure for solving the problem

Data structures

- Graph: I will denote the dependencies as a directed graph using adjacency list.
- Queue: I will use queue to perform BFS on the graph
- Dictionary: Use a dictionary to hold the indegree of each task.

Algorithm

- Initialize a graph `graph` of type `Dict[int, List[int]]`
- Initialize a queue `queue` of type `Deque`
- Initialiize a dictionary `indegree` of type `Dict[int, int]`
- Build the graph from the dependencies list
- Build indegree dictionary for all the tasks 1..n
- Initialize a list to hold the order of tasks
- Initialize a variable rounds = 0
- Loop over all the tasks, for each task t
    - If indegree[t] == 0
        - push task t to the queue
- While queue is not empty
    - size = len(queue)
    - rounds += 1
    - while size
        - pop task t from queue
        - put task t to the order list
        - for each dependent task dep
            - indegree[dep] -= 1
            - if indegree[dep] == 0
                - push dep to the queue

- return -1 if len(order) != len(indegree) else rounds


## Time complexity

- O(V + E): Where V is the no of tasks and E is the total no of dependencies, as we push each task to the queue once and traverse each edge once.

## Space complexity

- O(V) for storing tasks and dependencies