from typing import List, Dict, Deque
from collections import deque, defaultdict

class CISystem:
    def get_minimum_build_rounds(self, tasks: List[List[int]], n: int) -> int:
        task_graph: Dict[int, List[int]] = defaultdict(list)

        for task in tasks:
            task_graph[task[0]].append(task[1])

        in_degree: Dict[int, int] = {i : 0 for i in range(1, n + 1)}

        for task in task_graph:
            for dep in task_graph[task]:
                in_degree[dep] += 1

        queue: Deque[int] = deque()
        min_rounds = 0
        order: List[int] = []

        for task in range(1, n + 1):
            if in_degree[task] == 0:
                queue.append(task)

        while queue:
            size = len(queue)
            min_rounds += 1
            while size > 0:
                task = queue.popleft()
                order.append(task)

                for dep in task_graph[task]:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)

                size -= 1

        return -1 if len(order) != len(in_degree) else min_rounds

    def get_minimum_build_time(self, tasks: List[List[int]], time_list: List[int], n: int) -> int:
            task_graph: Dict[int, List[int]] = defaultdict(list)
            time: Dict[int, int] = {}

            for task in tasks:
                task_graph[task[0]].append(task[1])

            for index in range(len(time_list)):
                time[index + 1] = time_list[index]

            finish_time: List[int] = [0] * (n + 1)
    
            in_degree: Dict[int, int] = {i : 0 for i in range(1, n + 1)}
    
            for task in task_graph:
                for dep in task_graph[task]:
                    in_degree[dep] += 1
    
            queue: Deque[int] = deque()
            order: List[int] = []
    
            for task in range(1, n + 1):
                if in_degree[task] == 0:
                    queue.append(task)
                    finish_time[task] = time[task]

            while queue:
                task = queue.popleft()
                order.append(task)

                for dep in task_graph[task]:
                    in_degree[dep] -= 1
                    finish_time[dep] = max(finish_time[dep], finish_time[task] + time[dep])
                    if in_degree[dep] == 0:    
                        queue.append(dep)

    
            return -1 if len(order) != len(in_degree) else max(finish_time[1:])