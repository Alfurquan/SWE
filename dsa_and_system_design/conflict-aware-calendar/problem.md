# The Conflict-Aware Calendar
You're building the booking engine for Google Calendar's room reservation system. Conference rooms are a scarce resource and the system must handle bookings efficiently.

Design a class RoomScheduler that supports:

book(room_id: str, start: int, end: int) → bool
    Books the room for [start, end). Returns True if successful,
    False if it conflicts with an existing booking.

cancel(room_id: str, start: int, end: int) → bool
    Cancels the exact booking. Returns True if found and removed.

find_available(room_id: str, duration: int, earliest: int) → int
    Returns the earliest start time >= earliest where the room 
    has a free slot of at least `duration` minutes.

---

## Solution

Here is the high-level approach for this problem

### Data Structure

- Dictionary to store bookings for each room. The key is the `room_id`, and the value is a sorted list of tuples representing the booked intervals for that room. Each tuple contains the start and end times of a booking. The list is sorted by start time of the booking

### Logic

Here is the high level logic for the approach

- book(room_id, start, end):
    - Check if the room_id exists in the dictionary. If not, create an empty list for that room.
    - Find the index where the new booking would fit in the sorted list of bookings for that room. We can use `bisect` to find the index on the sorted list.
    - Check if the new booking conflicts with the previous or next booking in the list. If it does, return False. Else add the new booking to the list and return True.
    - Conflict check logic: Lets say bisect returns index i, 
        - If i > 0, check if the end time of the previous booking (bookings[i-1][1]) is greater than start. If so, return False.
        - If i < len(bookings), check if the start time of the next booking (bookings[i][0]) is less than end. If so, return False.

- cancel(room_id: str, start: int, end: int) → bool
    - Check if the room_id exists in the dictionary. If not, return False.
    - Use `bisect` to find the index of the booking to cancel. If found, remove it from the list and return True. If not found, return False.

- find_available(room_id: str, duration: int, earliest: int) → int
    - Check if the room_id existis in the dictionary. If not, return -1.
    - Use bisect to find an index where start time at index >= earliest.
    - Then we start searching from max(index - 1, 0) and at each step compare if end at index - start at index + 1 is >= duration, if yes we found the slot, if not the loop goes till the end of the list and the earliest is the last end time in the list


### Time Complexity

- book: O(log n) for bisect + O(n) for insertion in the list, so overall O(n)
- cancel: O(log n) for bisect + O(n) for deletion in the list, so overall O(n)
- find_available: O(log n) for bisect + O(n) for searching the list, so overall O(n)

### Space Complexity

- O(n) where n is the number of bookings for all rooms combined. Each booking is stored in a list for each room, and the total space used is proportional to the number of bookings.