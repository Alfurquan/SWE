# Metrics Storage Engine

We run a large-scale infrastructure monitoring system. Thousands of servers emit metrics — CPU usage, memory, disk I/O — every second. We need to store these metrics and support efficient queries.

Design and implement the storage engine for this system.

## Operations

- `write(metric_name: str, timestamp: int, value: float)`
- `read_range(metric_name: str, start_time: int, end_time: int) → List[(timestamp, value)]`
- `read_latest(metric_name: str) → (timestamp, value)`
- `delete(metric_name: str, timestamp: int)`

---

## Solution

Before I proceed with the implementation, I will lay out the data structures and design for the problem. 

For this problem, we would be creating a lightweight version of LSM (Log-Structured Merge) tree. The LSM tree is a data structure that is optimized for write-heavy workloads, which is suitable for our use case of storing metrics that are frequently updated.

For the scope of this problem, we would store both memtable and SSTable in memory. The memtable will be a sorted dictionary that holds the most recent writes, while the SSTable will be a list of sorted key-value pairs that represent the persisted data.

### Key 

For this problem, we would be choosing a composite key that consists of the metric name and timestamp. This will allow us to efficiently store and retrieve metrics based on their names and timestamps.

Further for Efficient read, we would store the data in memtable and sstable sorted by (metric_name, timestamp).

### Data Structures

- **Memtable**: SortedDict[(metric_name, timestamp), value] - This will hold the most recent writes in memory. It will be sorted by (metric_name, timestamp) for efficient range queries.

- **SSTable**: List[List[(metric_name, timestamp, value)]] - This will hold the persisted data in sorted order. It will be a list of lists, where each inner list represents a sorted run of key-value pairs. Each run will be sorted by (metric_name, timestamp) for efficient range queries.

- **Tombstone**: For deletion, we will use a tombstone marker to indicate that a particular metric at a specific timestamp has been deleted. This will help us avoid returning deleted metrics during read operations. In the memtable, we can represent a tombstone as a special value (e.g., None) for the corresponding key. Same for SSTable, we can store a special marker to indicate deletion.

### Approach

- Initialize the MetricsStorageEngine with an empty memtable and sstable. Pass a configurable threshold for memtable to sstable flush.
- Write Operation:
  - Insert the metric into the memtable.
  - If the memtable size exceeds the threshold, flush it to the sstable and clear the memtable.

- Read Range Operation:
    - Check both memtable and sstable
    - Get results from both, merge, dedup and filter out tombstones
    - Return the results

- Read Latest Operation:
    - Check both memtable and sstable
    - Get the latest result from both, compare and return the latest one.
    - If latest one is tombstone, return Not found

- Delete Operation:
    - Insert a tombstone marker for the specified metric and timestamp in the memtable.
    - If the memtable size exceeds the threshold, flush it to the sstable and clear the memtable.

- Compaction:
    - Periodically, we will perform compaction on the sstable.
    - Take N oldest SSTables, merge sort them into a new SSTable, and remove the old ones.
    - For duplicate keys, keep the latest value and discard the older ones. If a tombstone is encountered, discard the corresponding key-value pair.

### Complexity Analysis

- Write: Takes O(logN) for insert to memtable which is a sorted dict, O(T) for flush where T is bounded by threshold size of the memtable. Since flush happens after every T writes, amortized complexity is O(logN)
- Delete: Same O(logN) for inserting a tombstone to memtable which is a sorted dict, O(T) for flush where T is bounded by threshold size of the memtable. Since flush happens after every T writes, amortized complexity is O(logN)
- Flush: O(T), where T is the threshold size and we loop over all items in memtable to write to ss table

Now for read range and read latest, we first read memtable and then sstable and then return the final result.

Suppose we have S no of SSTables, each SS Table has T entries. Lets suppose we have N entries in memtable.
Suppose K1 is the no of entries lying in the range of start and end index for memtable bisect
Suppose K2 is the no of entries lying in the range of start and end index for sstable bisect
Suppose R is no of entries in the result set
Bisect operations take O(logN) for memtable and O(logT) for sstable

- Read Range: 
Reading from memtable - 
O(logN) + K1

Reading from sstable - 
S * (logT + K2)

Final merging and sorting - 
R Log R

Total time complexity = O(logN + K1) + O(S *(logT + K2)) + O(RlogR)

- Read latest

Reading from memtable - 
O(logN)

Reading from sstable -
O(S * logT)

Total time compexty = O(logN) + O(S*logT)

---

## Followups

### Question

"We have 100K metrics writes/sec. A single node with your LSM engine handles ~20K writes/sec. How would you partition this system across multiple nodes?"

Specifically - 

- What is your partition key and why?
- How do you route writes to the correct node?
- How many partitions/nodes do you need?
- What happens when you need to add more nodes later?

