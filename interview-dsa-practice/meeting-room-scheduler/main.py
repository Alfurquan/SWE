from typing import List, Tuple
import heapq


class Meeting:
    def __init__(self, start_time: int, end_time: int):
        self.start_time = start_time
        self.end_time = end_time

    def __lt__(self, other: 'Meeting') -> bool:
        return self.end_time < other.end_time

class MeetingInterval:
    def __init__(self, meeting: Meeting, index: int):
        self.meeting = meeting
        self.index = index

class MeetingRoomScheduler:
    def min_meeting_rooms(self, meetings: List[Meeting]) -> int:
        meetings.sort(key=lambda meeting: meeting.start_time)

        max_rooms = 0
        current_meetings: List[Meeting] = []

        for meeting in meetings:
            while current_meetings and current_meetings[0].end_time <= meeting.start_time:
                heapq.heappop(current_meetings)

            heapq.heappush(current_meetings, meeting)
            max_rooms = max(max_rooms, len(current_meetings))

        return max_rooms

    def meeting_rooms(self, meetings: List[Meeting]) -> List[int]:
        meeting_intervals: List[MeetingInterval] = []

        for index in range(len(meetings)):
            meeting_intervals.append(MeetingInterval(meetings[index], index))

        busy_room_count = 0
        free_rooms: List[int] = []
        result: List[int] = [0] * len(meetings)
        ongoing_meetings: List[Tuple[int, int]] = []

        meeting_intervals.sort(key=lambda interval: interval.meeting.start_time)

        for meeting_interval in meeting_intervals:
            index = meeting_interval.index
            meeting = meeting_interval.meeting

            while ongoing_meetings and ongoing_meetings[0][0] <= meeting.start_time:
                _, room = heapq.heappop(ongoing_meetings)
                busy_room_count -= 1
                heapq.heappush(free_rooms, room)

            if len(free_rooms) == 0:
                heapq.heappush(free_rooms, busy_room_count)

            room = heapq.heappop(free_rooms)
            result[index] = room
            heapq.heappush(ongoing_meetings, [meeting.end_time, room])
            busy_room_count += 1

        return result