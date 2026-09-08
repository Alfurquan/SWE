from typing import List, Dict, Tuple
from collections import defaultdict
import heapq

class SignalPropagation:
    def min_time(self, n: int, connections: List[List[int]], k: int) -> int:
        adj_list: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        times: Dict[int, int] = {}
        heap: List[Tuple[int, int]] = []

        for connection in connections:
            adj_list[connection[0]].append((connection[1], connection[2]))

        heapq.heappush(heap, (0, k))
        times[k] = 0

        while heap:
            time, node = heapq.heappop(heap)

            for next_node, dist in adj_list[node]:
                if next_node not in times or times[next_node] > time + dist:
                    heapq.heappush(heap, (time + dist, next_node))
                    times[next_node] = time + dist

        if len(times) != n:
            return -1

        return max(times.values())