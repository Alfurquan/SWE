# Problems

## Drill 1: The Append-Only Pivot

Scenario: You are designing a system to ingest sensor logs from IoT devices (100k writes/sec). You initially chose a standard MySQL instance with B-Tree indexing. The system is write-bound and CPU utilization is high due to index fragmentation.
Question: Why is the B-Tree architecture failing here? What specific database architecture (mentioned in your notes) would solve this without necessarily adding more servers, and what is the read-side trade-off?

---

## Solution

B-Tree indexes are optimized for read-heavy workloads, but they can become inefficient for write-heavy workloads due to the need to maintain the tree structure. Each insert can cause fragmentation and require rebalancing, which leads to high CPU utilization.

A Log-Structured Merge Tree (LSM Tree) architecture would be a better fit for this scenario. LSM Trees are designed for high write throughput by batching writes and periodically merging them into sorted runs. This allows for efficient writes without the overhead of maintaining a balanced tree structure.

The trade-off on the read side is that LSM Trees can have higher read latency, especially for point queries, because data may be spread across multiple levels of the tree. However, for workloads that are predominantly write-heavy, this trade-off is often acceptable.

"B-Trees force the disk head to jump around (Random I/O) to update pages in place. By switching to an LSM-based DB (like Cassandra or LevelDB), we turn those random writes into Sequential Writes (Append-Only), which are orders of magnitude faster on physical disks."

---

## Drill 2: The "Read-Heavy" Trap

Scenario: You have a Users table that is read-heavy (90% reads). The table is large and has many columns (profile data, preferences, etc.). However, there is one specific column, last_active_timestamp, that is updated on every API call a user makes. This single column is turning the entire table into a write-heavy bottleneck, causing lock contention and bloating the database with transaction logs.

Question: How do you apply Vertical Partitioning here to save the database?

What does the schema look like before and after the change?

Why does this specific change improve performance for the read-heavy profile data?

---

## Solution

Since the `last_active_timestamp` column is updated on every API call a user makes, we need to segregate the `Users` table accordingly. Basically we will need to partition the table here to avoid the write-heavy bottleneck.

Here's the schema before and after the changes

### Before

```sql
TABLE users(
    user_id,
    name,
    user_name,
    bio,
    ...
    last_active_timestamp
)
```

### After

```sql
TABLE users(
    user_id,
    name,
    user_name,
    bio,
    ...
)

TABLE user_active_status(
    user_id,
    last_active_timestamp
)
```

This specific change will help boost the performance for a read-heavy profile data as the profile data for the users will continue to be read from the `users` table whereas the `last_active_timestamp` column which is updated on every API call now will be updated in the `user_active_status` table.
Since both the operations now occur on different tables, the write bottle neck will now not affect the read performance.

To further optimize we can move the `user_active_status` table to a write optimized database like Cassandra and keep the read heavy `users` table in a relational database having B-Tree indexes. This way we can optimize both the read and write performance by using the right database for the right use case. This segregation of data based on access patterns is a key principle of vertical partitioning and can significantly improve performance by reducing contention and optimizing storage for different types of data.

---

## Drill 3: The "Bad Key" Disaster

Scenario: You are sharding a global ride-sharing dispatch system (like Uber). You need to store active trip data. You decide to shard by City_ID because queries are almost always local to a specific city (e.g., "Find drivers in New York").

Question:

What happens to your shards during New Year's Eve in New York City compared to a small town in New Zealand?

How does this impact the "free scalability" we hoped to gain?

Propose a better partitioning key strategy (mentioned in the "Hot Key" section of your notes) to mitigate this specific hotspot while keeping geospatial queries reasonably efficient.

---

## Solution

We have sharded the database for a global ride-sharing dispatch system (like Uber) by `city_id` column.

### What happens to your shards during New Year's Eve in New York City compared to a small town in New Zealand?

During new year's eve, the new york city shard will become the hot spot as there would be lots of requests there compared to a small town in New Zealand. This will lead to a situation where the shard for New York City will be overwhelmed with requests while the shard for the small town in New Zealand will be underutilized.

### How does this impact the "free scalability" we hoped to gain?

This impacts the "free scalability" as we will not be able to scale the system effectively due to the uneven distribution of traffic. The shard for New York City will become a bottleneck while the shard for the small town in New Zealand will be underutilized, leading to inefficient resource utilization and potential performance issues.

### Propose a better partitioning key strategy (mentioned in the "Hot Key" section of your notes) to mitigate this specific hotspot while keeping geospatial queries reasonably efficient.

To mitigate the hotspot issue, we can use salting in out sharding strategy. Instead of one key NYC, I will break NYC into a fixed number of buckets (e.g., 10 or 50) based on load testing.

When writing: I append a random number (0-9) to the key: NYC_0, NYC_1, etc. This spreads the write volume across 10 shards.

