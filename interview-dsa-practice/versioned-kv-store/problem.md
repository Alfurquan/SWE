# Versioned Key-Value Store
We are building a configuration management system that tracks changes to variables over time. You need to design and implement a VersionedKVStore class that supports storing values with timestamps and retrieving the correct version of a value based on a requested point in time.

The class must support the following two operations:

set(key: str, value: str, timestamp: int): Stores the key and value at the given timestamp.

get(key: str, timestamp: int) -> str: Returns the value associated with the key at the exact timestamp. If no value was set at that exact time, it should return the value from the most recent timestamp prior to the requested timestamp. If the requested timestamp is older than the very first time the key was ever set, it should return an empty string "".

## Example Usage
```python
store = VersionedKVStore()

# We set the "theme" to "dark" at timestamp 10
store.set("theme", "dark", 10)

# We ask for the theme at timestamp 15. 
# Since nothing was set exactly at 15, we fall back to the most recent value (10).
store.get("theme", 15) # Returns "dark" 

# We ask for the theme at timestamp 5.
# The earliest record of "theme" is at 10, so nothing exists yet.
store.get("theme", 5)  # Returns "" 

# We set the "theme" to "light" at timestamp 20
store.set("theme", "light", 20)

store.get("theme", 25) # Returns "light" (falls back to 20)
store.get("theme", 15) # Returns "dark" (falls back to 10)
```

---

## Approach

To implement the VersionedKVStore class, we can use a dictionary to store the key-value pairs along with their timestamps. Each key will map to a list of tuples, where each tuple contains a timestamp and the corresponding value. 

When we set a value for a key at a specific timestamp, we will append the (timestamp, value) tuple to the list associated with that key. 

When we get a value for a key at a specific timestamp, we will perform a binary search on the list of tuples for that key to find the most recent timestamp that is less than or equal to the requested timestamp. If such a timestamp exists, we return the corresponding value; otherwise, we return an empty string.