### Answer

- Regarding partition key, we have a few options. We can choose timestamp or metric_name as the partition key. If we choose timestamp as the partition key, it would melt down one partition since the data for closer timestamps would all eventually land on the same partitions. If we choose metric_name as the partition key, then as well a single high traffic metric can melt down a single partition. So we can choose a composite key of (metric_name, time_bucket) as the partition key. Lets say if we parition by (metric_name, hour_bucket), one metrics data for a given hour lives in one node. Within that node, data is sorted by exact timestamp for efficient range queries.

- For routing writes to the correct node, we can use consistent hashing on the composite key (metric_name, time_bucket) to determine which node should handle the write. This way, we can ensure that writes for the same metric and time_bucket are routed to the same node.

- We have 100K metrics writes/sec and a single node can handle ~20K writes/sec, so we need atleast 100K/20K = 5 nodes. Now to ensure that we have some buffer for peak loads and future growth, we can start with 5 * 1.5 = 8 nodes.

- When we need to add more nodes later, we can use consistent hashing to redistribute the keys across the new set of nodes. This way, we can ensure that the data is evenly distributed across the new set of nodes without having to move all the data around. With consistent hashing and virtual nodes, only ~1/N of the data needs to move when adding a node. The migration is background copying of SSTables. During migration, reads might need to check both old and new node.

---

### Question

A user queries: 'Give me cpu_usage across ALL servers for the last hour.' Your data is partitioned by (metric_name, time_bucket). How does your system serve this query? What's the latency profile? How would you optimize it if this query pattern is frequent?

### Answer

Our data is here partitioned by (metric_name, time_bucket). 

So for a query like 'Give me cpu_usage across ALL servers for the last hour', we would need to query all the nodes that have data for the metric_name 'cpu_usage' and the time_bucket corresponding to the last hour.

#### Read request flow

- This means when the client wants to read this data, it sends it our database. 
- Internally the database would then compute all the nodes having data for this metric (cpu_usage) for the time_bucket which is last hour and send out requests to all those nodes. 
- Each node would then read the data from its memtable and sstable, merge the results, and send it back to the database. 
- The database would then merge the results from all the nodes and return the final result to the client

#### Latency profile

- For each read request, we need multiple request to each of the node having the data points which the read request is interested in.
- Latency for the read request would be the maximum latency of all the nodes that are queried.
- Mathematically, if we have N nodes that are queried, and each node has a latency of L_i, then the total latency for the read request would be max(L_1, L_2, ..., L_N) + network latency for sending requests and receiving responses from all the nodes.

#### Optimization

- If this query pattern is frequent, we can optimize it by creating a materialized view or a pre-aggregated table that stores the cpu_usage metrics for all servers for the last hour. 
- This way, when a user queries for this data, we can simply read from the pre-aggregated table instead of querying all the nodes and merging the results.
- Materialized view updation options
    - On the write path: every write to cpu_usage also updates a rolling aggregate (adds write amplification but makes reads instant)
    - Async pipeline: stream writes through Kafka → aggregation job → write to a read-optimized store. Adds seconds of delay but doesn't impact write throughput.
    - Which one you'd choose depends on whether the user needs real-time or can tolerate 5-10s staleness.

---

### Question

Your system is taking 100K writes/sec. Compaction is a background process that merges SSTables. What happens if your write rate is so high that compaction can't keep up? How does the system degrade? What are your options to handle this?

### Answer

If the write rate exceeds the rate at which compaction can keep up, the system will start to degrade in the following ways:

- The memtable will fill up faster than it can be flushed to the SSTable, leading to increased memory usage and potential out-of-memory errors.
- The number of SSTables will increase, leading to increased read latency as more SSTables need to be checked for each read operation.
- Eventually the system may stall writes entirely to let compaction catch up.

#### Options to handle

- Backpressure: Implement backpressure on the write path to slow down incoming writes when the system is under heavy load. This can be done by rejecting writes or slowing down the rate at which writes are accepted.
- Circuit breaker: Implement a circuit breaker pattern that temporarily stops accepting writes when the system is under heavy load. This can help prevent the system from becoming overwhelmed and allow compaction to catch up.
- Horizontal scaling: Add more nodes, each node handle fewer writes, compaction has more headroom
- Increase compaction parallelism: Run multiple compaction threads. Tradeoff is that competes with read/write threads for CPU and disk bandwidth. So we need to tune the number of compaction threads based on the system's resources and workload.
- Larger memtable: Increase the size of the memtable to allow for more writes before flushing to SSTable. This can help reduce the frequency of flushes and give compaction more time to catch up. However, this will increase memory usage and may lead to out-of-memory errors if not managed properly.