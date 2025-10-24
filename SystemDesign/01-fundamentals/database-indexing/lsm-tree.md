# LSM Trees (Log-Structured Merge Trees)

LSM trees solve the write problem by batching writes in memory and flushing them to disk sequentially. Instead of immediately writing each update to disk like B-trees do, LSM trees buffer changes in memory and write them out in large chunks. This converts many small random writes into fewer large sequential writes, increasing efficiency.

Here's what happens when you write to a database that uses LSM trees:

- Memtable (Memory Component): New writes go into an in-memory structure called a memtable, typically implemented as a sorted data structure like a red-black tree or skip list. This is extremely fast since it's all in RAM.

- Write-Ahead Log (WAL): To ensure durability, every write is also appended to a write-ahead log on disk. This is a sequential append operation, which is much faster than random writes.

- Flush to SSTable: Once the memtable reaches a certain size (often a few megabytes), it's frozen and flushed to disk as an immutable Sorted String Table (SSTable). This is a single sequential write operation that can write megabytes of data at once.

- Compaction: Over time, you accumulate many SSTables on disk. A background process called compaction periodically merges these files, removing duplicates and deleted entries. This keeps the number of files manageable and maintains read performance.

This makes writes incredibly fast, you're just appending to memory and a log file. Even when flushing to disk, you're writing large sequential chunks rather than seeking to random locations.

## Negative Impact on Reads

As always, this benefits comes at a cost. While LSM trees excel at writes, they make reads more complex. Remember how B-trees could find any record with just 2-3 disk reads? With LSM trees, the story is different.

When you query for a specific key, the database must check multiple places:

- First, the memtable: Is the data in the current in-memory buffer?
- Then, immutable memtables: Any memtables waiting to be flushed?
- Finally, all SSTables on disk: Starting from the newest (most likely to have recent data) and working backwards

This means a single point query might need to check dozens of files in the worst case. It's like searching for a document that could be in your desk drawer, filing cabinet, or any of several archive boxes. And you have to check them all.

Obviously, this would make LSM trees almost unusable for any workflow requiring reasonable read performance. So to mitigate this problem, LSM trees typically employ several optimizations:

- Bloom Filters: Each SSTable has an associated bloom filter - a probabilistic data structure that can quickly tell you if a key is definitely NOT in that file. This lets you skip most SSTables without reading them. If the bloom filter says "maybe", you still need to check, but it eliminates the definite misses.

- Sparse Indexes: Since SSTables are sorted, they maintain sparse indexes that tell you the range of keys in each block. If you're looking for user_id=500 and an SSTable only contains keys 1000-2000, you can skip it entirely.

- Compaction Strategies: Different compaction strategies optimize for different workloads. Size-tiered compaction minimizes write amplification but can lead to more files to check. Leveled compaction maintains fewer files but requires more frequent rewrites.

Despite these optimizations, LSM trees fundamentally trade read performance for write performance. This makes them perfect for write-heavy workloads like time-series databases, logging systems, and analytics platforms where you're constantly ingesting new data but queries are less frequent or can tolerate slightly higher latency.

The key insight for system design interviews is knowing when this trade-off makes sense. If you're building a system that writes far more than it reads - like a metrics collection system, audit log, or IoT data platform - LSM trees are likely the right choice. But for a user-facing application where every page load triggers multiple queries, B-trees usually perform better.

## Real-World Examples

LSM trees power some of the most write-heavy systems on the internet:

- Cassandra handles Netflix's billions of viewing events. When you watch a show, that data gets written to Cassandra's LSM-based storage without slowing down playback.

- RocksDB (built by Facebook) serves as the storage engine for many databases. It handles millions of social interactions per second—likes, posts, messages—all written to LSM trees for fast persistence.

- DynamoDB uses both LSM trees and B-trees, automatically choosing the right storage engine for each workload. Write-heavy data like IoT sensor readings gets routed to LSM tree storage for fast appends. Read-heavy data like product catalogs gets B-tree storage for fast lookups. DynamoDB monitors your access patterns and switches between storage engines behind the scenes.

---