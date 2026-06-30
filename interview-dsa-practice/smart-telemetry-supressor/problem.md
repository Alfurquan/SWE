# Smart Telemetry Suppressor

We are building a client-side SDK for a cloud monitoring platform. Applications use this SDK to report errors identified by an error code.

To reduce network bandwidth and avoid sending repetitive telemetry, duplicate errors should be suppressed for a configurable time window. If an error has not been emitted before, or its previous emission was sufficiently long ago, the event should be allowed through and the suppression window for that error should be reset.

### Example

Suppose the suppression window is 10 seconds.

| Timestamp | Error Code | Should Emit |
| --------- | ---------- | ----------- |
| 1         | ERR_A      | True        |
| 5         | ERR_A      | False       |
| 11        | ERR_B      | True        |
| 12        | ERR_A      | True        |
| 15        | ERR_A      | False       |

Explanation:

* At time 1, `ERR_A` is seen for the first time, so it is emitted.
* At time 5, `ERR_A` occurred again within 10 seconds of its last emission, so it is suppressed.
* At time 11, `ERR_B` is seen for the first time, so it is emitted.
* At time 12, more than 10 seconds have elapsed since `ERR_A` was last emitted at time 1, so it is emitted again and its suppression window is reset.
* At time 15, `ERR_A` occurs again within 10 seconds of its most recent emission at time 12, so it is suppressed.

### Task

Design and implement a data structure that supports this functionality.

Please discuss the API you would expose and then implement it.

### Assumptions

* Timestamps are provided as integer seconds.
* Calls arrive in non-decreasing timestamp order.
* The suppression window is specified during initialization.

### 1. Memory leak / millions of error codes

The map grows forever.

Ask:

"Suppose the process runs for weeks and sees millions of distinct errors. How would you prevent unbounded memory growth?"

Expected direction:

Expire stale entries.
Queue/deque of (timestamp, error_code).
Lazy cleanup.

This becomes:

Map: error -> last_timestamp
Queue: (timestamp, error)

Before processing timestamp t:

Remove entries whose

t - timestamp >= window

and verify they are still current before deleting from map.


### Follow-up (if time permits)

How would your design change if:

* The system runs for a long time and may observe millions of distinct error codes?
* Multiple threads may invoke the SDK concurrently?
* Events can arrive out of timestamp order?
* Suppression needs to be done based on multiple attributes (for example, `(service, machine_id, error_code)`) instead of just the error code?


