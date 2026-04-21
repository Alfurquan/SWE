# Ad Click Tracking and Billing System

## Functional Requirements

- When a user clicks on an ad, the system should record the click
- The system should generate a bill (e.g., monthly) for the advertisers depending on the number of clicks for the ad
- Advertisers should be able to see ad click metrics in near real-time on a dashboard

> We can discuss with the interviewer and bring more requirements in scope. For billing, we assumed monthly — this can also be discussed with the interviewer.

## Non-Functional Requirements

- **Scale:** ~10K ad clicks per second
- **Latency:** Metrics for ad clicks should be near real-time with latency < 200 ms
- **Consistency:** Eventual consistency is acceptable — counts can lag for a few seconds, but the system should be highly available
- **Durability:** No ad clicks should be lost; all clicks must be durable in the database
- **Read/Write Ratio:** ~1:10 — the system should be optimized for writes
- **Billing Accuracy:** No over-billing or under-billing should happen for advertisers

> We can discuss with the interviewer and bring other non-functional requirements in scope (e.g., fraud detection).

---

## Data Model

We define the following data models. We can always come back later and refine them.

### Ad

| Field              | Type   |
| ------------------ | ------ |
| `ad_id`            | string |
| `ad_brand`         | string |
| `ad_content`       | string |
| `publisher_id`     | string |
| `ad_url`           | string |
| `ad_cost_per_click`| float  |

### Click

| Field       | Type      |
| ----------- | --------- |
| `click_id`  | string    |
| `ad_id`     | string    |
| `user_id`   | string    |
| `timestamp` | datetime  |

### Bill

| Field           | Type    |
| --------------- | ------- |
| `bill_id`       | string  |
| `advertiser_id` | string  |
| `month`         | integer |
| `year`          | integer |
| `total_clicks`  | integer |
| `total_amount`  | float   |

### Analytics

| Field              | Type    |
| ------------------ | ------- |
| `ad_id`            | string  |
| `publisher_id`     | string  |
| `total_clicks`     | integer |
| `clicks_per_minute`| integer |
| `clicks_per_hour`  | integer |
| `clicks_per_day`   | integer |

---

## Database Choice

We can use a **combination of databases** to meet the requirements:

- **Relational DB (MySQL / PostgreSQL):** For storing ad, billing, and click data. Works well for structured data with strong ACID properties — important for billing accuracy.

- **NoSQL / Time-Series DB (Cassandra / InfluxDB):** For real-time analytics. Cassandra is optimized for high write throughput using a log-structured storage engine, which is ideal for our 1:10 read-to-write ratio. We can use Cassandra to store click data and generate real-time metrics for the dashboard.

> Database choice can always be discussed and refined with the interviewer based on requirements and constraints.

---

## API Design

### Record Click API

- **Endpoint:** `POST /click`
- **Request Body:**

```json
{
  "ad_id": "string",
  "user_id": "string",
  "publisher_id": "string",
  "timestamp": "ISO8601 string"
}
```

- **Response:** `201 Created` on success

### Get Metrics API

- **Endpoint:** `GET /metrics?ad_id={ad_id}&publisher_id={publisher_id}`
- **Request Body:** None
- **Response:**

```json
{
  "ad_id": "string",
  "publisher_id": "string",
  "total_clicks": "integer",
  "clicks_per_minute": "integer",
  "clicks_per_hour": "integer",
  "clicks_per_day": "integer"
}
```

### Get Bill API

- **Endpoint:** `GET /bill?advertiser_id={advertiser_id}&month={month}&year={year}`
- **Request Body:** None
- **Response:**

```json
{
  "bill_id": "string",
  "advertiser_id": "string",
  "month": "integer",
  "year": "integer",
  "total_clicks": "integer",
  "total_amount": "float"
}
```

---

## High Level Architecture

### Why Kafka?

We use **Kafka** as the message broker for ingesting click events:

- **Append-only commit log:** With ~10K ad click events/sec, Kafka's append-only mechanism handles this write volume efficiently.
- **At-least-once semantics:** Ensures no click events are lost.
- **Durability:** Replication mechanism provides strong durability guarantees.

### Kafka Partitioning Strategy

- Multiple partitions on the `ad_clicks` topic allow **horizontal scaling** with parallel consumers.
- **Partition key:** Using `ad_id` ensures ordering per ad, but popular ads can cause **hot partitions**.
- **Salted partition key** (`ad_id + random_salt`): Distributes events more evenly across partitions, avoiding hot spots.
- **Trade-off:** We lose strict per-ad ordering, but a distributed processing framework like **Flink** can handle out-of-order events.

> **Back-of-the-envelope:** 10K clicks/sec × 100 bytes/click = ~1 MB/s — well within Kafka's capabilities. 10–20 partitions should suffice for good parallelism.

