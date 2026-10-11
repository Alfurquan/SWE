from store import Store
from job import JobStatus
from threading import Thread, Event

class JobExecutor:
    def __init__(self, store: Store):
        self.store = store
        self.thread = None
        self.event = Event()
        self.condition = self.store.condition

    def execute_job(self):
        while not self.event.is_set():
            job = self.store.select_next_job(self.event)
            if job is None:
                break
            self.store.mark_job_as_running(job.id)
            try:
                job.execute()
            except Exception as e:
                self.store.mark_job_as_failed(job.id)
            else:
                self.store.mark_job_as_succeeded(job.id)

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = Thread(target=self.execute_job)
            self.thread.start()

    def stop(self):
        if self.thread is not None and self.thread.is_alive():
            self.event.set()
            with self.condition:
                self.condition.notify_all()
            self.thread.join()
            self.thread = None
            self.event.clear()


