from .store import Store
from threading import Thread, Event
from datetime import datetime, timedelta
from typing import Callable

class JobExecutor:
    def __init__(self, store: Store, clock: Callable[[], datetime] = datetime.now):
        self.store = store
        self.thread = Thread(target=self.execute_job)
        self.condition = self.store.condition
        self.clock = clock
        self.stop_event = Event()

    def execute_job(self):
        while not self.stop_event.is_set():
            with self.condition:
                job = self.store.select_next_job()
                while not self.stop_event.is_set() and (not job or job.run_at > self.clock()):
                    timeout = None
                    if job:
                        timeout = max(0, timedelta.total_seconds(job.run_at - self.clock()))
                    self.condition.wait(timeout=timeout)
                    job = self.store.select_next_job()

                if not job:
                    continue

                if self.stop_event.is_set():
                    break
                
                self.store.mark_job_as_running(job.id)
            try:
                job.execute()
                self.store.mark_job_as_succeeded(job.id)
            except Exception:
                self.store.mark_job_as_failed(job.id)
            
    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        with self.condition:
            self.condition.notify_all()
        self.thread.join()
