from typing import List, Dict, Deque
from collections import defaultdict, deque

class DeadlockDetector:
    def is_deadlock(self, n: int, deps: List[List[int]]) -> bool:
        adj_list: Dict[int, List[int]] = defaultdict(list)
        queue: Deque[int] = deque()
        in_degree: Dict[int, int] = {i : 0 for i in range(n)}
        topo_order: List[int] = []

        for dep in deps:
            adj_list[dep[0]].append(dep[1])

        for node in range(n):
            for neighbor in adj_list[node]:
                in_degree[neighbor] += 1

        for node in range(n):
            if in_degree[node] == 0:
                queue.append(node)

        while queue:
            node = queue.popleft()

            topo_order.append(node)

            for neighbor in adj_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return len(topo_order) != n
