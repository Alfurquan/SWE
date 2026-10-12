from typing import List
import heapq

class Task:
    def __init__(self, enqueue: int, processing: int, index: int):
        self.enqueue = enqueue
        self.processing = processing
        self.index = index

    def __lt__(self, other: 'Task') -> bool:
        return (self.processing, self.index) < (other.processing, other.index)

class CPUScheduler:
    def get_task_order(self, task_list: List[List[int]]) -> List[int]:
        tasks: List[Task] = []
        cpu: List[Task] = []
        order: List[int] = []

        for index in range(len(task_list)):
            tasks.append(Task(task_list[index][0], task_list[index][1], index))

        tasks.sort(key=lambda task: task.enqueue)
        time = tasks[0].enqueue
        index = 0

        while index < len(tasks) or cpu:
            while index < len(tasks) and tasks[index].enqueue <= time:
                heapq.heappush(cpu, tasks[index])
                index += 1

            if len(cpu) == 0:
                time = tasks[index].enqueue
                continue

            task = heapq.heappop(cpu)
            order.append(task.index)
            time += task.processing

        return order