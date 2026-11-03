from typing import List, Dict, Optional, Deque
from collections import defaultdict, deque


def deployment_order(services, dependencies) -> Optional[List[str]]:
    in_degree: Dict[str, int] = {service: 0 for service in services}
    adj_list: Dict[str, List[str]] = defaultdict(list)
    topo_order: List[str] = []
    queue: Deque[str] = deque()

    for dependency in dependencies:
        for dependent in dependencies[dependency]:
            adj_list[dependency].append(dependent)

    for service in services:
        for next_service in adj_list[service]:
            in_degree[next_service] += 1

    for service in services:
        if in_degree[service] == 0:
            queue.append(service)

    while queue:
        service = queue.popleft()

        topo_order.append(service)

        for next_service in adj_list[service]:
            in_degree[next_service] -= 1
            if in_degree[next_service] == 0:
                queue.append(next_service)

    return topo_order if len(topo_order) == len(in_degree) else None

def min_time(services, dependencies) -> Optional[int]:
    in_degree: Dict[str, int] = {service: 0 for service in services}
    adj_list: Dict[str, List[str]] = defaultdict(list)
    topo_order: List[str] = []
    queue: Deque[str] = deque()
    rounds = 0

    for dependency in dependencies:
        for dependent in dependencies[dependency]:
            adj_list[dependency].append(dependent)

    for service in services:
        for next_service in adj_list[service]:
            in_degree[next_service] += 1

    for service in services:
        if in_degree[service] == 0:
            queue.append(service)

    while queue:
        size = len(queue)
        rounds += 1
        for _ in range(size):
            service = queue.popleft()

            topo_order.append(service)

            for next_service in adj_list[service]:
                in_degree[next_service] -= 1
                if in_degree[next_service] == 0:
                    queue.append(next_service)

    return rounds if len(topo_order) == len(in_degree) else None

def min_time(services, dependencies, time) -> Optional[int]:
    in_degree: Dict[str, int] = {service: 0 for service in services}
    adj_list: Dict[str, List[str]] = defaultdict(list)
    processed = 0
    queue: Deque[str] = deque()
    finish: List[int] = [0] * len(services)

    for dependency in dependencies:
        for dependent in dependencies[dependency]:
            adj_list[dependency].append(dependent)

    for service in services:
        for next_service in adj_list[service]:
            in_degree[next_service] += 1

    for service in services:
        if in_degree[service] == 0:
            queue.append(service)
            finish[service] = time[service]

    while queue:
        size = len(queue)
        for _ in range(size):
            service = queue.popleft()

            processed += 1

            for next_service in adj_list[service]:
                finish[next_service] = max(finish[next_service], finish[service] + time[next_service])
                in_degree[next_service] -= 1
                if in_degree[next_service] == 0:
                    queue.append(next_service)

    return max(finish) if processed == len(in_degree) else None