When reading: My application knows NYC is salted, so it sends parallel read requests to NYC_0 through NYC_9 and aggregates the results. This trades a slight read overhead (scatter-gather) for massive write scalability.

---

## Drill 4: The Resharding Migration

Scenario: You have a sharded database with 10 nodes. You need to scale to 20 nodes to handle increased load. You cannot afford any downtime.

Question:

Describe the specific "Dual-Write" sequence required to migrate users from the old shard configuration to the new one.

During the migration, where do Reads go? (Do they go to the old shard, the new shard, or both?)

When can you finally turn off the old shards?

---

## Solution

The "Dual-Write" sequence for migrating users from the old shard configuration to the new one involves the following steps:

1. **Data Migration**: First, we need to migrate the existing data from the old shards to the new shards. This can be done using a background process that copies data in batches to minimize performance impact.
2. **Dual-Write Implementation**: During the migration, we need to implement a dual-write mechanism in our application. This means that for every write operation, the application will write to both the old shard and the new shard simultaneously. This ensures that any new data is available in both configurations.
3. **Read Routing**: During the migration, reads should continue to go to the old shards to ensure consistency and avoid any potential issues with the new shards until we are confident that the new shards are fully operational and have all the necessary data.
4. **Monitoring and Validation**: We need to monitor the new shards closely for any issues and validate that the data is consistent between the old and new shards. This can involve running checksums or other validation techniques to ensure data integrity.
5. **Cutover**: Once we are confident that the new shards are fully operational and have all the necessary data, we can switch the read routing to point to the new shards. This can be done gradually to ensure a smooth transition.
6. **Decommissioning Old Shards**: After the cutover, we can continue to monitor the new shards for any issues. Once we are confident that everything is stable, we can finally turn off the old shards.

This approach allows us to migrate to the new shard configuration without any downtime, as both the old and new shards are operational during the transition period.

---

## Drill 5: The Infinite Queue

Scenario: It is Black Friday. Your e-commerce order processing service is backed by an SQS queue.

The database is running at 100% CPU (write-bound).

The queue depth is increasing by 10,000 messages per minute.

Question:

Your Junior Engineer suggests: "Let's add more consumer workers to read from the queue faster." Why is this the wrong answer? What happens to the database if you do this?

Since the database is the bottleneck, what is the correct immediate action to take to stop the bleeding ?

---

## Solution

Adding more consumer workers to read from the queue is not a good solution as all the writes from the consumers will still hit the database which is running at 100% CPU. There will be more consumers trying to write to the database, which will lead to even more contention and potentially cause the database to crash or become unresponsive. Simply put, adding more consumers will exacerbate the problem rather than solve it.

Since the database is the bottleneck, the correct immediate action to take to stop the bleeding would be to shed load by rejecting least important requests or by implementing a backpressure mechanism. This can help reduce the load on the database and allow it to catch up with the existing writes. Additionally, we can also consider scaling up the database instance temporarily to handle the increased load during peak times like Black Friday. This can provide immediate relief while we work on a more long-term solution to optimize the database performance or implement a more scalable architecture.

---

## Drill 6: The "Justin Bieber" Problem

Scenario: A celebrity starts a live video. 2 million users are watching. They are "liking" the video at a rate of 50k likes/second. You need to show the total like count on everyone's screen in near real-time.

The Constraint: If you try to write every single "like" to the database, it crashes immediately.

Question:

Design a multi-step reduction topology. Instead of writing to the DB, where do the users' phones send their "likes"?

How does the data flow from there to the final database write?

By what factor does this reduce the write volume hitting the database?

---

## Solution

The users' phones can send their "likes" to a set of broadcast nodes instead of directly writing to the database. These broadcast nodes can be distributed geographically to handle the load and reduce latency. The data flow would be as follows:

1. **Users' Phones → Broadcast Nodes**: Each user's phone sends their "like" to a nearby broadcast node. This can be done using a consistent hashing scheme to distribute the load evenly across the broadcast nodes.
2. **Broadcast Nodes → Root Processor**: The broadcast nodes aggregate the likes they receive and periodically send the aggregated counts to a root processor. The root processor is responsible for maintaining the total like count and updating it in the database.
3. **Root Processor → Database**: The root processor writes the updated like count to the database at a much lower frequency (e.g., every second or every few seconds) instead of writing every single like.

By using this multi-step reduction topology, we can significantly reduce the write volume hitting the database. Instead of writing 50k likes/second directly to the database, we can aggregate them at the broadcast nodes and only write the total count at a much lower frequency. This can reduce the write volume by a factor of 1000 or more, depending on how frequently the root processor updates the database. For example, if the root processor updates the database every second, we would only have 1 write per second instead of 50k writes per second, resulting in a reduction factor of 50,000.

---



