from typing import Deque
from collections import deque
from threading import Condition, Lock

class TaskQueue:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity should be greater than 0")
        
        self.capacity = capacity
        self.queue: Deque[int] = deque()
        self.lock = Lock()
        self.not_empty = Condition(self.lock)
        self.not_full = Condition(self.lock)
        self.shutdown = False

    def put(self, item: int) -> None:
        with self.lock:
            if self.shutdown:
                raise RuntimeError("Queue is shutting down...")

            while len(self.queue) == self.capacity:
                if self.shutdown:
                    raise RuntimeError("Queue is shutting down...")
                
                self.not_full.wait()

            if self.shutdown:
                raise RuntimeError("Queue is shutting down...")

            self.queue.append(item)
            self.not_empty.notify()
            

    def take(self) -> int:
        with self.lock:
            while not self.queue:
                if self.shutdown:
                    return None
                
                self.not_empty.wait()

            item = self.queue.popleft()
            self.not_full.notify()

        return item

    def invoke_shutdown(self):
        with self.lock:
            self.shutdown = True
            self.not_full.notify_all()
            self.not_empty.notify_all()
