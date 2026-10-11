from abc import ABC, abstractmethod
from job import Job, JobStatus
from typing import List, Dict, Optional
from threading import Condition, Event
import heapq

class Store(ABC):
    @abstractmethod
    def store_job(self, job: Job) -> None:
        pass

    @abstractmethod
    def select_next_job(self, shutdown_event: Event) -> Optional[Job]:
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

    def get_job(self, job_id: str) -> Optional[Job]:
        with self.condition:
            return self.jobs.get(job_id, None)

    def update_job(self, job_id: str, job: Job) -> None:
        with self.condition:
            if job_id not in self.jobs:
                return
            self.jobs[job_id] = job
            self.condition.notify_all()

    def cancel_job(self, job_id: str) -> bool:
        with self.condition:
            if job_id not in self.jobs:
                return False
            job = self.jobs[job_id]

            if job.status != JobStatus.PENDING:
                return False

            job.status = JobStatus.CANCELLED
            self.condition.notify_all()
            return True
        
        return False
    
    def select_next_job(self, shutdown_event: Event) -> Optional[Job]:
        with self.condition:
            while True:
                if shutdown_event.is_set():
                    return None
                while self.ready_jobs:
                    job = heapq.heappop(self.ready_jobs)

                    if job.status == JobStatus.PENDING:
                        return job

                self.condition.wait()
                
    def mark_job_as_running(self, job_id: str) -> None:
        with self.condition:
            if job_id not in self.jobs:
                return
            job = self.jobs[job_id]
            job.update_status(JobStatus.RUNNING)
            self.condition.notify_all()

    def mark_job_as_succeeded(self, job_id: str) -> None:
        with self.condition:
            if job_id not in self.jobs:
                return
            job = self.jobs[job_id]
            job.update_status(JobStatus.SUCCEEDED)
            self.condition.notify_all()

    def mark_job_as_failed(self, job_id: str) -> None:
        with self.condition:
            if job_id not in self.jobs:
                return
            job = self.jobs[job_id]
            job.update_status(JobStatus.FAILED)
            self.condition.notify_all()