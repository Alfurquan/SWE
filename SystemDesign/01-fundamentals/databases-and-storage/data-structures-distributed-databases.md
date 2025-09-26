# Data Structures that Power Distributed Databases

Distributed Databases are the backbone of modern large-scale applications, powering everything from real-time analytics to global e-commerce platforms.

Behind the scenes, these systems rely on specialized data structures to enable fast lookups, efficient storage, and high-throughput operations, even when managing terabytes of data.

## Hash Index

A hash index is a data structure that efficiently maps keys to values using a hash function.

The hash function converts a given key into an integer, which is used as an index in a hash table (buckets) to store and retrieve values.

This indexing technique is optimized for fast lookups and insertions, making it ideal for operations like:

- Inserting or finding a record with id = 123

In most cases, hash indexes provide an O(1) average-time complexity for insertions, deletions, and lookups.

**Hash Indexes are commonly used in key-value stores (e.g., DynamoDB) and caching systems (e.g., Redis) where quick access to data is crucial.**

## Bloom filters

A Bloom filter is a space-efficient, probabilistic data structure used to test set membership.

It answers the question: "Does this element exist in a set?"

Unlike traditional data structures, a Bloom filter does not store actual elements, making it extremely memory-efficient.

It starts as a bit array of size m, initialized with 0s, and relies on k independent hash functions, each of which maps an element to one of the m positions in the bit array.

## LSM trees (Log-Structured Merge Trees)

A Log-Structured Merge (LSM) Tree is a write-optimized data structure designed to handle high-throughput workloads efficiently.

Unlike B-Trees, which modify disk pages directly, LSM Trees buffer writes sequentially in memory and periodically flush them to disk, reducing random I/O operations.

This makes them ideal for write-heavy workloads.

### How LSM Trees Work ?

Writes (Inserts, Updates, Deletes)

- New writes are first stored in an in-memory structure called a MemTable (typically a Red-Black Tree or Skip List).
- Once the MemTable reaches a certain size, it is flushed to disk as an immutable SSTable (Sorted String Table).
- This sequential write pattern ensures fast insertions while avoiding costly disk seeks.

Reads

- Reads first check the MemTable (fast in-memory lookups).
- If not found, the search moves to recent SSTables.
- A Bloom Filter is often used to quickly determine whether a key exists in an SSTable.
- If found, the key is retrieved via binary search.

Compaction (Merging SSTables)

- Over time, multiple SSTables accumulate, increasing read overhead.
- To optimize storage and retrieval, the system merges smaller SSTables into larger ones.
- Compaction removes duplicate, obsolete, or deleted records, reducing disk space.

**LSM Trees are widely used in high-scale NoSQL databases like: Apache Cassandra, Google Bigtable and RocksDB.**

## Merkle Trees

A Merkle Tree (also called a Hash Tree) is a tree-based data structure that enables efficient and secure verification of large data sets. It is widely used in distributed databases and blockchain systems to ensure data consistency and tamper resistance.

### Why Merkle Trees?

In distributed systems, data is often replicated across multiple nodes. If even a single bit of data is modified, the system needs an efficient way to detect inconsistencies without rechecking the entire dataset.

Merkle Trees solve this problem by organizing data into a tree structure, where:

- Leaf nodes store cryptographic hashes of data blocks.
- Non-leaf (intermediate) nodes store hashes of their child node.
- The Merkle Root (topmost node) uniquely represents the entire dataset.

This structure allows quick verification by simply comparing hash values instead of entire data blocks.

## B-Trees and Variants (B+ Trees, B Trees)*

A B-tree is a self-balancing tree data structure designed to store sorted data in a way that optimizes reads, writes, and queries on large datasets.

In database indexing and file storage, the major performance bottleneck is disk I/O.

B-Trees minimizes disk I/O by storing multiple keys in a single node and automatically balancing itself providing logarithmic time complexity for search, insertion and deletion.

Unlike binary search trees, where each node has at most two children, B-Trees allow multiple children per node. The number of children is defined by the order of the B-Tree.

Internal nodes contain keys and pointers to child nodes and leaf nodes contain keys and pointers to the actual data.

Keys in each node are stored in sorted order, enabling fast binary searches.

## Skip lists

A skip list is a probabilistic data structure that extends the functionality of linked lists by adding multiple levels of "shortcuts" to enable fast search, insertion, and deletion operations.

