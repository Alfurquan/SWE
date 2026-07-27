# Real-Time Ad Click Attribution System — End-to-End Detailed Explanation

---

## The Business Problem

An ad platform shows ads to users. When a user **sees** an ad (impression) and later **clicks** it, we need to:
1. **Match** the click to the original impression (attribution)
2. **Bill** the advertiser (cost per click)
3. **Compute metrics** like CTR (click-through rate) in near real-time so advertisers can monitor campaign performance

---

## The Data Flow — Big Picture

```
Users browsing websites/apps
        │
        │ see ads, click ads
        ▼
┌──────────────────┐
│  Ad Serving Layer │  (renders ads, generates impression_id)
└────────┬─────────┘
         │
         │ emits events
         ▼
┌──────────────────────────────────────────────────┐
│                    KAFKA                          │
│                                                   │
│  Topic: impressions          Topic: clicks        │
│  Partitioned by              Partitioned by       │
│  impression_id               impression_id        │
│                                                   │
│  500K events/sec             50K events/sec       │
└────────┬─────────────────────────┬────────────────┘
         │                         │
         │    Spark Structured Streaming reads both
         ▼                         ▼
┌──────────────────────────────────────────────────┐
│           SPARK STRUCTURED STREAMING              │
│                                                   │
│  Job 1: Windowed Join (impression + click)        │
│         State store: RocksDB                      │
│         Window: 24 hours                          │
│         Output: joined_events                     │
│                                                   │
│  Job 2: Continuous Aggregation                    │
│         Rolling counters per ad_id                │
│         Output: CTR, spend metrics every 10 sec   │
└────────┬─────────────────────────┬────────────────┘
         │                         │
         ▼                         ▼
┌────────────────┐      ┌──────────────────────┐
│  Raw Joined    │      │  Analytical Store     │
│  Events Store  │      │  (CTR, spend per ad)  │
│  (Cassandra)   │      │  (Redis + Columnar DB)│
└────────────────┘      └──────────────────────┘
         │                         │
         ▼                         ▼
  Billing pipeline          Advertiser dashboard
  (compute charges)         (query CTR, spend)
```

---

## Part 1: Event Generation

### Impression Event

When the ad serving layer shows an ad to a user, it generates:

```json
{
  "impression_id": "imp_abc123",
  "ad_id": "ad_456",
  "advertiser_id": "adv_789",
  "user_id": "user_001",
  "cost_per_click": 0.50,
  "event_time": "2024-01-15T10:00:00.000Z",
  "page_url": "https://example.com/article"
}
```

**`event_time`** is the timestamp when the impression actually happened on the user's device. This is set by the ad server at the moment it serves the ad.

### Click Event

When the user clicks the ad (seconds, minutes, or hours later):

```json
{
  "click_id": "clk_xyz789",
  "impression_id": "imp_abc123",
  "user_id": "user_001",
  "event_time": "2024-01-15T10:05:30.000Z"
}
```

The click carries the `impression_id` — this is how we link it back to the original impression.

### Both events are published to Kafka:

```
Impression → Kafka topic "impressions", partition = hash(impression_id)
Click      → Kafka topic "clicks",      partition = hash(impression_id)
```

**Why partition both by `impression_id`?** Because the join needs to match them. If both events for `imp_abc123` land on partition 7 in their respective topics, Spark can join them locally without shuffling data across the network. This is called **co-partitioning**.

---

## Part 2: Event Time vs Processing Time

This is critical for correctness. Two different concepts:

### Event Time

**When the event actually happened** in the real world.

```
User sees ad at 10:00:00 AM → event_time = 10:00:00
User clicks ad at 10:05:30 AM → event_time = 10:05:30
```

Event time is embedded in the event payload. It never changes. It represents **reality**.

### Processing Time

**When Spark receives and processes the event.**

```
Impression event_time = 10:00:00 AM
But due to network delay, Kafka buffering, consumer lag:
Spark processes it at 10:00:03 AM → processing_time = 10:00:03
```

