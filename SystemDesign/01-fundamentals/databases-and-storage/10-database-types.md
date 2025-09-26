# 10 Must-Know Database Types for System Design Interviews

## Relational

A Relational Database stores data in structured tables with rows and columns. It’s like an Excel sheet, but much more powerful. Each table represents an entity (like Users, Orders, or Products), and relationships between tables are defined using foreign keys. It uses SQL (Structured Query Language) to query and manipulate data.

### When to use it ?

- Your data is structural and relational
- You need strong consistency
- You require complex query and reporting

### Design considerations

- Indexing: Indexes speed up read-heavy queries by allowing the database to quickly locate rows.
Create indexes on frequently queried columns (e.g., user_id, email). Use composite indexes for multi-column filters. Avoid over-indexing in write-heavy systems, as it can slow down inserts and updates.

- Normalization vs Denormalization: Normalize to reduce redundancy and ensure consistency. Denormalize in read-heavy systems to reduce join overhead.

- Joins: Joins are powerful for analytics and reporting. However, avoid excessive joins on large tables as they can become performance bottlenecks. Never design for cross-shard joins unless absolutely necessary.

- Sharding: Sharding enables horizontal scaling but introduces complexity.

## In memory

An In-Memory Database stores data directly in RAM instead of disk. This makes it blazingly fast for read and write operations.

### When to use it ?

- Ultra low latency need
- The data is temporary or can be regenerated
- You want to reduce load on your main database

### Design considerations

- Volatility: Since RAM is volatile, data is lost on crash or restart unless persistence is enabled.
Tools like Redis offer optional persistence via:
  - RDB (snapshotting): Saves data at intervals
  - AOF (Append Only File): Logs each write operation.
- Eviction policies: RAM is fast, but limited. When memory runs out, older or less-used data is evicted. Common eviction policies include LRU, LFU and TTL.
- Keep It Lean: Avoid storing large files or infrequently accessed data. Store only hot and frequently accessed data such as user sessions and recent activity.

## Key-Value

A Key-Value Database is the simplest type of database. It stores data as a collection of key-value pairs, where each key is unique and maps directly to a value. Think of it like a giant, distributed HashMap. There are no tables, schemas, or relationships—just keys and values. This makes key-value stores extremely fast and highly scalable.

### When to use it ?

- You need fast lookups by unique key
- You don’t need complex queries or relationships
- You’re dealing with high-volume, low-latency workloads

### Design considerations

- Lookup only access: You can only retrieve values by key. They typically don’t provide filtering, sorting, or joining. Secondary indexes are typically not supported.
- No enforced schema: Key-value databases are schema-less. Values can be strings, JSON, or binary blobs.
- Easy horizontal scaling: Key-based partitioning enables seamless distribution across nodes using consistent hashing or range-based partitioning.

## Document

A document database stores data as documents, typically in JSON or BSON format. Each document is a self-contained unit with fields and values making it flexible and schema-less.

### When to use it ?

- Data structures vary across records
- You need to store nested or hierarchical data
- You want schema flexibility and fast iteration

### Design considerations

- Indexing: Indexing is crucial for performance but indexing deeply nested fields may add overhead.
- Document Size Limits: Most systems (e.g., MongoDB) have limits (like 16MB per document). Large documents may need to be split or restructured.
- Denormalization: Related data is often embedded to avoid joins. This improves read performance but can increases write complexity and risk of duplication.
- Sharding: Most document databases support horizontal scaling via sharding, but it requires careful design

## Graph

A Graph Database is designed to store and navigate relationships. It represents data as nodes (entities) and edges (relationships between entities). This structure makes it ideal for scenarios where connections are as important as the data itself.

### When to use it ?

- Relationships are central to your data: Example - In a social network, you might need to find "friends of friends"
- You need traversals or recommendations: Example:
    - Movies watched by people similar to you
    - Customers who bought Product A also bought Product B
- You need to run complex relationship queries efficiently

### Design considerations

