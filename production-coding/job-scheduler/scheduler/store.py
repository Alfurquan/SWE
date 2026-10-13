from abc import ABC, abstractmethod
from .job import Job, JobStatus
from typing import List, Dict, Optional
from threading import Condition
import heapq

class Store(ABC):
    @abstractmethod
    def store_job(self, job: Job) -> None:
        pass

    @abstractmethod
    def select_next_job(self) -> Optional[Job]:
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    def update_job(self, job_id: str, job: Job) -> None:
        pass

    @abstractmethod
    def cancel_job(self, job_id: str) -> bool:
        pass

    @abstractmethod
    def mark_job_as_running(self, job_id: str) -> None:
        pass

    @abstractmethod
    def mark_job_as_succeeded(self, job_id: str) -> None:
        pass

    @abstractmethod
    def mark_job_as_failed(self, job_id: str) -> None:
        pass

class InMemoryStore(Store):
    def __init__(self):
        self.ready_jobs: List[Job] = []
        self.jobs: Dict[str, Job] = {}
        self.condition = Condition()

    def store_job(self, job: Job) -> None:
        with self.condition:
            heapq.heappush(self.ready_jobs, job)
            self.jobs[job.id] = job
            self.condition.notify_all()

    def select_next_job(self) -> Optional[Job]:
        with self.condition:
            while self.ready_jobs and self.ready_jobs[0].status != JobStatus.PENDING:
                heapq.heappop(self.ready_jobs)
    
            if not self.ready_jobs:
                return None
    
            return self.ready_jobs[0]

    def get_job(self, job_id: str) -> Optional[Job]:
        with self.condition:
            return self.jobs.get(job_id, None)

    def update_job(self, job_id: str, job: Job):
        with self.condition:
            self.jobs[job_id] = job

    def cancel_job(self, job_id: str) -> bool:
        with self.condition:
            job = self.jobs.get(job_id, None)

            if job is None or job.status != JobStatus.PENDING:
                return False

            job.update_status(JobStatus.CANCELLED)
            self.condition.notify_all()
            return True
        
    def mark_job_as_running(self, job_id: str) -> None:
        with self.condition:
            job = self.get_job(job_id)

            if not job:
                return

            job.update_status(JobStatus.RUNNING)

    def mark_job_as_succeeded(self, job_id: str) -> None:
        with self.condition:
            job = self.get_job(job_id)

            if not job:
                return

            job.update_status(JobStatus.SUCCEEDED)

    def mark_job_as_failed(self, job_id: str) -> None:
        with self.condition:
            job = self.get_job(job_id)

            if not job:
                return

            job.update_status(JobStatus.FAILED)