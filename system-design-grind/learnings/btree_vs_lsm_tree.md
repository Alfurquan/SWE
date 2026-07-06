# B-Tree vs LSM Tree — Decision Framework

## The Core Decision

```
B-Tree:   Pay on WRITE (random I/O to update in place)
          Benefit on READ (one tree traversal, predictable)

LSM Tree: Pay on READ (check multiple SSTables)
          Benefit on WRITE (sequential I/O, batched)
          Pay LATER (compaction — deferred cost of reorganizing data)
```

## Decision Criteria

| Question | B-Tree if... | LSM Tree if... |
|----------|-------------|----------------|
| Write-to-read ratio? | Read-heavy (>70% reads) | Write-heavy |
| Latency requirements? | p99 matters (predictable, no compaction spikes) | Average latency matters more than p99 |
| Transactions needed? | Yes — key exists in one place, simple locking | Not critical |
| Write throughput? | Moderate (<50K writes/sec per node) | High (100K+ writes/sec) |

---

## Practice Scenarios

### 1. User Profile Database
**Requirements**: 90% reads, 10% updates, needs transactions
**Choice**: B-Tree

Since the system is read heavy with a read to write ratio of 9:1 and it needs transactions, B-tree is the right choice. B-tree provides good read performance — we simply need to traverse 3-4 levels of the tree (branching factor 100-500 means billions of keys fit in 3-4 levels, so 3-4 disk I/Os per lookup). For LSM tree, we would need to first check the memtable and then search multiple SSTables. If compaction is not well performed, read complexity grows significantly. Also transaction support in B-tree is natural as every key exists in exactly one place and is easy to lock, compared to LSM tree where the key could be in memtable and multiple SSTables.

---

### 2. IoT Sensor Ingestion
**Requirements**: 500K writes/sec, queries are "last 24 hours for device X"
**Choice**: LSM Tree

Since the system is write heavy with 500K writes/sec, LSM tree is the right choice. LSM tree provides good write performance as data is written sequentially using append mechanism which is much faster compared to B-tree where data is written randomly and updated in position. At 500K writes/sec, B-tree would struggle — each write is a random I/O, and even SSDs max out around 50-100K random writes/sec.

Since LSM based databases use memtables and SSTables which are sorted using keys, queries like "last 24 hours for device X" can be supported efficiently. We can have memtable and SSTable sorted by a compound key like (device_name, timestamp) and then using binary search we can get the required index and do range scans on already sorted data.

---

### 3. E-commerce Product Catalog
**Requirements**: Frequent reads, occasional bulk imports, strong consistency needed
**Choice**: B-Tree

Since the system has frequent reads and needs strong consistency, B-tree is the right choice. Read performance is strong — 3-4 disk I/Os per lookup with branching factor 100-500. Transaction support is natural with single-location keys. For occasional bulk imports, B-tree can handle these without issue since writes happen infrequently. For large bulk imports specifically, building the index offline on sorted data and swapping it in is more efficient than row-by-row inserts.

---

### 4. Ad Click Tracking
**Requirements**: Extremely write-heavy, queries are hourly aggregations, p99 read latency not critical
**Choice**: LSM Tree

Since the system is write heavy and p99 read latency is not critical, LSM tree is the right choice. LSM tree provides good write performance through sequential append mechanism. Since p99 read latency is not critical, compaction spikes are acceptable — a good compaction strategy can optimize read performance.

For hourly aggregations, two approaches:
- **Real-time**: Dual write path using Kafka → stream processing (Flink/Spark Streaming) to compute hourly aggregations on the fly → write to a read-friendly or columnar database for fast querying.
- **Batch**: Scheduled job reads from LSM tree database, aggregates the data, writes to a materialized view optimized for read performance.
