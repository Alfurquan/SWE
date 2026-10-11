from typing import List, Tuple
import heapq

class TaskAssignment:
    def get_assignments(self, servers: List[int], tasks: List[int]) -> List[int]:
        free_servers: List[Tuple[int, int]] = []
        busy_servers: List[Tuple[int, int]] = []
        result: List[int] = []

        for index in range(len(servers)):
            heapq.heappush(free_servers, (servers[index], index))

        time = 0
        for index in range(len(tasks)):
            time = max(time, index)

            if len(free_servers) == 0:
                time = busy_servers[0][0]

            while busy_servers and busy_servers[0][0] <= time:
                _, server = heapq.heappop(busy_servers)
                heapq.heappush(free_servers, (servers[server], server))

            _, server_idx = heapq.heappop(free_servers)
            result.append(server_idx)
            heapq.heappush(busy_servers, (time + tasks[index], server_idx))

        return result
            