# 🎯 System Design Interview Tech Knowledge Guide (Google L5+)

---

## 🔌 Communication / APIs
✅ Learn:
- REST vs gRPC vs GraphQL (trade-offs).
- WebSockets vs long-polling vs SSE (when to use, scaling).
- Load balancing strategies (round-robin, least connections, sticky sessions).
- Rate limiting, throttling, API gateways.

❌ Avoid:
- HTTP/2 frame encoding.
- gRPC serialization internals.

---

## 📡 Messaging / Event-driven
✅ Learn:
- Kafka / PubSub / Kinesis concepts: topics, partitions, consumer groups.
- Delivery semantics: at-most-once, at-least-once, exactly-once.
- Replayability, backpressure handling.
- Trade-offs of async vs sync.

❌ Avoid:
- Kafka log segment compaction internals.
- Zookeeper/Raft consensus details.

---

## 🗄 Databases
✅ Learn:
- SQL vs NoSQL → when to use each.
- NoSQL types: key-value, document, column, graph.
- Replication (leader-follower), sharding, partitioning.
- Transactions vs eventual consistency.
- OLTP vs OLAP.

❌ Avoid:
- Query planner internals.
- B-tree vs LSM tree storage details.
- Compaction algorithms (SSTables, WAL internals).

---

## ⚡ Cache (Redis, Memcached)
✅ Learn:
- Why cache: latency, DB offload.
- Patterns: cache-aside, write-through, write-behind.
- Eviction: LRU, LFU, TTL.
- Scaling: sharding, replication.
- Cache invalidation strategies.

❌ Avoid:
- Redis data structure internals (ziplist, skiplist, etc.).
- Memcached slab allocator internals.

---

## 🗃 Queues (SQS, RabbitMQ, etc.)
✅ Learn:
- Use cases: async tasks, decoupling services.
- DLQ (dead letter queues).
- Scaling consumer workers.
- Delivery semantics trade-offs.

❌ Avoid:
- AMQP wire protocol.
- Queue broker persistence internals.

---

## 🌐 Storage
✅ Learn:
- Block vs object vs file storage.
- Blob/Object storage (S3, GCS): durability, eventual consistency, cost.
- CDN (CloudFront, Akamai, Cloudflare): caching, invalidation, latency reduction.

❌ Avoid:
- CRUSH algorithm (Ceph).
- Erasure coding details in S3.
- CDN routing algorithms.

---

## 🛠 Search & Indexing
✅ Learn:
- When to use Elasticsearch/Solr.
- Inverted indexes basics.
- Trade-offs: indexing latency vs query latency.
- Full-text search vs DB queries.

❌ Avoid:
- Lucene scoring algorithms.
- Segment merging internals.

---

## 🔑 Authentication & Security
✅ Learn:
- OAuth, JWT, session cookies.
- Scaling auth: stateless tokens, centralized ID provider.
- TLS basics (why needed, not crypto internals).
- Security trade-offs: expiration, refresh, revocation.

❌ Avoid:
- Exact OAuth RFC flows.
- Cryptographic primitive details (RSA, AES internals).

---

## 🏗 Scalability Patterns
✅ Learn:
- Horizontal vs vertical scaling.
- Partitioning & consistent hashing.
- Leader election basics.
- CQRS & Event Sourcing basics.
- Idempotency in APIs.

❌ Avoid:
- Paxos/Raft deep dives.
- Exact distributed consensus proofs.

---

## 📊 Analytics / Big Data
✅ Learn:
- Batch (Hadoop/Spark) vs Streaming (Flink, Spark Streaming, Kafka Streams).
- Data lake vs data warehouse.
- ETL vs ELT.
- Common trade-offs: latency vs throughput vs cost.

❌ Avoid:
- Spark DAG scheduler internals.
- Hadoop YARN details.

---

## 🛡 Resiliency / Reliability
✅ Learn:
- CAP theorem, PACELC.
- Circuit breakers, retries, backoff.
- Quorum reads/writes.
- Failover & replication strategies.

❌ Avoid:
- Detailed gossip protocol internals.

---

## 🚦 Monitoring / Ops
✅ Learn:
- Logging vs metrics vs tracing.
- SLAs, SLOs, SLIs.
- Canary releases, feature flags.
- Observability trade-offs.

❌ Avoid:
- Vendor-specific observability tool internals.

---

# 📝 Rule of Thumb
- ✅ Know concepts, trade-offs, scaling patterns, and when to apply.
- ❌ Skip internals, algorithms, and implementation details (unless you’re interviewing for infra/DB/storage specialization).