---

## Detailed Flows

### 1. Ingestion Flow (The Entry Point)

1. **Request Initiation:** User clicks an ad. The frontend sends `POST /click` with a client-generated `click_id` (UUID), `ad_id`, `user_id`, `publisher_id`, and `timestamp`.

2. **Stateless Validation & Fraud Check:** The API server performs basic schema validation.

3. **The Redis Shield:** Executes `SETNX click:<user_id>:<ad_id> "1" EX 60`.
   - Returns `0` → request dropped as duplicate/bot-click.
   - Returns `1` → proceeds.
   - This prevents click-spam from hitting expensive downstream processors.

4. **Buffering:** The API server produces a message to the Kafka topic `raw_clicks` and returns `202 Accepted` to the client.

5. **Partitioning:** Uses `ad_id + random_salt` as the partition key to avoid hot partitions.

### 2. Processing & Aggregation Flow (The Brain)

A distributed processing cluster (e.g., **Apache Flink**) consumes the `raw_clicks` topic and splits logic into two parallel sinks:

#### Path A: The Fast Path (Real-Time Metrics)

- Flink performs **windowed aggregations** (e.g., 1-minute sliding windows) to calculate `total_clicks` per `ad_id` and `publisher_id`.
- Results are written to **Cassandra**, which handles high-frequency increments and upserts better than relational databases.

#### Path B: The Accurate Path (Billing)

- **Price Capture:** For every click, Flink enriches the record with the current `ad_cost_per_click`. This "stamps" the price at click time, protecting advertisers if prices change later.
- **Micro-Batching:** Flink aggregates spend in 10-minute **Tumbling Windows** to avoid overwhelming the billing database.
- **PostgreSQL Sink:** Every 10 minutes, Flink writes one subtotal record per advertiser (e.g., "Advertiser X spent $45.00 in this 10-minute window").

### 3. Metrics Generation Flow (The Dashboard)

1. **Query:** The advertiser's dashboard calls `GET /metrics?ad_id={ad_id}`.
2. **Retrieval:** The API server queries Cassandra. Since Flink has already done the heavy lifting of counting, the database performs a simple **point lookup**.
3. **Latency:** Pre-aggregated data in Cassandra ensures dashboard updates in **< 200ms**.

### 4. Billing Flow (The Ledger)

1. **Scheduled Finalization:** At the end of the billing cycle (e.g., daily or monthly), a lightweight scheduled job runs.
2. **Lightweight Aggregation:** Instead of querying billions of raw clicks, the job sums the 10-minute micro-batch records in PostgreSQL.
   - Even at high scale, there are only ~4,320 micro-batch rows per advertiser per month — trivial for a relational database.
3. **Invoice Generation:** The total is stored in the `Bill` table, and the advertiser is notified.
4. **Audit Trail:** If an advertiser disputes a bill, we query **Cold Storage** (S3/ADLS Gen2) where a separate Kafka consumer has been dumping every raw click as a backup source of truth.

---

## Deep dives (Partitioning)

### The Time-Series Hotspot (Range Partitioning)

**The Scenario:** In our Ad Click system, you need to store the aggregated metrics in Cassandra. A junior engineer suggests: "Since the dashboard queries by time (e.g., 'Show me clicks in the last 10 minutes'), we should partition the database by the timestamp using Key-Range partitioning."

**The Question:** Why is this a catastrophic idea for our write-heavy system, and what exactly will happen to our database cluster at 12:00 PM?

**The Follow-Up:** How would you design the partition key to support fast time-based reads without destroying your write performance?

### Answer

If we partition our database by timestamp using key-range partitioning, it will be a bad idea for our write-heavy system. Let's say we do it and we have two partitions — for example, `p0` and `p1`. All the click events for timestamps between 12 AM to 12 PM go to `p0`, and the remaining go to `p1`.

Since our system is write-heavy and we have partitioned by timestamp, all the click events that happen between 12 AM to 12 PM will go to `p0` and all the click events that happen between 12 PM to 12 AM will go to `p1`. This means that at 12 PM, there will be a huge spike in writes to `p1` as all the click events that happen after 12 PM will go to `p1`. This will lead to a **hotspot** in `p1` and can cause performance degradation and even downtime for our system. Also, at any given time, only one partition will be receiving all the writes, which can lead to resource contention and further degrade performance.

To design the partition key, we can partition by a **hash of `ad_id`**. Further, in each partition, we can store the click events sorted by timestamp. This way, we can achieve a good distribution of writes across all partitions while still allowing for efficient time-based reads. When we need to query for clicks in the last 10 minutes, we can simply query all partitions and filter the results based on the timestamp. This approach avoids hotspots and ensures that our write performance remains stable even during peak times.

