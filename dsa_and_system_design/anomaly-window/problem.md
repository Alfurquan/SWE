# The Anomaly Window

You're building a monitoring service for a distributed microservices platform. Each service emits health metrics as a stream of events:

```json
{service: "auth", timestamp: 1000, latency_ms: 45}
{service: "auth", timestamp: 1002, latency_ms: 50}
{service: "payments", timestamp: 1003, latency_ms: 200}
{service: "auth", timestamp: 1005, latency_ms: 800}
...
```

Task: Design and implement an AnomalyDetector that identifies when a service becomes degraded. A service is degraded when its P95 latency over a sliding window of the last W seconds exceeds a given threshold T milliseconds.

Requirements:

- ingest(event) — processes an incoming event from the stream.

- is_degraded(service) -> bool — returns whether a service is currently degraded.

- get_degraded_services() -> List[str] — returns all currently degraded services, ordered by the timestamp they first became degraded.

---

## Solution

For this problem, first I will layout the high level approach I am going to take.

### Data Structures

- A dictionary mapping service names to a sorted list of recent latency measurements within the sliding window of the last W seconds. This allows efficient calculation of the P95 latency for each service.

- A Queue holding events for all services, ordered by timestamp. This allows efficient removal of old events that fall outside the sliding window of the last W seconds.

- An Ordered dictionary mapping service names to true/false which stores it in the order the service names are inserted in to this dict.

### Logic

- ingest(event)
    - Remove events from the queue that are older than W seconds from the current event's timestamp, and update the corresponding service's latency list. If the list becomes empty, we remove the service from the dict.
    - Compute the P95 latency for the service using its updated latency list.
    - Update the ordered dictionary to mark the service as degraded if its P95 latency exceeds the threshold T, or remove it from the dict if it no longer exceeds the threshold.
    - Add the current event to the queue and the service's latency list.
    - Compute the P95 latency for the service using its updated latency list.
    - Update the ordered dictionary to mark the service as degraded if its P95 latency exceeds the threshold T, or remove it from the dict if it no longer exceeds the threshold.

- is_degraded(service)
    - Simply return if the service name is in the dict of degraded services

- get_degraded_services()
    - Return list of degraded service from the ordered dict of degraded services.


### Assumptions

- Events arrive in increasing order of timestamp

### Time complexity

- ingest: In ingest function, we will do these operations 
    - remove from queue: Since each event will enqueue and dequeue from the queue atmost once, this step would be O(1). 
    - Updating service sorted latency list would be O(logN)
    - Compute p95 latency on sorted list of latency will be O(1)
    - Updating and removing service from ordered dict will be O(1)
    - Adding item to queue would be O(1), and to dictionary holding sorted list latency measurements would be O(logN).
    - Updating and removing service from ordered dict will be O(1)
So total time complexity will be O(logN)

- is_degraded(service)
    - It will be O(1), since we just check if service is present in the ordered dict of degraded services.

- get_degraded_services()
    - Will be O(1), since we simply return the services in the ordered dict.

### Space Complexity

- Ordered Dict of degraded services -> O(N), where N = no of services, assuming all services get degraded at the same time window.

- Queue -> O(W), since will hold events for window size w

- Dict of service to sorted list of latency -> O(N*W), where N is the number of services and W is the window size, since each service maintains a sorted list of latencies within the sliding window.

---

## Followup

`This works great on one machine. Now your event rate jumps to 10M/sec across 50 data centers. How do you partition this system across a cluster while still correctly detecting global P95 degradation per service?`

## Solution

Here is how I will scale this system to work across a cluster of data centers.
We have regional datacenters. So would partition the system first by region and then withing each region by service.

So it would look something like this

Region_1
    |_ auth
    |_ payments
    |_ checkout

Region_2
    |_ auth
    |_ payments
    |_ checkout

The flow for write would be something like this

- The request goes to a global data center.
- Based on the region where the request originated, the global data center routes it to the regional datacenter. This ensures low latency for requests to be served. The request which originated in lets say Europe is served by Europe datacenter.
- Once the request reaches the regional datacenter, based on the service, the request is routed to the right partitions.


If one of the service partition becomes hot in a region, we can use deterministic sharding where we append a shard Id to the partition name in the region. We use deterministic sharding over random suffix to ensure retries of same request end up on the same partition.

This approach helps even out the writes across partitions in a region, but has a tradeoff with reads now have to query multiple partitions. For a write heavy system, I think we can pay this cost.

Now for read flow we have these types of queries which needs to be answered

- Degraded service for region 1
- Global degraded services
- Is auth degraded in region 1 ?
- Is auth degraded globally ?

- For regional queries, the request can be routed to the regional datacenter to get the answer.
- For global queries, we can optimize further depending on use cases
    - If global queries are made less frequently, then we can fan out requests to all regions, get results from then regions and accumulate the results.
    - If global queries are made more often, then we will follow below strategy

Stream processing layer

- Each regional datacenter will write p95 latency summaries, not exact p95 latency as they are not additive. They write it to some message queue like a kafka.
- A stream processing job will consume from kafka, compute the p95 latencies for services and write it to some global datastore good for analytical queries, we can use columnar datastores here.
- The queries needing global results can fetch from this global datastore.


Regional Datacenters -> Kafka <- Stream Processing -> Columnar Global DataStore

The tradeoff here is that the global datastore might not always have the accurate results and the data can be stale sometimes which will reconcile eventually. But it is a cost we pay to keep this write heavy system efficient and performant.