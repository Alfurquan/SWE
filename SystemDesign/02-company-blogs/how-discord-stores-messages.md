# How Discord Stores Billions of Messages

Discord chooses Cassandra for storing billions of chat messages.

## Earlier Version

The original version of Discord was built in just under two months in early 2015. Arguably, one of the best databases for iterating quickly is MongoDB. Everything on Discord was stored in a single MongoDB replica set and this was intentional, but they also planned everything for easy migration to a new database (they knew they were not going to use MongoDB sharding because it is complicated to use and not known for stability).

The messages were stored in a MongoDB collection with a single compound index on channel_id and created_at. Around November 2015, Discord reached 100 million stored messages and at this time they started to see the expected issues appearing: the data and the index could no longer fit in RAM and latencies started to become unpredictable. It was time to migrate to a database more suited to the task.

## Choosing the right database

Before choosing the new database, they had to understand the read/write patterns and why they were having problems with current solution

- It quickly became clear that reads were extremely random and read/write ratio was about 50/50.
- Voice chat heavy Discord servers send almost no messages. This means they send a message or two every few days. The problem is that even though this is a small amount of messages it makes it harder to serve this data to the users. Just returning 50 messages to a user can result in many random seeks on disk causing disk cache evictions.
- Large public Discord servers send a lot of messages. They have thousands of members sending thousands of messages a day and easily rack up millions of messages a year. They almost always are requesting messages sent in the last hour and they are requesting them often. Because of that the data is usually in the disk cache.

Reasoning behind choosing Cassandra as the database

Cassandra was the only database that fulfilled all of the requirements. We can just add nodes to scale it and it can tolerate a loss of nodes without any impact on the application. Large companies such as Netflix and Apple have thousands of Cassandra nodes. Related data is stored contiguously on disk providing minimum seeks and easy distribution around the cluster. It’s backed by DataStax, but still open source and community driven.

## Data Modelling

The best way to describe Cassandra to a newcomer is that it is a KKV store. The two Ks comprise the primary key. The first K is the partition key and is used to determine which node the data lives on and where it is found on disk. The partition contains multiple rows within it and a row within a partition is identified by the second K, which is the clustering key. The clustering key acts as both a primary key within the partition and how the rows are sorted. You can think of a partition as an ordered dictionary. These properties combined allow for very powerful data modeling.

Remember that messages were indexed in MongoDB using channel_id and created_at? channel_id became the partition key since all queries operate on a channel, but created_at didn’t make a great clustering key because two messages can have the same creation time.
Luckily every ID on Discord is actually a Snowflake (chronologically sortable). The primary key became (channel_id, message_id), where the message_id is a Snowflake. This meant that when loading a channel we could tell Cassandra exactly where to range scan for messages.

Simplified version of the `Message` table

```sql

CREATE TABLE messages (
  channel_id bigint,
  message_id bigint,
  author_id bigint,
  content text,
  PRIMARY KEY (channel_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

When existing messages began to be imported into Cassandra, warnings immediately started appearing in the logs indicating that partitions exceeding 100 MB in size had been found. This was surprising, given that Cassandra is advertised to support partitions up to 2 GB. However, it soon became apparent that capability does not imply advisability. Large partitions were found to place significant garbage collection pressure on Cassandra during compaction, cluster expansion, and other operations. Moreover, such partitions prevent their data from being evenly distributed across the cluster. It therefore became evident that the size of partitions needed to be constrained, as a single Discord channel can persist for years and grow indefinitely in size.

A decision was made to bucket the messages by time. An analysis of the largest Discord channels was conducted, and it was determined that storing approximately ten days of messages within a single bucket would keep partition sizes comfortably below 100 MB. The buckets were required to be derivable from either the message_id or a timestamp.

Cassandra partition keys can be compounded, so the new primary key became ((channel_id, bucket), message_id).

```sql

