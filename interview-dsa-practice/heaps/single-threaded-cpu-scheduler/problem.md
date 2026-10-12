# Problem: Single-Threaded CPU Scheduler
You're given tasks where tasks[i] = [enqueue_time_i, processing_time_i]. A single CPU processes tasks under these rules:

- The CPU is idle if no task is available.
- When the CPU is free and at least one task has enqueue_time <= current_time, it picks the available task with the shortest processing time. Ties broken by smallest original index.
- Once started, a task runs to completion (non-preemptive).
- If the CPU is idle and no task is available yet, it jumps to the enqueue time of the next task.

Return the order in which tasks are processed, as a list of their original indices.

Example 1
```
Input:  tasks = [[1,2],[2,4],[3,2],[4,1]]
Output: [0, 2, 3, 1]
```

Example 2
```
Input:  tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]
Output: [4, 3, 2, 0, 1]
```

## Solution

I would solve this problem using a min heap which will store tasks being processed by the cpu ordered by processing time and index, so that we process the smaller processing tasks first. I would sort all the tasks by enqueue time and we need some way to keep track of the index of the task, so I would store the tasks in a custom class for it.

Here is the high level algorithm for the approach

- Define class for Task
```python
Class Task:
    def __init__(self, enqueue: int, processing: int, index: int):
        self.enqueue = enqueue
        self.processing = processing
        self.index = index

    def __lt__(self, other: 'Task') -> bool:
        return (self.processing, self.index) < (other.processing, other.index)
```
- Initialize task_list: List[Task] = []
- Initialize order: List[int] = []
- Initialize cpu: List[Task] = []  // min heap storing processing task by cpu
- for index in range(len(tasks)):
    - task_list.append(Task(task[0], task[1], index))
- task_list.sort(key=lambda task: task.enqueue)
- Initialize index = 0, time = task_list[0].enqueue
- while index < len(task_list) or cpu:
    - while index < len(task_list) and time >= task_list[index].enqueue:
        - heapq.heappush(cpu, (task_list[index]))
        - index += 1

    - if len(cpu) == 0:
        time = task_list[index].enqueue
        continue
    
    - task = heapq.heappop(cpu)
    - order.append(task.index)
    - time += task.processing
- return order

## Time complexity

- O(NlogN) for sorting
- O(NlogN) for loop and min heap operations. Even though while loop present inside for loop, it runs a total of N times as each task is inserted and popped from the min heap at most once, so a total of N times.

## Space complexity

- O(N) for min heap, order and task_list arrays.


