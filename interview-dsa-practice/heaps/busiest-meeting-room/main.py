from typing import List, Tuple
import heapq

class MeetingRoomScheduler:
    def get_busiest_meeting_room(self, meetings: List[List[int]], n: int) -> int:
        meetings.sort(key = lambda meeting: meeting[0])
        count: List[int] = [0] * n
        free_rooms: List[int] = []
        busy_rooms: List[Tuple[int, int]] = []

        for room in range(n):
            heapq.heappush(free_rooms, room)

        for meeting in meetings:
            while busy_rooms and busy_rooms[0][0] <= meeting[0]:
                _, room  = heapq.heappop(busy_rooms)
                heapq.heappush(free_rooms, room)

            best_start_time = meeting[0]
            if len(free_rooms) == 0:
                end_time, room = heapq.heappop(busy_rooms)
                best_start_time = end_time
                heapq.heappush(free_rooms, room)

            room = heapq.heappop(free_rooms)
            meeting_end_time = best_start_time + (meeting[1] - meeting[0])
            heapq.heappush(busy_rooms, (meeting_end_time,  room))
            count[room] += 1

        return max(range(n), key= lambda room: count[room])