CREATE TABLE messages (
   channel_id bigint,
   bucket int,
   message_id bigint,
   author_id bigint,
   content text,
   PRIMARY KEY ((channel_id, bucket), message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

## Dark Launch

Introducing a new system into production is always accompanied by a degree of risk, so efforts were made to test it without impacting users. The code was configured to perform double reads and writes to both MongoDB and Cassandra.

Immediately after the launch, errors began appearing in the bug tracker indicating that the author_id field was null. This was unexpected, as the field was defined as required.

### Eventual Consistency

Cassandra is an AP database which means it trades strong consistency for availability which is something we wanted. It is an anti-pattern to read-before-write (reads are more expensive) in Cassandra and therefore everything that Cassandra does is essentially an upsert even if you provide only certain columns. You can also write to any node and it will resolve conflicts automatically using “last write wins” semantics on a per column basis.

In a scenario where one user edited a message while another simultaneously deleted the same message, a row was left containing only the primary key and text. This occurred because all writes in Cassandra are treated as upserts. Two possible solutions were identified to address this issue:

- The entire message could be written back during an edit operation. However, this approach carried the risk of resurrecting deleted messages and increasing the likelihood of conflicts during concurrent writes to other columns.

- Alternatively, corrupted messages could be detected and deleted from the database.

The second option was chosen. This was implemented by designating a required column—author_id in this case—and deleting the message whenever its value was found to be null.

During the resolution of this issue, it was observed that the write operations were being handled inefficiently. Because Cassandra is an eventually consistent system, it cannot immediately delete data. Instead, deletions must be replicated across other nodes, even if some nodes are temporarily unavailable. Cassandra achieves this by representing deletions as a special kind of write known as a tombstone. When data is read, Cassandra simply skips over any tombstones it encounters. These tombstones persist for a configurable duration (ten days by default) and are permanently removed during compaction once this period has elapsed.

In Cassandra, deleting a column and writing a null value to it produce the same effect—both actions generate a tombstone. Since all writes are upserts, a tombstone is created even when a null value is written for the first time. In practice, the message schema consisted of sixteen columns, but an average message contained values for only four of them. As a result, twelve unnecessary tombstones were being written most of the time.

## The Big Surprise

Everything proceeded smoothly, and Cassandra was rolled out as the primary database, with MongoDB being phased out within a week. The system continued to function flawlessly for approximately six months—until one day, Cassandra became unresponsive.

It was observed that Cassandra was repeatedly executing 10-second “stop-the-world” garbage collection (GC) cycles, though the cause was initially unknown. Further investigation revealed that a Discord channel was taking nearly 20 seconds to load. The culprit was identified as the Puzzles & Dragons Subreddit public Discord server. Since the server was public, it was joined for inspection. To everyone’s surprise, the affected channel contained only a single message. It then became evident that millions of messages had been deleted through the API, leaving behind only one.

As previously discussed, Cassandra handles deletions using tombstones. When the channel was loaded, Cassandra was required to scan through millions of these tombstones—even though only one message remained—causing excessive garbage generation that the JVM was unable to reclaim quickly enough.

The issue was resolved through the following measures:

The lifespan of tombstones was reduced from ten days to two days, as Cassandra repairs (an anti-entropy process) were already being performed nightly on the message cluster.

The query logic was updated to track and skip empty buckets for each channel. As a result, if the same query occurred again, Cassandra would, at worst, need to scan only the most recent bucket.

---

# 🧭 The Evolution Journey

---

## Phase 1: MongoDB (Early 2015)

**Why MongoDB initially:** Fast iteration, single replica set  
**The problem:** 100M messages → data + index couldn't fit in RAM → unpredictable latencies  
**Key lesson:** Plan for migration from day one, even when using "good enough" solutions  

---

## Phase 2: Database Selection

### Read/Write Patterns Analysis
- 50/50 read/write ratio  
- Extremely random read patterns  
- Two types of servers:
  - Voice-heavy (few messages)  
  - Large public (millions of messages)

### Why Cassandra Won
- Linear scalability by adding nodes  
- Fault tolerance (node loss doesn't impact the app)  
- Data locality (related data stored contiguously)  
- Proven at scale (Netflix, Apple use thousands of nodes)  

---

## Data Modeling Evolution

### Version 1: Simple Schema
- `channel_id` as partition key (all queries are per-channel)  
- `message_id` (Snowflake ID) as clustering key for chronological ordering  
- **Problem:** Large partitions (>100MB) caused GC pressure  

### Version 2: Time Bucketing
- Added bucket for ~10 days of messages per partition  
- Keeps partitions under 100MB  
- **Key insight:** Even if Cassandra supports 2GB partitions, it doesn’t mean you should use them  

---

## Production Lessons

### Dark Launch Strategy
- Double reads/writes to both MongoDB and Cassandra  
- Gradual migration with fallback capability  
- **Lesson:** Always test new systems in production with real traffic  

### Eventual Consistency Challenges
- **The bug:** `author_id` becoming null due to concurrent edit/delete operations  
- **Root cause:** Cassandra’s upsert behavior + “last write wins”  
- **Solution:** Designate required columns; delete corrupted messages  
- **Optimization:** Avoid writing null values (they create unnecessary tombstones)  

---

## The Tombstone Crisis

**The disaster:** Channel with millions of deleted messages taking 20 seconds to load  
**Root cause:** Scanning millions of tombstones to find one message  

### Solutions
1. Reduced tombstone TTL from 10 days to 2 days  
2. Tracked empty buckets to skip them in queries  

---

## Key Takeaways for System Design Interviews

### 1. Database Selection Process
- Analyze access patterns first: read/write ratio, randomness, data locality  
- Consider operational requirements: scaling, fault tolerance, team expertise  
- Plan for evolution: start simple, but design for migration  

### 2. Data Modeling Best Practices
- **Partition key selection:** Based on query patterns (`channel_id` for per-channel queries)  
- **Clustering key design:** Use chronologically sortable IDs (`Snowflake`)  
- **Partition size management:** Bucket data to prevent hot/large partitions  
- **Real-world constraints:** Theory vs practice (2GB vs 100MB partitions)  

### 3. Production Deployment Strategies
- **Dark launches:** Run new systems alongside old ones with real traffic  
- **Gradual rollouts:** Phase out old systems incrementally  
- **Monitor edge cases:** Large channels, deletion patterns, GC pressure  

### 4. Handling Distributed System Challenges
- **Eventual consistency trade-offs:** Accept for availability, handle edge cases  
- **Tombstone management:** Understand deletion implications in LSM trees  
- **Performance monitoring:** Watch for unexpected patterns (e.g., mass deletions)  

---

## Interview Application

When designing a chat system:

1. **Start with access patterns:**  
   “Messages are queried per channel, chronologically.”
2. **Choose an appropriate database:**  
   “Cassandra for high write throughput and availability.”
3. **Design schema thoughtfully:**  
   “Partition by `channel_id`, cluster by `message_id`.”
4. **Address scaling concerns:**  
   “Bucket by time to prevent large partitions.”
5. **Consider operational challenges:**  
   “Handle tombstones, monitor for edge cases.”

---

## 🎯 This Case Study Demonstrates

- Real-world database migration challenges  
- The importance of understanding data access patterns  
- How theoretical limits differ from practical constraints  
- The complexities of eventually consistent systems  

---