### How skip list works ?

- A skip list consists of multiple levels, with each level being a subset of the level below.
- The bottom-most level contains all elements in sorted order (like a regular linked list).
- Higher levels contain fewer elements, acting as shortcuts to speed up searches.
- Nodes are randomly promoted to higher levels, ensuring an even distribution without requiring rebalancing.

This structure allows O(log n) average-time complexity for search, insertion, and deletion while maintaining the simplicity of linked lists.

Skip lists are particularly well-suited for in-memory storage and dynamic datasets where updates are frequent.

Redis uses skip lists to implement it’s sorted sets (ZSET), enabling fast insertions, deletions, and range queries while maintaining sorted order.

## Inverted Index

An inverted index is a data structure that maps terms (words or tokens) to the documents or locations where they appear.

It is called "inverted" because it reverses the conventional relationship of an index: instead of mapping documents to the terms they contain, it maps terms to the documents that contain them.

### How Inverted Index is Created

- Tokenization: Text is split into individual tokens (words or terms).

Example: "Database systems are powerful" → ["database", "systems", "are", "powerful"]

- Normalization: Tokens are standardized (e.g., lowercased, stemmed, or lemmatized).

Example: "Databases" → "database"

- Index Construction and Storage: For each term, a postings list is created or updated with the document ID and metadata (e.g., term frequency, positions).

Inverted indexes are widely used in databases, search engines, and information retrieval systems to enable efficient keyword lookups, Boolean queries, and relevance ranking.

## CRDTs (Conflict-Free Replicated Data Types)

A Conflict-Free Replicated Data Type (CRDT) is a distributed data structure that allows concurrent updates across multiple nodes without requiring coordination. CRDTs ensure that all replicas eventually converge to the same state, even if updates are applied in different orders.

In distributed databases and real-time applications, multiple nodes may receive concurrent updates. Traditional approaches use locks or coordination mechanisms to maintain consistency, but this slows down performance and reduces availability.

CRDTs solve this problem by allowing each node to update its local copy of the data independently, and when nodes sync, updates are merged automatically without conflicts.

### How CRDTs Work ?

CRDTs ensure eventual consistency using two key properties:

- Idempotency: Repeated application of the same update does not change the final result. This avoids duplicate operations when syncing nodes.

- Commutativity & Associativity: Order of operations does not matter—updates can arrive in any order, and merging will still produce the correct result. This ensures conflict-free resolution.

### Types of CRDTs

CRDTs are broadly classified into two categories based on their merging strategy:

- State-Based CRDTs (Convergent Replicated Data Types - CvRDT)
Each node maintains a local state and periodically sends the entire state to other replicas.

Nodes merge states using a deterministic function.

- Operation-Based CRDTs (Commutative Replicated Data Types - CmRDT)
Instead of syncing the entire state, nodes only propagate operations (changes).

Operations are applied in the same order at all nodes.

CRDTs are used for eventual consistency in NoSQL databases.

## Vector clocks

A Vector Clock (VC) is a mechanism used in distributed systems to keep track of the order of events across multiple nodes without requiring a centralized clock.

It helps determine causality between events, answering questions like:

- Did Event A happen before Event B?
- Are Events A and B concurrent (happened independently)?
- Did two updates conflict, and if so, how should they be resolved?

In distributed databases and systems, different nodes often process updates out of order due to network latency, failures, or parallel execution. Traditional timestamps (e.g., UNIX time) cannot reliably capture causal relationships between events. Vector Clocks solve this problem by providing a structured way to track event dependencies

### How vector clocks work ?

A Vector Clock is essentially a list of counters, where:

- Each node (or process) in the distributed system maintains its own vector (array) of logical timestamps.
- Each entry in the vector represents a node's current logical time.
- Every time an event occurs at a node, its own counter is incremented.
- When a node sends a message, it includes its current vector clock.
- When a node receives a message, it updates its vector by taking the maximum value for each entry.

### How to Compare Two Vector Clocks ?

- Happens Before (V1 < V2)
If all elements in V1 are less than or equal to V2, and at least one is strictly less, then V1 happened before V2 (V1 → V2).

- Concurrent Events (V1 || V2)
If some elements in V1 are greater and some are smaller than V2, the events are concurrent.