Processing time can be seconds, minutes, or even hours after event time (if there's a backlog, outage recovery, etc.).

### Why This Distinction Matters

Scenario:

```
Timeline (real world):
  10:00:00  User sees ad (impression)
  10:05:30  User clicks ad (click)

Timeline (Spark processing):
  10:00:03  Spark processes impression (3 second network delay)
  10:06:00  Spark processes click (30 second delay — Kafka consumer was slow)
```

If we use **processing time** for the join window:
- Window: "join events within 24 hours of processing"
- Works in this case, but what about:

```
Outage scenario:
  10:00:00  Impression event_time
  10:05:30  Click event_time
  
  Spark goes down at 10:01, comes back at 12:00
  
  Processing times:
  12:00:05  Spark processes impression (2 hours late!)
  12:00:06  Spark processes click (2 hours late!)
  
  Real gap between events: 5 minutes 30 seconds
  Processing time gap: 1 second
```

If we used processing time, the window semantics are meaningless — events that are hours apart in reality might be processed in the same second, and events that are seconds apart might be processed hours apart.

**Solution: always use event time for business logic.** Spark Structured Streaming supports this natively:

```python
# Define the watermark on event_time
impressions_df = (
    spark.readStream
    .format("kafka")
    .option("subscribe", "impressions")
    .load()
    .selectExpr("CAST(value AS STRING)")
    .select(from_json("value", impression_schema).alias("data"))
    .select("data.*")
    .withWatermark("event_time", "2 hours")  # tolerate up to 2 hours late
)

clicks_df = (
    spark.readStream
    .format("kafka")
    .option("subscribe", "clicks")
    .load()
    .selectExpr("CAST(value AS STRING)")
    .select(from_json("value", click_schema).alias("data"))
    .select("data.*")
    .withWatermark("event_time", "2 hours")
)
```

---

## Part 3: Watermarks — Handling Late Data

### The Problem

Spark processes events in the order they arrive (processing time order). But it needs to reason about event time. The question: **how long should Spark wait for late events before closing a window?**

```
Window: 10:00 to 11:00 (event time)

Events arrive:
  10:00:05  event_time=10:15 ✓ (in window, on time)
  10:30:00  event_time=10:20 ✓ (in window, on time)
  11:05:00  event_time=10:55 ✓ (in window, arrived late but within tolerance)
  13:00:00  event_time=10:45 ✗ (in window, but arrived 2+ hours late)
```

### The Watermark

A watermark says: "I will wait up to X time for late events. After that, I consider the window complete and drop any later arrivals."

```python
.withWatermark("event_time", "2 hours")
```

This means:
- Spark tracks the maximum event_time it has seen so far
- Watermark = max_event_time - 2 hours
- Any event with event_time < watermark is considered **too late** and dropped
- State for windows older than the watermark is cleaned up

```
Example progression:

Max event_time seen: 12:00:00
Watermark: 12:00:00 - 2 hours = 10:00:00

→ Any event with event_time < 10:00:00 is dropped
→ State for windows ending before 10:00:00 is purged
→ Memory doesn't grow unbounded
```

### For Our System

```python
# Impressions: tolerate 2 hours late
impressions_df.withWatermark("event_time", "2 hours")

# Clicks: tolerate 2 hours late  
clicks_df.withWatermark("event_time", "2 hours")
```

Why 2 hours? It's a business/operational trade-off:
- Too short (5 minutes): miss legitimate late events (mobile user on bad connection)
- Too long (12 hours): state store grows huge, memory pressure
- 2 hours: catches 99.9%+ of events, manageable state size

---

## Part 4: The Windowed Join (Job 1)

### What We're Doing

Match each click to its original impression using `impression_id`, within a 24-hour event-time window.

```python
# Stream-stream join with event time constraint
joined_df = clicks_df.join(
    impressions_df,
    on=(
        clicks_df.impression_id == impressions_df.impression_id
    ),
    how="inner"
).where(
    # Click must happen within 24 hours after impression
    (clicks_df.event_time >= impressions_df.event_time) &
    (clicks_df.event_time <= impressions_df.event_time + expr("INTERVAL 24 HOURS"))
)
```

### How Spark Executes This

```
Kafka "impressions" topic              Kafka "clicks" topic
  Partition 0 ──┐                       Partition 0 ──┐
  Partition 1 ──┤                       Partition 1 ──┤
  Partition 2 ──┤                       Partition 2 ──┤
  ...           │                       ...           │
                ▼                                     ▼
         ┌─────────────────────────────────────────────────┐
         │              Spark Executor (Task)               │
         │                                                  │
         │  Reads partition 0 from BOTH topics              │
         │  (co-partitioned by impression_id)               │
         │                                                  │
         │  ┌──────────────────────┐                        │
         │  │  RocksDB State Store │                        │
         │  │                      │                        │
         │  │  Stores impressions  │                        │
         │  │  keyed by            │                        │
         │  │  impression_id       │                        │
         │  │  with event_time     │                        │
         │  │                      │                        │
         │  │  Retention: 24h +    │                        │
         │  │  2h watermark        │                        │
         │  └──────────────────────┘                        │
         │                                                  │
         │  When impression arrives:                        │
         │    → Store in RocksDB: {imp_abc123: full_event}  │
         │                                                  │
         │  When click arrives:                             │
         │    → Lookup impression_id in RocksDB             │
         │    → Found? → Emit joined event                  │
         │    → Not found? → Store click, wait for          │
         │      impression (it might arrive late)           │
         │                                                  │
         │  Watermark advances:                             │
         │    → Purge impressions older than 26 hours       │
         │      (24h window + 2h watermark)                 │
         └─────────────────────────────────────────────────┘
```

### The Joined Output

```json
{
  "impression_id": "imp_abc123",
  "click_id": "clk_xyz789",
  "ad_id": "ad_456",
  "advertiser_id": "adv_789",
  "user_id": "user_001",
  "impression_time": "2024-01-15T10:00:00.000Z",
  "click_time": "2024-01-15T10:05:30.000Z",
  "cost_per_click": 0.50,
  "time_to_click_seconds": 330
}
```

This joined event is written to:
1. **Cassandra** (raw joined events — for billing pipeline, auditing, debugging)
2. **Kafka topic "attributed_clicks"** (for downstream aggregation)

---

## Part 5: Continuous Aggregation (Job 2)

Job 2 reads from **two sources**, one of which is Job 1's output.

### What Job 2 Needs to Compute

```
CTR = clicks / impressions

For ad_456 in the last hour:
  impressions: 50,000
  clicks: 2,500
  CTR: 2,500 / 50,000 = 5%
```

To compute this, Job 2 needs two counts:
1. **Total impressions** for an ad
2. **Total clicks** (attributed/matched clicks) for an ad

These come from **two different sources**.

### What We're Doing

Compute rolling CTR and spend per ad, updated every ~10 seconds, without waiting for any window to close.

This is a **separate Spark Structured Streaming job** that reads from **two sources**:

### Source 1: Impression Counts — Reads Directly from Kafka

```
Kafka topic: "impressions"
    │
    ▼
Job 2 reads every impression event
    │
    ▼
Groups by ad_id, counts them in a sliding window
```

**Why read raw impressions and not Job 1's output?** Because Job 1 only outputs **matched** events (impression + click pairs). Most impressions (~95%) never get clicked. If we only counted impressions from Job 1's output, we'd miss those unclicked impressions and our CTR denominator would be wrong.

### Source 2: Click Counts — Reads from Job 1's Output

```
Job 1 output → Kafka topic: "attributed_clicks"
    │
    ▼
Job 2 reads every attributed click event
    │
    ▼
Groups by ad_id, counts them + sums cost_per_click
```

**Why read from Job 1 and not raw clicks?** Because a raw click is meaningless until it's matched to an impression. Job 1 does the matching — it confirms "this click is legitimate, it corresponds to a real impression within 24 hours." Only matched clicks should count toward CTR and billing.

### The Code

```python
# Source 1: Raw impressions (from Kafka)
# Count impressions per ad_id in a sliding window
impression_counts = (
    impressions_df
    .withWatermark("event_time", "30 seconds")
    .groupBy(
        window("event_time", "1 hour", "10 seconds"),  # 1-hour window, slides every 10 sec
        "ad_id"
    )
    .count()
    .withColumnRenamed("count", "impression_count")
)

# Source 2: Attributed clicks (from Kafka topic "attributed_clicks")
# Count clicks and sum spend per ad_id
click_aggregates = (
    attributed_clicks_df
    .withWatermark("click_time", "30 seconds")
    .groupBy(
        window("click_time", "1 hour", "10 seconds"),
        "ad_id"
    )
    .agg(
        count("*").alias("click_count"),
        sum("cost_per_click").alias("total_spend")
    )
)
```

### How the Two Aggregations Merge

They're independent counters that get **merged at write time**:

```python
# When writing to Redis, merge them
def write_to_redis(batch_df, batch_id):
    for row in batch_df.collect():
        redis.hset(
            f"ctr:{row.ad_id}:{row.window.start}",
            mapping={
                "impressions": row.impression_count,
                "clicks": row.click_count,
                "ctr": row.click_count / row.impression_count,
                "spend": row.total_spend
            }
        )
        redis.expire(f"ctr:{row.ad_id}:{row.window.start}", 86400)  # 24h TTL
```

### The Full Data Flow for Job 2

```
                    Kafka "impressions"
                     │            │
                     │            │
                     ▼            ▼
                   Job 1        Job 2 (impression counts)
                     │
                     ▼
              Kafka "attributed_clicks"
                     │
                     ▼
                   Job 2 (click counts + spend)
                     │
                     ▼
                   Redis (merged: CTR = clicks/impressions)
```

### Why This Meets the 30-Second Requirement

```
Event happens (event_time)
    │
    │ ~1-3 seconds (Kafka ingestion + network)
    ▼
Spark reads from Kafka
    │
    │ trigger every 10 seconds
    ▼
Spark emits updated aggregation
    │
    │ ~1-2 seconds (write to Redis)
    ▼
Dashboard queries Redis → sees updated CTR

Total end-to-end: ~15-20 seconds. Well within 30-second SLA.
```

---

## Job 1's 24-Hour Window vs Job 2's 1-Hour Window

These are **completely unrelated windows** solving different problems.

### Job 1's 24-Hour Window: "How long to wait for a click"

This is a **join window** — it defines the maximum time gap between an impression and its corresponding click.

```
Impression at 10:00 AM Monday
Click can arrive anytime up to 10:00 AM Tuesday (24 hours later)

Job 1 keeps the impression in RocksDB for 24 hours,
waiting for a matching click to show up.
```

This is a **business rule**: "we only attribute a click to an impression if it happens within 24 hours." It has nothing to do with aggregation.

### Job 2's 1-Hour Sliding Window: "What time range to aggregate over"

This is an **aggregation window** — it defines the time range for computing CTR.

```
"How many impressions and clicks did ad_456 get in the last hour?"

Window: 10:00 - 11:00  → impressions: 50K, clicks: 2.5K, CTR: 5%
Window: 10:00:10 - 11:00:10 → (updated counts, slides every 10 sec)
```

This could be 1 hour, 15 minutes, 1 day — whatever the dashboard needs. It's purely about **how you slice the metrics for display**.

### They're Independent

```
Job 1 window = "match timeout" (how long to wait for a partner event)
Job 2 window = "reporting bucket" (what time range the dashboard shows)

You could change Job 2 to a 15-minute window — Job 1 wouldn't change.
You could change Job 1 to a 48-hour attribution window — Job 2 wouldn't change.
```

---

## Part 6: The Query Path

### `get_ctr(ad_id, time_range)`

```
Advertiser dashboard → API server
    │
    ▼
Redis: HGET "ctr:ad_456:2024-01-15T10:00"
    │
    ▼
Returns: {impressions: 50000, clicks: 2500, ctr: 0.05, spend: $1250}

Single key lookup. Sub-millisecond. No scanning.
```

### `get_spend(advertiser_id, time_range)`

```
Advertiser has multiple ads. Need total spend across all ads.
    │
    ▼
Option A: Redis stores a per-advertiser rollup too (updated by aggregation job)
Option B: Query columnar DB (like ClickHouse) for ad-hoc time-range queries

For the dashboard's default view: Redis (pre-computed)
For custom date ranges / drill-downs: ClickHouse (columnar scan)
```

---

## Part 7: Handling Edge Cases

### Late Events (click arrives after watermark)

```
Watermark has advanced past the impression's event_time.
State for that impression has been purged from RocksDB.

Click arrives → no matching impression in state → DROPPED

This click is written to a "late_events" Kafka topic.
A batch job runs daily, reads late_events + raw impressions from 
Cassandra, performs offline reconciliation.
Billing adjustments made in next billing cycle.
```

### Duplicate Events

```
Click event arrives twice (network retry):

Spark's join state already recorded this click for imp_abc123.
But Spark doesn't inherently deduplicate.

Solution: dropDuplicates on click_id within the watermark window.

clicks_df = clicks_df.dropDuplicates(["click_id"])
```

Spark Structured Streaming's `dropDuplicates` maintains a state store of seen IDs within the watermark window. After the watermark advances past an event's time, its dedup entry is cleaned up.

### Unmatched Impressions (user saw ad but never clicked)

```
Impression sits in RocksDB state store for 24h + 2h watermark.
No click arrives. Watermark advances past it.
Impression state is purged.

This impression counts toward impression_count in the aggregation 
(Job 2 reads directly from the impressions topic).
It just never gets a matching click → CTR reflects this naturally.
```

---

## Part 8: Crash Recovery

### Spark Checkpointing

```python
query = joined_df.writeStream \
    .format("kafka") \
    .option("topic", "attributed_clicks") \
    .option("checkpointLocation", "hdfs:///checkpoints/attribution_join") \
    .start()
```

What's checkpointed:
1. **Kafka offsets**: which messages have been consumed from each partition
2. **State store snapshots**: RocksDB state (buffered impressions/clicks)
3. **Watermark position**: current watermark value

### Recovery scenario:

```
Spark crashes at processing_time = 12:00:00
Last checkpoint at processing_time = 11:59:50

Recovery:
1. Spark restarts
2. Reads last checkpoint from HDFS
3. Restores RocksDB state from checkpoint
4. Reads Kafka from last committed offset (11:59:50)
5. Reprocesses ~10 seconds of events
6. Back to normal

Data loss: ZERO (Kafka retains events, state is checkpointed)
Duplicate processing: possible for ~10 seconds of events
→ Handled by idempotent writes (Redis SET is idempotent) 
  and downstream dedup
```

---

## Part 9: Complete Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                     │
│                                                                      │
│  Ad Server                                                           │
│  ├── impression event ──→ Kafka [impressions] (by impression_id)     │
│  └── click event ──────→ Kafka [clicks] (by impression_id)           │
│                                                                      │
│  Spark Job 1: WINDOWED JOIN                                          │
│  ├── Reads both topics (co-partitioned)                              │
│  ├── Stores impressions in RocksDB (24h + 2h watermark)              │
│  ├── Joins click to impression by impression_id                      │
│  ├── Output: joined events → Cassandra (raw) + Kafka [attributed]    │
│  └── Late events → Kafka [late_events] (batch reconciliation)        │
│                                                                      │
│  Spark Job 2: CONTINUOUS AGGREGATION                                 │
│  ├── Reads Kafka [impressions] → counts per ad_id (sliding window)   │
│  ├── Reads Kafka [attributed] → counts + spend per ad_id             │
│  ├── Emits updated metrics every 10 seconds                          │
│  └── Writes to Redis (dashboard) + ClickHouse (ad-hoc queries)       │
│                                                                      │
│  QUERY PATH                                                          │
│  ├── get_ctr(ad_id) → Redis (sub-ms, pre-computed)                   │
│  ├── get_spend(advertiser_id) → Redis (rollup) or ClickHouse         │
│  └── Billing pipeline → reads Cassandra (joined events)              │
│                                                                      │
│  FAILURE HANDLING                                                    │
│  ├── Spark crash → checkpoint recovery (zero data loss)              │
│  ├── Late events → dead letter topic + batch reconciliation          │
│  ├── Duplicates → dropDuplicates(click_id) + idempotent writes       │
│  └── Kafka unavailable → producers buffer locally, retry             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 10: Key Decisions Summary

| Decision | Choice | Why |
|----------|--------|-----|
| Ingestion | Kafka | Durable, partitioned, handles 550K events/sec, decouples producers from consumers |
| Partition key | impression_id | Enables co-partitioned join without shuffle |
| Stream processor | Spark Structured Streaming | Exactly-once with checkpointing, native event-time support |
| State store | RocksDB | LSM-based, handles 500K writes/sec for buffering impressions |
| Join type | Stream-stream interval join | Both streams are unbounded, event-time windowed |
| Time semantics | Event time + watermarks | Correct results despite processing delays and out-of-order events |
| Aggregation | Continuous (sliding window) | Meets 30-second freshness SLA without waiting for window close |
| Dashboard store | Redis | Sub-ms reads for pre-computed metrics |
| Analytical store | ClickHouse (columnar) | Ad-hoc queries across time ranges |
| Raw events | Cassandra (LSM) | High write throughput for append-only joined events |
| Late events | Dead letter + batch reconciliation | Business rule: 24h attribution window, anything beyond is reconciled offline |
