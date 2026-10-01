# Problem: Time-Based Key-Value Store

(asked at Google, Databricks, and similar for senior roles)

Design a key-value store where each key can have multiple values over time, each stamped with a timestamp. Support:

- set(key, value, timestamp) — store value for key at the given timestamp.
- get(key, timestamp) — return the value that was set for key at the largest timestamp ≤ the query timestamp. If no such value exists (no set at or before that time), return "".
Guarantee: calls to set on a given key are made with strictly increasing timestamps.

Example
```
store = TimeMap()
store.set("foo", "bar", 1)
store.get("foo", 1)      -> "bar"
store.get("foo", 3)      -> "bar"     # latest at or before 3 is (1,"bar")
store.set("foo", "bar2", 4)
store.get("foo", 4)      -> "bar2"
store.get("foo", 5)      -> "bar2"
store.get("foo", 0)      -> ""        # nothing set at or before time 0
```

## Solution

We would need to design a time based key value store here. So the data structure that we would use here need to answer question like what was the value of a key at a timestamp.

So we would store the data in this sort of a data structure to answer the question efficiently -

- items: Dict[str, SortedDict[[int, str]]] // Key -> [(timestamp, value)], where dict is sorted by timestamp.

The sort order by timestamp helps in retrieving the value at a timestamp quickly by using binary search on the dict in O(logN) time instead of linear search which would take O(N) time.

Here is the high level algorithm/pseudocode for the problem - 

- Initialize items: Dict[str, SortedDict[[int, str]]] = {}
- set(key, value, timestamp):
    - if key not in items:
        - items[key] = SortedDict()
    - items[key][timestamp] = value

- get(key, timestamp) -> str:
    - if key not in items:
        - return ""
    - list_items = items[key]
    - index = list_items.bisect_right(timestamp) - 1
    - return "" if index < 0 else list_items.peekitem(index)[1]

## Time complexity

- set: O(logN) for sorted dict insertion

- get: O(logN) for bisect operations

## Space complexity

- O(N) for storing items in the dict