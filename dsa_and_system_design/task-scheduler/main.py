from typing import Dict, Tuple, Optional
import time
from sortedcontainers import SortedSet

class TaskScheduler:
    def __init__(self):
        self.execution_order: SortedSet[Tuple[int, str]] = SortedSet()
        self.task_to_execution_time: Dict[str, int] = {}
    
    def schedule(self, task_id: str, delay_ms: int):
        if task_id in self.task_to_execution_time:
            print(f"Task with id {task_id} is already scheduled at {self.task_to_execution_time[task_id]}")
            return

        current_system_time = time.time()
        task_execution_time = current_system_time + (delay_ms / 1000.0)
        self.task_to_execution_time[task_id] = task_execution_time
        self.execution_order.add((task_execution_time, task_id))

    def get_next_task(self) -> Optional[str]:
        current_system_time = time.time()

        if not self.execution_order:
            return None

        if not self.execution_order[0][0] <= current_system_time:
            return None
        
        _, task_id = self.execution_order.pop(0)
        self.task_to_execution_time.pop(task_id)
        return task_id

    def cancel_task(self, task_id: str):
        if task_id not in self.task_to_execution_time:
            print(f"Task with id {task_id} is not scheduled")
            return
        
        task_execution_time = self.task_to_execution_time[task_id]
        self.execution_order.remove((task_execution_time, task_id))
        self.task_to_execution_time.pop(task_id)
