# Log Stream Aggregator

We are building a distributed tracing feature. You are given a stream of logs from a cluster of servers. Each log entry is represented as a string format: "timestamp:request_id:status".

- timestamp: An integer representing the time in seconds.
- request_id: A unique string identifier for a network request.
- status: Either "START" or "END".

The log stream is strictly sorted by timestamp. A request is considered fully captured if it has both a "START" log and an "END" log. However, due to network delays or service crashes, some requests might only have a "START" log without a corresponding "END" log.

Task: Write a function that takes this list of log strings and a window size parameter W (in seconds). The function should return the maximum number of overlapping, fully completed requests that were active at any single point in time within any rolling window of size W.

An active request is defined as one that has started but not yet ended.

Example Input:

```shell
logs = [
    "1:req_A:START",
    "2:req_B:START",
    "3:req_A:END",
    "5:req_B:END",
    "6:req_C:START"
]
W = 3
```

Example Output:

```shell
2
```

In this example, the maximum number of overlapping, fully completed requests within any rolling window of size 3 seconds is 2 (both req_A and req_B are active between timestamps 2 and 3).

--

## Approach

We would approach this problem in two phases:

### Phase 1: Parse the logs and track active requests

In this phase, we would iterate over the logs and find all valid requests, i.e. those that have both "START" and "END" logs and duration of the request is within window w. We store the start and end times of these valid requests in a list. We also drop requests which have some other string apart from "START" and "END" in the status section.

### Phase 2: Count overlapping requests within the window

In this phase, we would iterate over the list of valid requests and for each request, we would check how many other requests overlap with it within the window w.

We would be using a heap data structure. We would maintain a min-heap to keep track of the end times of the active requests. For each request, we would remove all requests from the heap that have ended before the current request's start time. Then we would add the current request's end time to the heap and update the maximum count of overlapping requests.
