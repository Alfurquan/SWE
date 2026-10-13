from abc import abstractmethod, ABC
from enum import Enum
from datetime import datetime
import uuid

class JobStatus(Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    CANCELLED = 'Cancelled'
    FAILED = 'Failed'

class Job(ABC):

    def __init__(self, name: str, run_at: datetime):
        self.name = name
        self.run_at = run_at
        self.id = str(uuid.uuid4())
        self.status = JobStatus.PENDING

    def __lt__(self, other: 'Job') -> bool:
        return (self.run_at, self.id) < (other.run_at, other.id)

    def update_status(self, status: JobStatus):
        self.status = status
    
    @abstractmethod
    def execute(self):
        pass