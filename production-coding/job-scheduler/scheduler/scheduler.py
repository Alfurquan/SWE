from job import Job, JobStatus
from store import Store

class Scheduler:
    def __init__(self, store: Store):
        self.store = store

    def schedule(self, job: Job) -> str:
        self.store.store_job(job)
        return job.id

    def cancel(self, job_id: str) -> bool:
        return self.store.cancel_job(job_id)