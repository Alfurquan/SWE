from typing import List, Deque
from collections import deque
from threading import Condition, Lock, Thread
import time

class ConcurrentWriter:
    def __init__(self, capacity: int, batch_size: int, flush_interval: int):
        if capacity <= 0 or batch_size <= 0 or flush_interval <= 0:
            raise ValueError("Invalid arguments")

        self.capacity = capacity
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.lock = Lock()
        self.queue: Deque[str] = deque()
        self.not_empty = Condition(self.lock)
        self.not_full = Condition(self.lock)
        self.is_shutdown = False
        self.writer_thread = Thread(target=self.writer_loop)
        self.writer_thread.start()

    def write(self, record: str) -> None:
        with self.not_full:
            while len(self.queue) == self.capacity:
                if self.is_shutdown:
                    raise RuntimeError("Writer is shutting down")

                self.not_full.wait()

            if self.is_shutdown:
                raise RuntimeError("Writer is shutting down")

            self.queue.append(record)
            self.not_empty.notify()

    def writer_loop(self) -> None:
        while True:
            with self.not_empty:
                if self.is_shutdown and len(self.queue) == 0:
                    break

                while len(self.queue) == 0:
                    if self.is_shutdown:
                        break

                    self.not_empty.wait()

                if len(self.queue) == 0:
                    break

                batch: List[str] = []
                record = self.queue.popleft()
                self.not_full.notify()

                batch.append(record)
                deadline = time.monotonic() + self.flush_interval

                while len(batch) < self.batch_size:
                    remaining = deadline - time.monotonic()

                    if remaining <= 0:
                        break

                    while len(self.queue) == 0:
                        remaining = deadline - time.monotonic()

                        if remaining <= 0 or self.is_shutdown:
                            break

                        self.not_empty.wait(timeout=remaining)

                    if len(self.queue) == 0:
                        break

                    record = self.queue.popleft()
                    batch.append(record)
                    self.not_full.notify()

            print(f"Flushing batch to the file on disk")

    def shutdown(self):
        with self.lock:
            self.is_shutdown = True
            self.not_full.notify_all()
            self.not_empty.notify_all()

        self.writer_thread.join()