- Traversal Efficiency: Graph databases handle multiple level of relationships far more efficiently than relational joins. 
- Indexing: While traversals are optimized, indexing is still essential for quickly locating the starting node(s) of a query. Index common node and relationship properties like user_id, email, or timestamp.
- Schema Flexibility: While schema is optional, consistent labeling (e.g., User, FOLLOWS) helps maintain query clarity and performance.
- Query Language: Graph databases use domain-specific languages to query and manipulate graph data like Cypher (used by neo4j), gremlin etc.

## Wide column

A Wide-Column Database stores data in tables, rows, and columns, but unlike traditional relational databases, each row can have a different set of columns. It’s optimized for large-scale, write-heavy workloads and high-speed data retrieval across massive datasets.

### When to use ?

- You need high write throughput at scale: Example: A time-series logging service that collects logs from thousands of services every second.
- Your data grows continuously and at massive scale
- You want fast lookups and flexible row-level schemas

### Design considerations

- Schema design: In wide-column databases, the most critical part of performance comes down to how you design:
 - Row keys – Used to identify rows uniquely (e.g., user_id, device_id)
 - Partition keys – Determines how data is distributed across nodes
 - Clustering columns – Defines how data is sorted within a partition
- Denormalization
- Indexing
- Sharding and replication
- Tunable consistency

## Time series

A Time-Series Database (TSDB) is purpose-built to store, retrieve, and analyze data points that are time-stamped.

### When to use it ?

- Data is generated in chronological order
- You need to perform rollups, aggregations, or downsampling
- You need high write volume with time-bound queries

## Text search

A Text-Search Database is designed to efficiently store, index, and search through large volumes of textual data. It goes beyond simple substring matching by supporting full-text search, ranking, tokenization, stemming, fuzzy matching, and relevance scoring.

Instead of scanning documents line by line, it builds inverted indexes—a map of words to the documents they appear in, allowing lightning-fast text lookups.

### When to use it ?

- You need fast, flexible search over text: Example: In an e-commerce store, find products that match the phrase "running shoes", ranked by relevance.
- You want ranked or fuzzy search: A blog platform where searching “recieve” still returns results for “receive”.
- You need search plus structured filtering: Example: A real estate site where users search for "3-bedroom house near park" and filter by price range, location, and amenities.

### Design considerations

- Inverted Indexing: Instead of storing data row-by-row like a typical database, text-search engines build an inverted index—a data structure that maps terms (words) to the documents they appear in. Example: "shoe" → [doc_2, doc_4, doc_7]

- Tokenization & Stemming: Before indexing, search engines tokenize the text (split it into individual words) and often apply stemming or lemmatization to reduce words to their root form. “Running”, “runs”, and “ran” → “run”

- Relevance Scoring: Text-search engines don’t just match documents, they rank them by relevance using scoring algorithms like TF-IDF or BM25.

## Spatial

A Spatial Database is designed to store and query geospatial data—information about locations, shapes, distances, and coordinates on Earth. It supports complex spatial operations like proximity search, intersection, bounding box queries, and geofencing.

### When to use it ?

- Your system uses location-based features: A ride-hailing app like Uber
- You need to store and query shapes or regions

## Blob store

A Blob Store is a storage system optimized for handling large, unstructured binary files like images, videos, PDFs, backups, or logs.
Instead of storing content in rows and columns, it stores it as binary blobs and uses metadata (like filenames or upload timestamps) for retrieval.

### When to use it ?

- You need to store large media files: Example - A video platform (e.g., YouTube) stores media in blobs, while metadata (user ID, tags, timestamps) is stored in a relational or NoSQL database.
- The data doesn’t fit a traditional database
- You want scalable, low-cost storage


### Design considerations 

- Metadata Management: Blob stores typically don’t support querying metadata. Store metadata (e.g., uploader, upload time) in a database, linked by the blob’s key or filename.
- Access Control: Blob stores typically do not have built-in user authentication or fine-grained permission systems. You'll need to handle access control explicitly to prevent unauthorized access.
- Chunking large files: Uploading or downloading large files (e.g., videos, high-res images) can fail or time out if done in a single request. Blob storage platforms support chunked or multi-part uploads, which split files into smaller parts.
