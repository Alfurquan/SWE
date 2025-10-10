# Scaling Writes

📈 Scaling Writes addresses the challenge of handling high-volume write operations when a single database or single server becomes the bottleneck. As your application grows from hundreds to millions of writes per second, individual components hit hard limits on disk I/O, CPU, and network bandwidth and interviewers love to probe these bottlenecks.

## The challenge

Many system design problems start with modest scaling requirements before the interviewer throws down the gauntlet: "how does it scale?" While you might be familiar with tools to handle the read side of the equation (e.g. read replicas, caching, etc.) the write side is often a much bigger challenge.

Bursty, high-throughput writes with lots of contention can be a nightmare to build around and there are a bunch of different choices you can make to handle them or make them worse. Interviewers love to probe bottlenecks in your solution to see how you would react to the runaway success of their next product.

## The Solution

Write scaling isn't (only) about throwing more hardware at the problem, there's a bunch of architectural choices we can make which improve the system's ability to scale. A combination of four strategies will allow you to scale writes beyond what a single, unoptimized database or server can handle:

- Vertical Scaling and Database Choices
- Sharding and Partitioning
- Handling Bursts with Queues and Load Shedding
- Batching and Hierarchical Aggregation

### Vertical Scaling and Write Optimization

The first step in handling write challenges is to make sure we've exhausted the hardware at our disposal. We want to show our interviewer that we've done our due diligence and we're not prematurely adding complexity when hardware or local software tweaks will do it.

#### Vertical Scaling

We'll start with the hardware, or "vertical scaling". Writes are bottlenecked by disk I/O, CPU, or network bandwidth. We should confirm we're hitting those walls before we proceed. Often this means we need to do some brief back-of-the-envelope math to see both (a) what our write throughput actually is, and (b) whether that fits within our hardware capabilities.

Many candidates are used to thinking about instances with 4-8 cores and a single, spinning-platted hard disk. But in many cases cloud providers and data center operators offer substantially more powerful hardware we can use before we need to re-architect our application.

*You can make the case (and most interviewers will expect or appreciate it) that some of your challenge is solved with modern hardware. We most often see this from staff+ candidates who are intuitively familiar with the edges of the performance curves. However, many interviewers have an assessment built out non-vertical scaling and they frequently will move the goalposts until you're forced to contend with scale in other ways. So make the case, but try not to get into a back-and-forth if the interviewer is not receptive.*

#### Database Choices

The next thing we might do is to consider whether our underlying data stores are optimized for the writes we're doing. Most applications include a mix of reads and writes. We need to take both types of access into consideration as we make a decision about a data store, but oftentimes write-heavy systems can be optimized by stripping away at some of the features that are only used for reads.

A great example of this is using a write-heavy database like Cassandra. Cassandra achieves superior write throughput through its append-only commit log architecture. Instead of updating data in place (which requires expensive disk seeks), Cassandra writes everything sequentially to disk. This lets it handle 10,000+ writes per second on modest hardware, compared to maybe 1,000 writes per second for a traditional relational database doing the same work.

But here's the trade-off: Cassandra's read performance isn't great. Reading data often requires checking multiple files and merging results, which can be slower than a well-indexed relational database. So you're trading read performance for write performance, which is exactly what you want in a write-heavy system.

**Write vs. Read Tension: This is a classic example of the fundamental tension in scaling writes. Optimizing for write performance often degrades read performance, and vice versa. You need to identify which is your bottleneck - writes or reads - and optimize accordingly. Different parts of your system may require different approaches.**

Other databases make similar trade-offs in different ways:

- Time-series databases like InfluxDB or TimescaleDB are built for high-volume sequential writes with timestamps (they also have built-in delta encodings to make better use of the storage)
- Log-structured databases like LevelDB append new data rather than updating in place
- Column stores like ClickHouse can batch writes efficiently for analytics workloads

Beyond this, there are other things we can do to optimize any database for writes:

- Disable expensive features like foreign key constraints, complex triggers, or full-text search indexing during high-write periods
- Tune write-ahead logging - databases like PostgreSQL can batch multiple transactions before flushing to disk
- Reduce index overhead - fewer indexes mean faster writes, though you'll pay for it on reads

**In interviews, mentioning specific database choices shows you understand the trade-offs. Don't just say "use a faster database" - explain why Cassandra's append-only writes are faster than MySQL's B-tree updates, or why you might choose a time-series database for metrics collection.**

#### Sharding and Partitioning

Ok, so we've exhausted our options with the existing hardware and need to go horizontal. What's next?

Well if one server can handle 1,000 writes/second, then 10 servers should (big should!) handle 10,000 writes/second. In the ideal state, we can distribute write volume across multiple servers so each one handles a manageable portion and win some free scalability.

