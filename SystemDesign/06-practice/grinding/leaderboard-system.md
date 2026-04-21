# Leaderboard System

---

## 1. High-Level Architecture Components

- **API Gateway:** Ingests scores and routes read requests.
- **Kafka (Source of Truth):** A highly durable, partitioned, append-only commit log handling the massive write throughput.
- **Relational Database (Cold Storage):** A PostgreSQL/MySQL cluster consuming from Kafka to maintain a durable, long-term ledger of all points ever scored.
- **Sharded Redis Cluster (Fast Path):** Partitioned by `user_id` across multiple nodes. Stores the entire 10-million user leaderboard in Sorted Sets (ZSETs) for $O(1)$ point lookups and $O(\log N)$ rank calculations.
- **Global Top 100 Redis Node (Materialized View):** A single, isolated node that only holds the top 100 players, optimized purely for massive read concurrency.

---

## 2. The End-to-End Flow

### The Write Path (Ingestion & Idempotency)

1. Client sends `POST /score` with `Idempotency-Key: req-777` (a UUID).
2. API Gateway drops the event onto Kafka and immediately returns `202 Accepted`.
3. The "Fast-View Consumer" reads the Kafka offset (e.g., Offset 42).
4. The Consumer executes an atomic Lua script on the user's Redis Shard.
5. **Two-Tiered Idempotency Check:** The script checks if `req-777` exists (to block client network retries) **AND** checks if the stored Kafka offset is $\ge 42$ (to block consumer crash replays).
6. If safe, the script executes `ZINCRBY`, updates the partition offset, and sets the UUID with a 10-minute TTL.

### The Aggregation Path (Computing the Top 100)

1. Every second, the 5 Redis Shards publish their local Top 100 to a secondary Kafka topic.
2. A Stream Aggregator consumes these, performs an in-memory merge-sort, and writes the absolute Top 100 to the isolated Global Redis Node.

### The Read Path

- **Global Top 100:** Hits the single Global Redis Node with `ZREVRANGE 0 99` ($O(1)$).
- **Personal Rank:** Uses a **Scatter-Gather** pattern. Hits the user's specific shard for their absolute score via `ZSCORE`, then scatters a `ZCOUNT` to all shards to find how many users have a higher score, sums the results, and returns the global rank.

---

## 3. Follow-Up: Asynchronous Replication Data Loss

### The Scenario

Redis uses asynchronous replication. Consumer A safely updates the Redis Leader with User123's new score. The Leader acknowledges the write and the Consumer commits Offset 42 back to Kafka. Milliseconds later, the Redis Leader suffers a hardware failure before it can replicate Offset 42 to its Follower. Redis Sentinel promotes the Follower to Leader.

**The system has now permanently lost User123's points in the cache.**

### The Answer: State Reconciliation

Because we architected the system using **CQRS** (Command Query Responsibility Segregation) with Kafka as the immutable commit log, a data loss in Redis is **not catastrophic**; Redis is merely a materialized view. We can heal it.

1. **Detection:** When the new Redis Leader boots up, it still contains the offset state from the exact moment before the crash (e.g., it thinks the last processed offset is 41).
2. **The Reconciliation Worker:** You introduce a background reconciliation process (or build it into consumer startup). This process checks the Kafka consumer group's committed offset (Offset 42) against the offset stored inside the new Redis Leader (Offset 41).
3. **Healing (Rewind and Replay):** Detecting the divergence, the Kafka consumer simply rewinds its reading pointer back to Offset 41.
4. **Idempotency Saves the Day:** It replays Offset 41. The Lua script sees Redis is already at Offset 41, so it safely ignores it. It replays Offset 42. The Lua script sees Redis needs this, executes the `ZINCRBY`, and restores the lost score.

> **Interviewer Note:** You can also mention the Redis `WAIT` command, which forces synchronous replication (blocking until replicas acknowledge). However, you should immediately dismiss it for this specific system, as it drastically increases write latency and defeats the purpose of using an in-memory store for high-throughput gaming telemetry.