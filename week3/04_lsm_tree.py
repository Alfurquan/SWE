"""
Week 3 - Problem 4: LSM Tree for Time-Series Database
Difficulty: Hard | Time Limit: 90 minutes | Google L5 Database Internals

PROBLEM STATEMENT:
Implement LSM (Log-Structured Merge) tree for time-series data

OPERATIONS:
- write(timestamp, metric, value): Write time-series point
- read(metric, start_time, end_time): Range query
- compact(): Merge SSTables and remove tombstones
- flush(): Flush memtable to disk
- delete(metric, timestamp): Mark for deletion

REQUIREMENTS:
- Write-optimized storage (append-only)
- Efficient range queries for time-series
- Background compaction process
- Compression for similar timestamps

ALGORITHM:
LSM tree, memtable, SSTable, compaction strategies

REAL-WORLD CONTEXT:
Apache Cassandra, RocksDB, InfluxDB, time-series databases

FOLLOW-UP QUESTIONS:
- Compaction strategy optimization?
- Write amplification minimization?
- Query optimization techniques?
- Distributed LSM trees?

EXPECTED INTERFACE:
lsm_tree = LSMTree()
lsm_tree.write(1000, "cpu_usage", 75.5)
lsm_tree.write(1060, "cpu_usage", 80.2)
data = lsm_tree.read("cpu_usage", start=1000, end=1100)
lsm_tree.compact()
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
