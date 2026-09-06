from typing import List, Dict, Deque, Tuple
from collections import deque

class CheapestFlight:
    def get_cheapest_flight_with_stops(self, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        graph: Dict[int, List[Tuple[int, int]]] = {}

        for flight in flights:
            if flight[0] not in graph:
                graph[flight[0]] = []
            
            graph[flight[0]].append((flight[1], flight[2]))

        queue: Deque[Tuple[int, int, int]] = deque()
        min_cost: Dict[int, int] = {}

        queue.append((src, 0, 0))
        min_cost[src] = 0

        while queue:
            city, cost, stops = queue.popleft()

            if stops > k:
                continue

            for next_city, price in graph.get(city, []):
                if next_city not in min_cost or min_cost[next_city] > price + cost:
                    min_cost[next_city] = price + cost
                    queue.append((next_city, price + cost, stops + 1))

        return -1 if dst not in min_cost else min_cost[dst]