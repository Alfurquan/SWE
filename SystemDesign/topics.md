# 🏗️ System Design Fundamentals (Must-Haves for L5)

---

## 1. Requirements Analysis
- Functional vs Non-functional requirements (availability, latency, scalability, durability, cost).
- Clarifying scope with interviewer: MVP vs production-grade.
- Estimation & capacity planning: QPS, storage size, read/write ratio.

---

## 2. Networking & Communication
- Client-server model basics.
- Synchronous (REST, gRPC) vs Asynchronous (queues, pub/sub).
- WebSockets vs polling vs SSE (when to use each).
- Load balancers: horizontal scaling, sticky sessions.

---

## 3. Storage Systems
- SQL vs NoSQL (and when to choose each).
- NoSQL types: Key-value, Document, Column, Graph.
- Replication (leader-follower), Sharding, Partitioning.
- Indexing basics.
- Blob/Object storage vs block storage.

---

## 4. Caching
- Why caches help (latency, offload DB).
- Cache patterns: cache-aside, write-through, write-behind.
- Eviction: LRU, LFU, TTL.
- Consistency & invalidation strategies.
- CDN basics (edge caching).

---

## 5. Queues & Event-driven Systems
- Message queues (SQS, RabbitMQ) → async tasks, buffering.
- Pub/Sub (Kafka, Google PubSub) → decoupling, fan-out.
- Delivery semantics: at-most-once, at-least-once, exactly-once.
- Backpressure, consumer scaling.

---

## 6. Scalability Concepts
- Horizontal vs vertical scaling.
- Partitioning & consistent hashing.
- Read vs write scaling.
- Leader election basics.
- Idempotency in APIs.

---

## 7. Reliability & Resilience
- CAP theorem, PACELC trade-offs.
- Replication strategies.
- Circuit breakers, retries, exponential backoff.
- Quorum reads/writes.
- Fault tolerance, failover.

---

## 8. Monitoring & Operations
- Logging, metrics, tracing (LMT).
- SLAs, SLOs, SLIs.
- Canary deployments, feature flags.
- Observability → debugging distributed systems.

---

## 9. Security & Auth
- Authentication: OAuth, JWT, sessions.
- Authorization: RBAC, ABAC.
- TLS basics (encryption in transit).
- Token expiration & refresh strategies.

---

## 10. Analytics & Batch/Stream Processing (basic awareness)
- OLTP vs OLAP workloads.
- Batch (Hadoop/Spark) vs Streaming (Flink, Kafka Streams).
- ETL basics.
- When to use warehouses vs lakes.

---

# 🎯 Must-have Knowledge for Interviews
- **Trade-offs** → Every choice (SQL vs NoSQL, cache vs no-cache, sync vs async).
- **Scaling** → How to handle 10x or 100x more users.
- **Consistency vs Availability** → Be able to argue why you prioritize one.
- **Bottlenecks** → Identify weakest link in your design (DB, cache, network).
- **Failure handling** → What happens when a service or DB node goes down?

---

# 🚫 What you *don’t* need at L5
- Deep DB internals (B-trees, SSTables).
- Consensus protocol deep dives (Paxos, Raft proofs).
- Low-level networking (TCP/IP stack internals).
- Crypto math (RSA, AES).
- Vendor-specific tool details.

---

👉 If you master the **10 fundamentals above**, you’ll be equipped to tackle **any system design problem** at the whiteboard.  
The interview is less about “knowing all tech” and more about **clear reasoning, trade-offs, and structured approach**.
