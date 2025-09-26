# System Design: Work Backwards from Problems and Iterate

In **system design**, the phrase *"work backwards from common problems
and iterate"* usually refers to a **practical approach to solving design
questions** --- instead of trying to build the "perfect" architecture
from scratch, you start by imagining the **real-world problems systems
usually face**, and then evolve your design step by step to address
them.

------------------------------------------------------------------------

## 🔹 Step-by-Step Approach

### 1. Start simple (baseline design)

Begin with a **naïve design** that just solves the functional
requirements, without worrying about scale or failure.

Example:\
For a Twitter-like service, your baseline may just be:\
- App server + DB\
- Users → Post tweets → Stored in DB\
- Users → Fetch tweets → Query DB

------------------------------------------------------------------------

### 2. Identify common problems

Now ask: *What breaks if the system grows?* or *What if requirements get
tougher?*

Some common problems:\
- **Scaling reads** → Too many users hitting the DB.\
- **Scaling writes** → Too many posts overwhelming the DB.\
- **Hotspotting** → A celebrity tweet overloads one partition.\
- **High latency** → Users worldwide face slow responses.\
- **Data loss / consistency** → What if a server crashes?\
- **Large blobs** → Images/videos don't fit in DB well.\
- **Long running tasks** → Processing videos takes minutes, blocking
users.

------------------------------------------------------------------------

### 3. Work backwards from those problems

Instead of over-designing, take one problem at a time and **iterate the
design**:

-   **Scaling reads?** → Add cache (Redis/Memcached), read replicas.\
-   **Scaling writes?** → Introduce sharding, partition DB.\
-   **Hotspotting?** → Use consistent hashing, load balancers.\
-   **Latency?** → Add CDNs, geo-distributed servers.\
-   **Data loss?** → Replication, backups, message queues.\
-   **Large blobs?** → Move to object storage (S3).\
-   **Long tasks?** → Offload to async workers + queues.

Each iteration refines the system to handle a *specific, common failure
mode*.

------------------------------------------------------------------------

### 4. Iterate & balance trade-offs

You don't try to solve everything at once --- you **layer solutions**.\
At each stage:\
- Evaluate if the added component solves the problem.\
- Re-check trade-offs (cost, complexity, latency, consistency).\
- Continue until the system is robust enough for the scale.

------------------------------------------------------------------------

## 📝 Common Problems & How to Iterate in System Design

### 1. **Scaling Reads**

-   **Problem**: Too many users reading data → DB overloaded.
-   **Iterations**:
    -   Add cache (Redis / Memcached).\
    -   Add read replicas.\
    -   Use CDNs (for static/large content).\
    -   Use denormalization or materialized views for faster queries.

### 2. **Scaling Writes**

-   **Problem**: DB can't handle high write throughput.
-   **Iterations**:
    -   Sharding / partitioning.\
    -   Write-ahead queues (Kafka, RabbitMQ).\
    -   Batch writes.\
    -   Use NoSQL for high-ingest workloads.

### 3. **Hotspotting / Uneven Load**

-   **Problem**: One partition or node gets overloaded (e.g., celebrity
    tweet).\
-   **Iterations**:
    -   Consistent hashing.\
    -   Load balancing (round-robin, weighted).\
    -   Randomized IDs / key prefixing to spread load.

### 4. **Latency**

-   **Problem**: Users in distant regions experience slowness.\
-   **Iterations**:
    -   CDN for static assets.\
    -   Geo-distributed servers & databases.\
    -   Edge caching.\
    -   Async APIs (return fast, process later).

### 5. **Data Loss / Durability**

-   **Problem**: What if a machine crashes?\
-   **Iterations**:
    -   Replication (multi-AZ / multi-region).\
    -   Write-ahead logging.\
    -   Backups & snapshots.\
    -   Queue-based processing (at least once delivery).

### 6. **Consistency vs Availability**

-   **Problem**: Conflicts in distributed writes.\
-   **Iterations**:
    -   Leader--follower replication (strong consistency).\
    -   Multi-leader / quorum (eventual consistency).\
    -   Conflict resolution (last-write-wins, CRDTs, app logic).

### 7. **Large Blobs (images, videos, files)**

-   **Problem**: DB not good at storing blobs.\
-   **Iterations**:
    -   Move blobs to object storage (S3, GCS, Azure Blob).\
    -   Store only metadata/links in DB.\
    -   Use CDN for delivery.

