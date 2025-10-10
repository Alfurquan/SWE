# 📈 Scaling Writes Pattern - Cheatsheet

## 🎯 The Core Problem

Single databases/servers hit hard limits on disk I/O, CPU, and network bandwidth when write volume grows from hundreds to millions of writes per second. Unlike reads, writes can't be easily cached.

## 🔧 The Solution Progression

### Vertical Scaling & Optimization (Start Here!)

#### 🟢 Hardware Upgrades (Foundation)

Better SSDs, more RAM, faster CPUs
Modern cloud instances can handle 10K+ writes/second
Use when: Haven't exhausted single-machine limits yet
L5 Tip: Do back-of-envelope math to prove you need horizontal scaling

#### 🟡 Database Choice for Writes

Write-Heavy Options:

- Cassandra: Append-only writes (10K+ writes/sec)
- InfluxDB: Time-series optimized
- LevelDB: Log-structured, sequential writes

Trade-off: Write performance vs read performance
Use when: Current DB not optimized for write patterns

### Horizontal Scaling

#### 🔴 Horizontal Sharding

User posts → Shard by user_id hash
Geographic data → Shard by region  
Time-series → Shard by time ranges

- Key insight: Good partitioning key = even distribution
- Use when: Single DB overwhelmed, data can be logically split
- Challenge: Resharding, cross-shard queries

#### 🟣 Vertical Partitioning

```text
monolithic posts table → 
├── post_content (write-once, read-many)
├── post_metrics (high-frequency updates) 
└── post_analytics (append-only events)
```

Use when: Different data types have different access patterns
Benefit: Optimize each partition for its specific workload

### Burst Handling

#### 🔵 Write Queues (Kafka/SQS)

```text
App → Queue → Database Workers
Handles traffic spikes, smooths bursts
```

Use when: Temporary bursts, can tolerate async processing
Warning: Not a solution for sustained overload
Trade-off: Eventual consistency, complexity

#### 🟨 Load Shedding

During overload:
✅ Keep: Critical user actions, payments
❌ Drop: Analytics events, non-critical updates

Use when: Business can tolerate dropping some writes
Example: Drop location updates (new ones coming anyway)

### Write optimizations

#### 🟠 Batching
 
```shell
-- Instead of 1000 individual inserts:
INSERT INTO events VALUES (1,'click'), (2,'view'), (3,'buy')...;

-- Application-level:
buffer.push(event)
if (buffer.length >= BATCH_SIZE) sendBatch(buffer)
```

Use when: High write volume, can tolerate slight latency
Benefit: Amortizes overhead, improves throughput

#### 🔶 Hierarchical Aggregation

Million viewers → Regional aggregators → Central processor
Reduces N-to-N writes to manageable fan-out

Use when: Need shared state across millions of users
Example: Live streaming comments, real-time analytics

## 🚀 Quick Decision Tree

- Single machine limits hit? → Try better hardware first
- Wrong database for writes? → Consider write-optimized DB
- Sustained high volume? → Horizontal sharding
- Temporary bursts? → Queues + load shedding
- Lots of small writes? → Batching
- Millions need shared state? → Hierarchical aggregation

## 💡 L5 Interview Tips

- Start with Math: "Let's see... 1M users × 10 posts/day = 10M writes/day = 115 writes/sec"
- Show Trade-offs: "Sharding gives us scale but complicates cross-user queries"
- Mention Hot Keys: "What if a celebrity post gets 100K likes/second?"
- Consider Business Logic: "Can we drop some analytics during peak load?"

## 🎪 Common Interview Scenarios

- 📱 Social Media Posts: Shard by user_id, vertical partition (content vs metrics)
- 📊 Analytics Systems: Time-series DB + batching + hierarchical aggregation
- 🚗 Location Tracking: Load shedding (drop old updates) + batching
- 💬 Live Chat: Hierarchical aggregation to avoid N-to-N writes
- 🛒 E-commerce Orders: Queue for burst handling, shard by customer_id

## 🔥 Deep Dive Prep

- Resharding: Dual-write phase (write to old + new, read from new)
- Hot Keys: Split single hot key across multiple shards
- Cross-Shard Queries: Aggregate at application layer or use federated queries
- Queue Backlog: Monitor queue depth, implement backpressure

## ⚖️ Key Trade-offs Framework

Strategy → Benefit → Cost
Sharding → Horizontal scale → Complexity, cross-shard queries
Queues → Burst handling → Eventual consistency  
Batching → Efficiency → Latency
Load shedding → Availability → Data loss
Write-optimized DB → Write performance → Read performance

---
