from datetime import datetime, timedelta

from scheduler.store import InMemoryStore
from scheduler.executor import JobExecutor
from scheduler.job import Job
from scheduler.scheduler import JobScheduler

store = InMemoryStore()
executor = JobExecutor(store)
executor.start()

scheduler = JobScheduler(store)

class MyJob(Job):
    def execute(self):
        print(f"Executing job {self.name}")

scheduler.schedule(MyJob(name="example1", run_at=datetime.now() + timedelta(seconds=5)))
scheduler.schedule(MyJob(name="example2", run_at=datetime.now() + timedelta(seconds=10)))
executor.stop()
