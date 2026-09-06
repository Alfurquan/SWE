from typing import List
import heapq

class Trip:
    def __init__(self, pickup: int, drop: int, num_passengers: int):
        self.pickup = pickup
        self.drop = drop
        self.num_passengers = num_passengers

    def __lt__(self, other: 'Trip'):
        return self.drop < other.drop

class Shuttle:
    def is_possible(self, trips: List[Trip], capacity: int) -> bool:
        current_capacity = capacity
        current_trips: List[Trip] = []

        trips.sort(key=lambda trip: trip.pickup)

        for trip in trips:
            while current_trips and current_trips[0].drop <= trip.pickup:
                popped_trip = heapq.heappop(current_trips)
                current_capacity += popped_trip.num_passengers

            if current_capacity < trip.num_passengers:
                return False

            heapq.heappush(current_trips, trip)
            current_capacity -= trip.num_passengers

        return True

    def get_max_passengers(self, trips: List[Trip]) -> int:
        current_passengers = 0
        max_passengers = 0
        active_trips: List[Trip] = []

        trips.sort(key=lambda trip: trip.pickup)

        for trip in trips:
            while active_trips and active_trips[0].drop <= trip.pickup:
                popped_trip = heapq.heappop(active_trips)
                current_passengers -= popped_trip.num_passengers
            
            current_passengers += trip.num_passengers
            heapq.heappush(active_trips, trip)
            max_passengers = max(max_passengers, current_passengers)


        return max_passengers