### Learning

#### 1. The Problem: The "Scatter-Gather" Trap

When we choose to partition a database by `ad_id`, we are making a bet. We are betting that most of our queries will ask for one specific ad.

**The Trade-off:**

- **The Win (Write & Single Read):** If you want to record a click for `ad_123` or read the count for `ad_123`, the system knows exactly which node to go to. It's ultra-fast ($O(1)$).
- **The Loss (The "All My Ads" Query):** Imagine an advertiser like Nike. They have 5,000 different ads running. If they open their dashboard and want to see the "Total Clicks for all Nike Ads," the database has a problem.
  - Since the data is partitioned by `ad_id`, Nike's 5,000 ads are scattered across all 50 nodes in your cluster.
  - The API has to "Scatter" the query to every single node, wait for all 50 to respond, and then "Gather" (sum) the results.

> **The L5 Insight:** If just one of those 50 nodes is having a "bad day" (slow disk, garbage collection), the entire dashboard feels slow to the user. This is called the **Tail Latency** problem.

#### 2. The Solution: Flink as the "Pre-Aggregator"

This is where Flink enters the architectural flow. Instead of making the database do the "math" (summing up numbers) every time a user hits "Refresh" on their dashboard, we do the math while the data is moving.

Think of Flink as a **filter and a calculator** sitting between Kafka and the Database.

**How it relates to Partitioning:**

Flink allows us to create multiple views of the same data, each partitioned optimally for the query it serves.

| Query Type                                  | Partition Strategy           | Database Table         |
| ------------------------------------------- | ---------------------------- | ---------------------- |
| "How is Ad #123 doing?"                     | Partition by `ad_id`         | `clicks_by_ad`         |
| "How is Nike (Advertiser A) doing overall?" | Partition by `advertiser_id` | `clicks_by_advertiser` |

**The Flow:**

1. **Kafka:** Receives a click for `ad_123` (owned by Nike).
2. **Flink:** Receives that click. It doesn't just pass it through.
   - It updates its internal memory for `ad_123`: `Count = Count + 1`.
   - Simultaneously, it updates its memory for Nike: `Total_Advertiser_Spend = Total_Advertiser_Spend + $0.50`.
3. **The Database Write:**
   - Flink writes the updated `ad_123` count to the `clicks_by_ad` table (Partitioned by `ad_id`).
   - Flink writes the updated Nike total to a separate `clicks_by_advertiser` table (Partitioned by `advertiser_id`).

#### 3. The Result: No More Trade-off

Now, when the Nike executive opens the dashboard:

- The API does **not** scatter-gather across 5,000 ads.
- Instead, it does a **Single Point Lookup** on the `clicks_by_advertiser` table using the key `Nike`.
- It hits one node, gets one row, and returns in **10ms**.

> The tradeoff you made was **"Write Volume"**: You are writing the data twice (once for the ad view, once for the advertiser view) to make the Read Performance perfect. In system design, we almost always trade extra disk space/writes for faster reads on the dashboard.

### Scenario 2: The "Super Bowl" Viral Hit

The Context:
We are using Hash Partitioning on ad_id to distribute clicks across our Kafka partitions and our Cassandra cluster. Under normal conditions, this works perfectly—each node handles roughly the same amount of traffic.

#### The Problem:
It is Super Bowl Sunday. A famous soda brand releases a 30-second ad with a massive "Scan this QR code to win $1 Million" CTA.

Total system traffic: 100,000 clicks/sec.

The Viral Ad: 50,000 clicks/sec (50% of your total traffic) belong to this one single ad_id.

Because hash(viral_ad_id) % total_partitions always points to the same number, all 50,000 requests per second are hitting one single Kafka partition and one single database node. That node’s CPU is at 100%, disk I/O is maxed out, and it’s about to crash, while the other 49 nodes in your cluster are sitting idle.

#### The Questions for You:

The Fix: How do you alter your partitioning strategy (specifically for the write path) to "break up" that massive traffic spike so it spreads across multiple nodes?

The Read Complication: Once you've "shattered" that single ad_id into multiple sub-partitions to save your database, how does your Flink Aggregator or your Dashboard API find all the pieces to give the advertiser an accurate total count?

### Answer

To break the massive traffic spike, we would add a random salt to the ad_id, so now when we do the hash of ad_id + random salt, it goes to different partitions instead of the single one. This helps distribute the traffic across different partitions and prevents a single partition from getting overwhelmed with lots of traffic.

