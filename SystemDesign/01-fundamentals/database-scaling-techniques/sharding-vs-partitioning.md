# Sharding vs Partitioning

Sharding and partitioning are two of the most commonly confused concepts in system design.
At first glance, they may seem similar, and people often use them interchangeably. But they are not the same.
Both are techniques to divide and scale large databases; however, they differ in how the data is divided.

Simply put, partitioning typically means breaking down database tables within a single server while sharding is about distributing data across multiple servers.

## What is partitioning ?

Partitioning is the process of splitting a large database table (or index) into smaller, more manageable chunks called partitions, all within the same database instance.

Each partition holds a subset of the data. This means the database can skip scanning the entire table and instead operate only on the relevant partition, which significantly improves performance for queries that filter on the partition key.

### Example: Partitioning a logs Table by Month

Imagine you have a table called logs that stores application logs with millions of rows. Each row has a timestamp column.

Instead of keeping all log entries in a single massive table, you can partition it by month using the timestamp column as the partition key.

So internally, the database will create partitions like:

logs_2024_01 for January 2024
logs_2024_02 for February 2024
logs_2024_03 for March 2024...and so on.

```SQL
SELECT * FROM logs 
WHERE timestamp BETWEEN '2024-03-01' AND '2024-03-31';
```

The database knows it only needs to scan the logs_2024_03 partition instead of scanning every row in the full logs table. This is called partition pruning, and it can drastically reduce disk I/O and speed up query execution.

### Vertical vs. Horizontal Partitioning

- Vertical partitioning means splitting a table by columns. Different sets of columns are stored in separate tables, but they’re still linked by the same primary key.
- Horizontal partitioning means dividing a table by rows. Each partition holds a subset of the rows, usually based on a condition like a value range or the result of a hash function. The table’s schema stays the same across all partitions, only the data rows are split.

### Common Horizontal Partitioning Strategies

- Range Partitioning: In range partitioning, each partition is responsible for a continuous range of values from the partition key.
- Hash Partitioning: Here, a hash function is applied to the partition key to evenly distribute rows across a fixed number of partitions.
- Composite Partitioning: This is a hybrid approach, combining two strategies, most commonly range + hash.

## What is sharding ?

Sharding is the process of splitting your data and distributing them across multiple physically separate database servers (or instances).

Each of these servers—called a shard—stores only a subset of the overall dataset.
`Sharding = Horizontal Partitioning + Distribution Across Servers`
