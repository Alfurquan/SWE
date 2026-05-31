from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
import heapq

@dataclass
class Request:
    id: str
    start_time: int
    end_time: int

    def __lt__(self, other: 'Request') -> bool:
        return self.end_time < other.end_time

class Status(Enum):
    START = "START"
    END = "END"

class Solution:
    def find_max_overlapping_requests(self, request_logs: List[str], w: int) -> int:
        requests: List[Request] = []
        request_start_times: Dict[str, int] = {}

        for log in request_logs:
            log_parts = log.split(":")
            
            timestamp = int(log_parts[0])
            request_id = log_parts[1]
            status = log_parts[2]

            if status != Status.START.value and status != Status.END.value:
                continue

            if status == Status.START.value:
                request_start_times[request_id] = timestamp
            else:
                if request_id not in request_start_times:
                    continue

                request_duration = timestamp - request_start_times[request_id]
                if request_duration <= w:
                    requests.append(Request(request_id, request_start_times[request_id], timestamp))
            
        
        requests.sort(key=lambda request: request.start_time)

        active_requests : List[Request] = []
        max_overlapping_count = 0

        for request in requests:
            while active_requests and active_requests[0].end_time < request.start_time:
                heapq.heappop(active_requests)

            heapq.heappush(active_requests, request)
            max_overlapping_count = max(max_overlapping_count, len(active_requests))

        return max_overlapping_count
        