- Conflict Detection
If two nodes update the same value concurrently, the system must resolve the conflict (e.g., via Last-Write-Wins or merging strategies).

**Vector Clocks are used in distributed databases like DynamoDB and Cassandra to help detect conflicting updates and resolve them gracefully.**

## Geo Hash

A Geohash is a spatial data structure that encodes latitude and longitude coordinates into short alphanumeric strings, allowing efficient storage and retrieval of geographic data.

The encoding is hierarchical, meaning that shorter Geohashes represent larger areas, while longer Geohashes represent more precise locations.

### Geohash Encoding Process

1. Divide the Earth's surface into a grid

- The world is divided into a 2D grid based on latitude and longitude.
- Each grid cell is assigned a binary value based on whether the coordinate is above or below a midpoint.

2. Interleave Latitude and Longitude bits

- The latitude and longitude values are converted into binary representations and interleaved to form a single binary string.

3. Convert the binary string to a Geohash

- The binary sequence is converted into an alphanumeric string using a base-32 encoding scheme (digits 0-9 and letters except ‘a’, ‘i’, ‘l’, and ‘o’ to avoid confusion).

## What to Know for System Design

### Hash Index

- **Purpose:** Fast key-value lookups.
- **Use Case:** Caches, key-value stores (Redis, DynamoDB).
- **Strengths:** O(1) average lookup, insert, delete.
- **Limitations:** Not good for range queries.

### Bloom Filter

- **Purpose:** Probabilistic membership test (is X in set?).
- **Use Case:** Caches, databases (Cassandra, Bigtable), spam filters.
- **Strengths:** Very space-efficient, fast.
- **Limitations:** False positives possible, no deletions (unless counting Bloom filter).

### LSM Tree (Log-Structured Merge Tree)

- **Purpose:** Write-optimized storage for high-throughput workloads.
- **Use Case:** NoSQL databases (Cassandra, RocksDB, Bigtable).
- **Strengths:** Fast writes, good for sequential disk access.
- **Limitations:** Reads can be slower, needs compaction.

### Merkle Tree

- **Purpose:** Efficient and secure verification of large datasets.
- **Use Case:** Blockchains, distributed databases.
- **Strengths:** Tamper detection, quick consistency checks.
- **Limitations:** More complex than simple hash lists.

### B Tree

- **Purpose:** Balanced tree for sorted data and range queries.
- **Use Case:** Relational databases, file systems.
- **Strengths:** Fast range queries, balanced structure.
- **Limitations:** More disk I/O for writes than LSM trees.

### Skip List

- **Purpose:** Probabilistic alternative to balanced trees for ordered data.
- **Use Case:** In-memory indexes (Redis), concurrent data structures.
- **Strengths:** Simple, fast search/insert/delete.
- **Limitations:** Not as cache-friendly as trees.

### Inverted Index

- **Purpose:** Maps content (e.g., words) to locations (e.g., documents).
- **Use Case:** Search engines, full-text search (Elasticsearch, Solr).
- **Strengths:** Fast text search.
- **Limitations:** Needs extra storage for index.

### CRDT (Conflict-free Replicated Data Type)

- **Purpose:** Data type for eventual consistency in distributed systems.
- **Use Case:** Real-time collaboration (Google Docs), distributed databases.
- **Strengths:** Automatic conflict resolution, no central coordination.
- **Limitations:** More memory overhead, complex logic.

### Vector Clock

- **Purpose:** Track causality and ordering of events in distributed systems.
- **Use Case:** Distributed databases, versioning.
- **Strengths:** Detects concurrent updates.
- **Limitations:** Grows with number of nodes.

### HyperLogLog

- **Purpose:** Probabilistic counting of unique elements.
- **Use Case:** Analytics, counting unique users/events.
- **Strengths:** Very space-efficient for cardinality estimation.
- **Limitations:** Approximate results, not exact.

### Count-Min Sketch

- **Purpose:** Probabilistic frequency counting.
- **Use Case:** Streaming analytics, network monitoring.
- **Strengths:** Space-efficient, fast.
- **Limitations:** Overestimates counts, approximate only.

### Geo Hash

- **Purpose:** Encode geographic coordinates into short strings.
- **Use Case:** Location-based search, spatial indexing.
- **Strengths:** Efficient spatial queries, easy to shard.
- **Limitations:** Precision loss at higher compression.