### 8. **Long Running Tasks**

-   **Problem**: Video processing, ML training, batch jobs take too
    long.\
-   **Iterations**:
    -   Offload to async workers.\
    -   Use job queues.\
    -   Track progress with job IDs.\
    -   Use distributed task frameworks (Celery, Airflow, etc.).

### 9. **Fault Tolerance / Failover**

-   **Problem**: Single server failure → downtime.\
-   **Iterations**:
    -   Redundant replicas.\
    -   Leader election (ZooKeeper, Raft, Paxos).\
    -   Circuit breakers, retries, backoff.

### 10. **Security & Abuse**

-   **Problem**: Spamming, DDoS, bad actors.\
-   **Iterations**:
    -   Rate limiting & quotas.\
    -   Authentication & authorization.\
    -   WAF / DDoS protection.\
    -   Audit logging.

### 11. **Observability**

-   **Problem**: System misbehaves, can't debug easily.\
-   **Iterations**:
    -   Centralized logging.\
    -   Metrics + monitoring dashboards.\
    -   Distributed tracing (Jaeger, OpenTelemetry).\
    -   Alerts & on-call runbooks.

### 12. **Cost & Efficiency**

-   **Problem**: Cloud bills skyrocketing at scale.\
-   **Iterations**:
    -   Use caching/CDN to reduce DB load.\
    -   Auto-scaling.\
    -   Spot/preemptible instances.\
    -   Optimize storage (cold vs hot tiers).

------------------------------------------------------------------------

## 🎤 System Design Iteration Script (Interview-Ready)

### 1. Start with baseline

*"Let me start with a very simple design that satisfies the core
functional requirements: a client talks to an app server, and the app
server reads/writes to a single database. This works well at small
scale."*

### 2. Introduce problems one by one & iterate

**Scaling Reads**\
*"If the system grows, one common issue is too many reads on the
database. To solve this, I'd add a cache like Redis to handle frequent
queries, and possibly read replicas to offload traffic."*

**Scaling Writes**\
*"Next, with heavy write traffic, a single DB becomes a bottleneck. At
that point, I'd shard or partition the database to spread writes across
nodes."*

**Hotspotting**\
*"If certain keys/users get disproportionate traffic --- say a celebrity
tweet --- I'd use consistent hashing or add load balancing to avoid
hotspots."*

**Latency / Global Users**\
*"For global scale, latency becomes an issue. I'd introduce a CDN for
static content and possibly geo-distributed servers for faster access."*

**Data Loss / Durability**\
*"Another concern is reliability. If a node crashes, we risk losing
data. To mitigate, I'd add replication across availability zones, and
use write-ahead logs or backups."*

**Consistency vs Availability**\
*"In a distributed setup, we need to balance consistency and
availability. For strong consistency, I'd stick to leader--follower. For
high availability, I might allow eventual consistency with conflict
resolution."*

**Large Blobs**\
*"For large assets like images or videos, storing them directly in the
DB is inefficient. I'd move them to an object store (like S3) and serve
via CDN."*

**Long Running Tasks**\
*"If the system has tasks like video processing, we shouldn't block
requests. I'd offload those to background workers with a queue and let
clients poll for status."*

**Fault Tolerance**\
*"If servers fail, we need redundancy. I'd set up replicas and use
leader election for failover, along with retries and circuit breakers
for resiliency."*

**Security & Abuse**\
*"At scale, abuse is a risk. I'd enforce rate limiting, authentication,
and WAF for protection against DDoS."*

**Observability**\
*"To operate reliably, we need monitoring. I'd add centralized logging,
metrics dashboards, and distributed tracing for debugging issues."*

**Cost & Efficiency**\
*"Finally, cost efficiency is key at scale. Caching, auto-scaling, and
storage tiering help keep costs under control."*

------------------------------------------------------------------------

### 3. Wrap up with trade-offs

*"So, starting from a simple design, I iterated by addressing common
scaling and reliability issues one by one. The exact choices depend on
priorities --- for example, if strong consistency is critical, I'd favor
leader--follower; if high availability is more important, I'd lean
toward eventual consistency."*

------------------------------------------------------------------------

✅ This script gives you a **clear path**:\
- Start simple.\
- Add components only when problems appear.\
- Explain trade-offs.