We typically will call these extra servers "shards", and the many shards may actually exist as part of a logical database — we'll think of it like one. The fact that we require multiple servers is (mostly) hidden from the application.

Horizontal Sharding

A great, simple example of sharding is what Redis Cluster does. Each entry in Redis is stored with a single string key. These keys are hashed using a simple CRC function to determine a "slot number". These slot numbers are then assigned to the different nodes in the cluster.

Clients query the Redis Cluster to keep track of servers in the cluster and the slot numbers they are responsible for. When a client wants to write a value, it hashes the key to determine the slot number, looks up the server responsible for that slot, and sends the write request to that server.

Selecting a Good Partitioning Key

In practice, interviewers are expecting you to say "sharding" but they want to know how that's going to work. The most important detail you'll want to share is how to select a partitioning key. If you've chosen a good key (say, hashing the userID), all of your data will be spread evenly across the cluster, so that we've solved the problem and realized our hypothetical gain of 10x by multiplying the number of servers by 10.

**Many interviewers will accept that, if you have a good partitioning key, there's a straightforward way for clients to find the right server to access with that data. But it's not uncommon for interviewers to probe here for details on how that actually happens. Familiarizing yourself with consistent hashing, virtual nodes, and slot assignment schemes is a good way to ensure you're not caught off guard.**

But what if we select a bad key? Let's pretend if, instead of hashing the userID we decided to use the user's country as the key. We might end up with a lot of writes going to highly populated China, and very few writes going to sparse New Zealand. This means the New Zealand shard will be underutilized and the China shard will be overloaded.

Vertical Partitioning

While horizontal sharding splits rows, vertical partitioning splits columns. You separate different types of data that have different access patterns and scaling requirements. Instead of cramming everything into one massive table, you break it apart based on how the data is actually used.

Think of a social media post. In a monolithic approach, you might have a single table or database with all of the data about a post:

```sql
TABLE posts (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    content TEXT,
    media_urls TEXT[],
    created_at TIMESTAMP,
    like_count INTEGER,
    comment_count INTEGER,
    share_count INTEGER,
    view_count INTEGER,
    last_updated TIMESTAMP
);
```

This table gets hammered from all directions. Users write content, the system updates engagement metrics constantly, and analytics queries scan through massive amounts of data. Each operation interferes with the others.

With vertical partitioning, you split this into specialized tables:

```sql
-- Core post content (write-once, read-many)
TABLE post_content (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    content TEXT,
    media_urls TEXT[],
    created_at TIMESTAMP
);

-- Engagement metrics (high-frequency writes)
TABLE post_metrics (
    post_id BIGINT PRIMARY KEY,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP
);

-- Analytics data (append-only, time-series)
TABLE post_analytics (
    post_id BIGINT,
    event_type VARCHAR(50),
    timestamp TIMESTAMP,
    user_id BIGINT,
    metadata JSONB
);
```

Once we've logically separated our data, we can also move each table to a different database instance which can handle the unique workloads. Each of these databases can be optimized for its specific access pattern:

- For Post content we'll use traditional B-tree indexes and is optimized for read performance
- For Post metrics we might use in-memory storage or specialized counters for high-frequency updates
- For Post analytics we can use time-series optimized storage or database with column-oriented compression

The data modelling challenge is as much about how you logically think about your data as it is about the technical details of where it physically lives in your design!

### Handling Bursts with Queues and Load Shedding

While partitioning and sharding will get you 80% of the way to scale, they often stumble in production. Real-world write traffic isn't steady, and while scale often does smooth (Amazon's ordering volume is surprisingly stable), some bursts are common. Interviewers love to drill in on things like "what happens on black friday, when order volume 4x's" or "during new years, we triple the number of drivers on the road".

If we need to be able to 4x our write volume at peak, we can only be using 25% of our overall capacity during sleepier times. Most systems just aren't scaled this way! A lot of candidates think the solution here is "autoscaling", and autoscaling can be a great tool, but it's not panacea. Scaling up and down takes time, and worse with database systems it frequently means downtime or reduced throughput while the scaling is happening. That's exactly the opposite of what we generally want when our business is on fire.

This means we either need to (a) buffer the writes so we can process them as quickly as we can without failure, or (b) get rid of writes in a way that is acceptable to the business. Let's talk about both.

#### Write Queues for Burst Handling

The first idea that comes to mind for most candidates is to add a queue to the system, using something like Kafka or SQS. This decouples write acceptance from write processing, allowing the system to handle the writes as quickly as possible.

