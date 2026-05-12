from sortedcontainers import SortedSet
from dataclasses import dataclass
from typing import Dict, Tuple
from enum import Enum

class EventType(Enum):
    StartEvent = "Start"
    EndEvent = "End"

@dataclass
class Log:
    job_id: str
    timestamp: int
    event_type: EventType

class TimeoutDetector:
    def __init__(self, threshold):
        self.threshold = threshold
        self.inprogress_jobs: SortedSet[Tuple[int, str]] = SortedSet()
        self.job_index: Dict[str, int] = {}
        self.watermark_time = 0
        self.first_ever_timed_out_job = None
    
    def process_log(self, log: Log) -> str:
        """
        Process a single log message
        and return the job id of the job to cross the threshold if any, else return None
        """
        self.watermark_time = max(self.watermark_time, log.timestamp)

        if log.event_type == EventType.StartEvent:
            self.inprogress_jobs.add((log.timestamp + self.threshold, log.job_id))
            self.job_index[log.job_id] = log.timestamp + self.threshold
        else:
            if log.job_id not in self.job_index:
                return self.first_ever_timed_out_job
            
            expected_timeout = self.job_index.pop(log.job_id)
            self.inprogress_jobs.remove((expected_timeout, log.job_id))

        while self.inprogress_jobs and self.inprogress_jobs[0][0] <= self.watermark_time:
            timeout_time, job_id = self.inprogress_jobs.pop(0)
            self.job_index.pop(job_id)

            if self.first_ever_timed_out_job is None:
                self.first_ever_timed_out_job = job_id

        return self.first_ever_timed_out_job
        

    def get_first_timeout(self) -> str:
        """
        Returns the job id of the job to cross the threshold
        """
        return self.first_ever_timed_out_job