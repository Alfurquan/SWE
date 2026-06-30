# Metrics ingestion syste

## Phase 1: Clarification & Scope (Minutes 0–5)

Candidate: "Before I draw any boxes, I want to lock down the exact constraints we are designing for.

Scale: We have 10,000 servers, each emitting 100 metrics every 10 seconds. That means our ingestion API must handle a sustained load of 100,000 requests per second (10k * 100 / 10).

Read vs. Write Ratio: This is incredibly write-heavy (99% writes). Reads are infrequent but scan massive time ranges (e.g., dashboard loads).

Durability vs. Availability: Because this is a telemetry system and not a financial ledger, we favor high availability and massive throughput over strict 100% durability. Losing 0.01% of CPU data during a spike is acceptable."

###Phase 2: The Data Model (Minutes 5–10)

Candidate: "The fundamental payload for a single metric data point will look like this:
```json
{ "timestamp": 1717332000, "metric_name": "cpu_utilization", "server_id": "srv-848", "value": 85.5 }
```

Because our reads are always time-bound (e.g., 'Show me CPU for the last hour'), the storage engine we choose must inherently index and cluster data physically by time to avoid full table scans."

## Phase 3: High-Level Architecture & Deep Dives (Minutes 10–35)
Candidate: "Let's trace a metric from the server to the dashboard.

1. The Ingestion Layer (API & Message Broker)
If our API nodes try to write 100,000 QPS synchronously to a database, any minor disk latency will cause the API node's memory to fill up with waiting connections, leading to a cascading crash.

The Solution: I will put a Kafka cluster directly behind a stateless ingestion API. Kafka acts as an elastic buffer, writing the payloads to an append-only commit log on disk with incredibly low latency.

The L5 Trade-off (Throughput): To maximize throughput, I will configure the API producers with acks=1. We trade the absolute durability of waiting for full cluster replication in exchange for surviving massive traffic spikes.

The L5 Trade-off (Partitioning): I will explicitly not partition the Kafka topic by metric_name or server_id, as that creates data skew (hot spots). Since our downstream database will sort the data by the timestamp inside the payload anyway, strict queue ordering doesn't matter. I will use a Round-Robin strategy to ensure perfectly even load distribution across all Kafka brokers.

2. The Storage Engine (LSM-Tree)
Standard B-Tree databases will choke on 100,000 random inserts per second due to heavy disk I/O.

The Solution: I will use a Time-Series Database (like InfluxDB or Cassandra) built on an LSM-Tree architecture. Incoming writes hit an in-memory MemTable and are then flushed sequentially to disk as immutable SSTables. This guarantees fast sequential disk I/O.

The L5 Trade-off (Sharding): To distribute this data across a cluster, I will use a composite partition key of (metric_name, time_bucket_1hr). This prevents the 'current time' from melting a single node, and it prevents a single massive metric from overwhelming a node. When a dashboard queries a 4-hour window, the query router calculates exactly which 4 nodes hold the data and fetches it directly, avoiding a cluster-wide scatter-gather operation.

3. The Aggregation & Read Layer
Querying raw 10-second data over a 30-day window requires scanning billions of rows, which will time out the dashboard. We must downsample.

The Solution: I will deploy a stream processor (like Flink) to read from Kafka, calculate 1-minute and 1-hour rollups, and write the summaries directly to the database.

The L5 Trade-off (Percentiles & Late Data): The prompt requires P99 calculations. Because percentiles are non-associative, we cannot simply average them over time. Our Flink jobs will compute data sketches (T-Digests) instead of flat numbers, allowing the dashboard to accurately merge billions of points into a P99 in milliseconds. Furthermore, if a server loses connection and dumps 5 minutes of late data, Flink will capture this via a 'late-data side output' and upsert it directly into the time-series database. During the next background LSM compaction cycle, the database will seamlessly merge the late data into the correct historical block."

## Phase 4: Bottlenecks & Edge Cases (Minutes 35–45)
Candidate: "To wrap up, the biggest operational risk here is Write Amplification in the storage layer. As the LSM-tree creates thousands of SSTables, read performance degrades.

To mitigate this, I would heavily tune the database's background Compaction strategy. For telemetry data, I would specifically implement a Time-Window Compaction strategy, which aggressively drops old data chunks that fall outside our retention policy (e.g., dropping raw data older than 7 days) without needing to execute heavy DELETE operations across the disk."