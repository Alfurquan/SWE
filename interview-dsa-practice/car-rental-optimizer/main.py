from typing import List, Deque, Tuple
from collections import deque
import heapq

class Request:
    def __init__(self, id: int, pickup_time: int, return_time: int):
        self.id = id
        self.pickup_time = pickup_time
        self.return_time = return_time

class Assignment:
    def __init__(self, request_id: int, car_id: int):
        self.request_id = request_id
        self.car_id = car_id

class RentalSystem:
    def assign_cars(self, n: int, requests: List[Request]) -> List[Assignment]:
        requests.sort(key = lambda request: request.pickup_time)

        serving_request: List[Tuple[int, int]] = []

        result: List[Assignment] = []
        free_cars: Deque[int] = deque()

        for i in range(n):
            free_cars.append(i)

        for request in requests:
            while serving_request and serving_request[0][0] <= request.pickup_time:
                _, car_id = heapq.heappop(serving_request)
                free_cars.append(car_id)

            car_id = free_cars.pop()
            result.append(Assignment(request.id, car_id))

            heapq.heappush(serving_request, (request.return_time, car_id))

        return result
        