The tradeoff here would be read complication. Since we have shattered the single ad_id into multiple sub-partitions, the dashboard or the flink aggregator would now have to gather the values from all the partitions and then compute the count for the ad_id. This would increase the read latency and make it more complex to retrieve the data, but it would ensure that our system remains available and responsive even during traffic spikes. To mitigate the read complication, flink can do the global sum of the counts for the ad_id across all partitions and store it in a separate table that is optimized for reads, so that the dashboard can query that table directly without having to gather data from multiple partitions.

### More refinements

1. Selective Salting (The Efficiency Play)
In a real system, you don't want to salt every ad. If you add a random salt (e.g., 1-10) to every single ad_id, you increase the complexity for all ads.

The Pro Move: You only apply salting to "Hot Keys." You can keep a list of "Top 100 Viral Ads" in a cache (like Redis). If an ad_id is in that list, the API adds a salt. If not, it uses the raw ad_id. This keeps the system efficient for the 99% of ads that aren't viral.

2. Flink as the "De-Salter"
You mentioned Flink storing data in a separate table. Let's look at the "Physical Flow" of how Flink handles this:

The Shatter: The API writes ad_123_salt1, ad_123_salt2, etc., into Kafka.

Local Aggregation: Flink workers consume these salted keys and sum them up locally.

The Global Merge: Flink then performs a second "Group By" on the original ad_id (stripping the salt).

The Clean Write: Flink writes one single row for ad_123 into the database.

---

### Scenario 3: The "Secondary Index" Dilemma

#### The Context:
Our Ad Database is partitioned by ad_id. This is great for looking up an ad's name or URL.
But now, we need to build a Publisher Portal. A publisher (like The New York Times) logs in and wants to see: "Which ads are currently running on my site?"

#### The Problem:
Our query is now SELECT * FROM ads WHERE publisher_id = 'NYTimes'.
Since our data is partitioned by ad_id, the records for the NYTimes are scattered across every single node in the cluster.

The Questions for You:

If we don't do anything, what happens when we run that query? (Hint: It’s the "Scatter-Gather" we talked about).

According to DDIA, you have two ways to build a "Secondary Index" to fix this:

A. Document-Partitioned (Local Index): Each node keeps an index of the ads it owns.

B. Term-Partitioned (Global Index): You create a separate index/table partitioned specifically by publisher_id.

The Choice: Which one would you choose for our Ad system, and what is the "Write Penalty" you pay for that choice?

### Answer

For the Publisher Portal query, I would choose the Term-Partitioned (Global Index) approach. This means creating a separate table that is partitioned by publisher_id. This way, when a publisher like NYTimes queries for their ads, we can do a single point lookup on the publisher_id partition and get all the ads associated with that publisher without having to scatter-gather across all nodes.

Tradeoff here would be with an extra write penalty. Every time we create or update an ad, we would have to write to both the main ad table (partitioned by ad_id) and the secondary index table (partitioned by publisher_id). This means that for every ad creation or update, we are doing two writes instead of one, which can increase the latency of write operations and also increase the load on the database. However, this tradeoff is necessary to ensure that our read queries for the publisher portal are efficient and do not suffer from high latency due to scatter-gather operations.

### Scenario 4: The Black Friday Scale-Up
This is the final test of your partitioning knowledge. It’s about Rebalancing.

The Context:
It is mid-November. Our click-tracking database is currently a cluster of 10 nodes. We use a simple hash-based routing: hash(ad_id) % 10.
As Black Friday approaches, we realize 10 nodes won't handle the traffic. We need to add 5 more nodes, bringing the total to 15.

The Problem:
If we simply update our code to hash(ad_id) % 15:

hash("ad_123") % 10 might have been Node 3.

hash("ad_123") % 15 might now be Node 8.

Suddenly, the database thinks the data for ad_123 is on Node 8, but the actual data is still sitting on Node 3. The system is effectively "empty" because it can't find any existing data.

The Questions for You:

Why is "Mod N" (hash % N) partitioning considered a "disaster" for rebalancing?

According to DDIA, what is a better way to assign data to nodes so that when we add Node 11, 12, 13, 14, and 15, we only have to move a small amount of data instead of remapping everything?

### Answer

The "Mod N" partitioning is considered a disaster for rebalancing because when you change the number of nodes (N), it changes the hash mapping for all keys. This means that every single key in the database would potentially need to be moved to a different node, which is a massive operation that can lead to downtime and performance degradation.

A better way to assign data to nodes is to use **Consistent Hashing**. In consistent hashing, each node is assigned a position on a hash ring. Each key is also hashed to a position on the same ring. A key is stored on the first node that comes after its position on the ring.

When you add new nodes, you only need to move the keys that fall between the new node's position and the next node's position on the ring. This means that when we add Node 11, 12, 13, 14, and 15, we only have to move a small fraction of the data (the keys that fall into the new nodes' ranges) instead of remapping everything. This allows for seamless scaling with minimal disruption to the system.