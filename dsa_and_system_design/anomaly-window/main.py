from dataclasses import dataclass
from typing import List, Dict, Deque, Tuple
from sortedcontainers import SortedList
from collections import OrderedDict, deque

import math

@dataclass
class Event:
    service: str
    timestamp: int
    latency: int

class AnomalyWindow:
    def __init__(self, window_size: int = 10, threshold_size: int = 500):
        self.window_size = window_size
        self.threshold_size = threshold_size
        self.service_latencies: Dict[str, SortedList[int]] = {}
        self.degraded_services: Dict[str, bool] = OrderedDict()
        self.event_order: Deque[Tuple[int, str, int]] = deque()

    def ingest(self, event: Event):
        service = event.service
        timestamp = event.timestamp
        latency = event.latency

        while self.event_order and timestamp - self.event_order[0][0] >= self.window_size:
            _, popped_service, popped_latency = self.event_order.popleft()

            self.service_latencies[popped_service].remove(popped_latency)
            if len(self.service_latencies[popped_service]) == 0:
                self.service_latencies.pop(popped_service)
                self.degraded_services.pop(popped_service, None)

        if service not in self.service_latencies:
            self.service_latencies[service] = SortedList()

        self.service_latencies[service].add(latency)
        self.event_order.append((timestamp, service, latency))

        p95_latency = self.get_p95_latency(service)
        is_service_degraded = p95_latency is not None and p95_latency > self.threshold_size
        
        if is_service_degraded:
            self.degraded_services[service] = True
        else:
            if service in self.degraded_services:
                self.degraded_services.pop(service)


    def get_p95_latency(self, service) -> int:
        index = math.ceil(0.95 * len(self.service_latencies[service])) - 1
        return self.service_latencies[service][index] if index >= 0 else None

    def is_degraded(self, service: str) -> bool:
        return service in self.degraded_services
    
    def get_degraded_services(self) -> List[str]:
        return [service for service in self.degraded_services]