Because queues are inherently async, it means the app server only knows that the write was recorded in the queue, not that it was successfully written to our database. In most cases, this means that clients will often need a way to call back to check the write was eventually made to the database. No problem, for some cases!

This approach provides a few benefits, but the most important is burst absorption: the queue acts as a buffer, smoothing out traffic spikes. Your database processes writes at a steady rate while the queue handles bursts.

But queues are only a temporary solution, if the app server continues to write to the queue faster than records can be written to the database, we get unbounded growth of our queue. Writes take longer and longer to be processed.

And while we might be able to scale our database to handle the increased load (and backlog we've accumulated into the queue), oftentimes this actually makes the problem worse as our users grow increasingly restless.

**Queues are a powerful tool but candidates frequently fail to consider situations where they mask an underlying problem. Use queues when you expect to have bursts that are short-lived, not to patch a database that can't handle the steady-state load.**

It's important to understand at the requirements stage what tolerance we have for delayed writes or inconsistent reads. In many cases, systems can tolerate a bit of delay, especially for rare cases where traffic is highest. If this is the case, using a queue may be a good way to go! But be careful of introducing a queue which disturbs key functional or non-functional requirements.

#### Load Shedding Strategies

Another option for handling bursts may seem like a cop-out, but it's actually a powerful tool. When your system is overwhelmed, you need to decide which writes to accept and which to reject. This is called load shedding, and it's better than letting everything fail.

Load shedding tries to make a determination of which writes are going to be most important to the business and which are not. If we can drop the less important writes, we can keep the system running and the more important writes will still be processed.

Consider problems like Strava or Uber where users are reporting their locations at regular intervals. If we have an excess number of users, adding a queue to the system sets us up for a blown out queue. But if we take a step back we can realize that users are going to keep calling back every few seconds to send us their location. If we drop one write, we should expect another write to be sent in a few seconds that will be fresher than the one we dropped!

A simple solution here is to simply drop the least useful writes during times of system overload. For Uber these might be location updates that are within seconds of a previous update. For an analytics system, we might drop impressions for a while to ensure we can process the more important clicks.

Load shedding is a powerful tool, but it requires a deep understanding of the business requirements. You need to be able to make informed decisions about which writes are important and which can be dropped without significantly impacting the user experience or business goals.

### Batching and Hierarchical Aggregation

While previous solutions accept that the existing writes are given, frequently we can change the structure of the writes to make them easier to process. Individual write operations have overhead like network round trips, transaction setup, index updates. Additionally, most databases process batches more efficiently than individual writes. When our database becomes the bottleneck, we can look upstream to see how we can make the incoming data easier to process.

#### Batching

One example of this is batching writes together. Instead of processing writes one by one, you batch multiple writes together to amortize this overhead. This can be done at the application layer, as an in-between process, or even at the database layer.

For example, instead of sending 1,000 individual insert statements to a database, you can send a single batch insert statement that includes all 1,000 records. This reduces the number of round trips and allows the database to optimize the write operation.

```sql
INSERT INTO events (user_id, event_type, timestamp) VALUES
(1, 'click', '2024-01-01 12:00:00'),
(2, 'view', '2024-01-01 12:00:01'),
(3, 'purchase', '2024-01-01 12:00:02'),
...
(1000, 'click', '2024-01-01 12:16:39');
```

This single statement is much more efficient than 1,000 separate insert statements.

Batching can also be done at the application layer. For example, if you're collecting metrics from users, you might buffer them in memory and send them to the server in batches every few seconds instead of sending each metric as it occurs.
This reduces the number of requests the server has to handle and allows it to process the metrics more efficiently.

```// Pseudocode for batching metrics
buffer = []
function collectMetric(metric) {
    buffer.push(metric)
    if (buffer.length >= BATCH_SIZE || timeSinceLastSend() >= MAX_WAIT_TIME) {
        sendBatch(buffer)
        buffer = []
    }
}
```

Another example is reading from queue and processing and writing to database. Instead of processing each message individually, you can read a batch of messages from the queue and write them to the database in a single operation.

```python
# Pseudocode for processing messages in batches
while True:
    messages = queue.readBatch(BATCH_SIZE)
    if messages:
        database.writeBatch(messages)
```

This approach is especially useful for high-frequency events where individual writes are small and frequent.

#### Hierarchical Aggregation

This last strategy applies in some of the most extreme cases. For high-volume data like analytics and stream processing, you often don't need to store individual events and instead need aggregated views. The important insight is that these views can be built up incrementally. Hierarchical aggregation processes data in stages, reducing volume at each step.

Let's talk about a concrete example. In live video streams, viewers are often able to both comment and like comments on the stream. Whenever a viewer performs either of these events, all other users need to be notified of it. This creates an ugly situation if there are millions of viewers, millions of users are writing, and all of the writes need to be to sent to all of their peers!

But wait, we can simplify this a bit. All of our viewers are looking for the same, eventually consistent view: they want to see all the latest comments and the counts associated with them. We'll assign the users to broadcast nodes using a consistent hashing scheme. Instead of writing independently to each of them, we can write out to broadcast nodes which can forward updates to their respective viewers.

Now instead of writing to N viewers, we only have to write to M broadcast nodes. Great! But we still have one more problem, our root processor is receiving the incoming events from all the viewers. Fortunately, we can handle this in much the same way:

The write processor we call out to can be chosen based on the ID of the comment (or, for likes, the comment ID it is liking). The write processors can then aggregate the likes on the comments they own, over a window, and forward a batch of updates to the root processor, who only needs to merge them.

By aggregating the data with the write processors and dis-aggregating it with the broadcast nodes, we've substantially reduced the number of writes that any one system needs to handle at the cost of some latency introduced by adding steps. And that's the heart of hierarchical aggregation!

## When to use in an interview

An example of a strong candidate's response:

- "With millions of users posting content, we'll quickly hit write bottlenecks. Let me see what kind of write throughput we're dealing with ...Ok this is significant! I'll come back to that in my deep dives."
- "For the posting writes, I think it's sensible for us to partition our database by user ID. This will spread the load evenly across our shards. We'll still need to handle situations where a single user is posting a lot of content, but we can handle that with a queue and rate limits."

### Common interview scenarios

- Instagram/Social Media - Perfect for demonstrating sharding by user ID for posts, vertical partitioning for different data types (user profiles, posts, analytics), and hierarchical storage for older posts.

- News Feeds - News feeds require careful tuning between write volume for celebrity posts which need to be written to millions of followers and read volume when those millions of use come to consume their feed.

- Search Applications - Search applications are often write-heavy with substantial preprocessing required in order to make the search results quick to retrieve. Partitioning and batching are key to making this work.

- Live Comments - Live comments are a great example of a system which can benefit from hierarchical aggregation to avoid an intractable all-to-all problem where millions of viewers need a shared view of the activities of millions of their peers.

### When not to use in an interview

Be careful of employing write scaling strategies when no scaling is necessary! If you see something that looks like it might be a bottleneck, that's a good time to use some quick back-of-the-envelope math to see if it's worth the effort.

Each of these strategies comes with tradeoffs. Queues mean eventual consistency and delay, partitioning means the read path may be compromised, batching adds latency and moving pieces. Show your interviewer that you're cognizant of these tradeoffs before making a proposal. The worst case is creating a problem where one doesn't exist!

## Common deep dives

### "How do you handle resharding when you need to add more shards?"

This is the classic operational challenge with sharding. You started with 8 shards, but now you need 16. How do you migrate data without downtime?

The naive approach is to take the system offline, rehash all data, and move it to new shards. But this creates hours of downtime for large datasets.

Production systems use gradual migration which targets writes to both locations (e.g. the shard we're migrating from and the shard we're migrating to). This allows us to migrate data gradually while maintaining availability.

**The dual-write phase ensures no data is lost during migration. You write to both old and new shards, but read with preference for the new shard. This allows you to migrate data gradually while maintaining availability.**

### "What happens when you have a hot key that's too popular for even a single shard?"

We talked earlier about how we need to spread load evenly across our shards. Sometimes, in spite of even the best choices around keys, a shard can still have a disproportionate traffic pointed at it. Consider a viral tweet that receives 100,000 likes per second. Even though we've spread out our tweets evenly across our shards, this tweet may still cause us problems! Even dedicating an entire shard to this single tweet isn't enough.

- Split all keys: The first option is to split all keys a fixed k number of times. This is a pretty big hammer, but it's the simplest solution. Instead of having each tweet's likes be stored on a single shard, we can instead store them across multiple shards.

## Conclusion

Write scaling comes down to four fundamental strategies that work together: vertical scaling and database choices, sharding and partitioning, queues and load shedding, and batching and multi-step reducers. The most successful interviews don't overcomplicate these concepts, they look for places where they are required and apply them strategically.

- Sharding and partitioning is a great place to start when you're trying to scale your system. It's a simple strategy that can give you a lot of bang for your buck, and most interviews are going to be expecting it.

- If you're dealing with high volume analytics or numeric data, batching and hierarchical aggregation can give you immediate 5-10x improvements.

- Finally, queues and load shedding are great tools when requirements allow for async processing or even dropping requests. Keep them in mind as you're navigating requirements to see if they're a good fit.

---