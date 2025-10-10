# Scaling Write Operations - Exercises

## Scenario 1: Twitter-like Social Media Platform

You're designing a Twitter clone where users can post tweets, follow other users, and interact with posts (likes, retweets, replies). During peak hours, you have 10 million users posting 50 million tweets per day. Popular tweets can receive 100,000+ interactions per minute. The system needs to handle both the initial writes and the high-frequency engagement updates.

Your task: How do you scale the write operations for posts and user interactions? What's your strategy?

### Solution

"Looking at 50M tweets/day, that's ~580 tweets/second normally, up to 1,740 at peak. A single database typically handles ~1K writes/second, so I need horizontal scaling.

I'll shard by user_id for tweet creation - this spreads writes evenly since users post relatively uniformly.

For engagement updates, popular tweets create hot key problems. I'll batch these updates - collect likes for 1-2 seconds then write in batches. This reduces 1,667 individual writes to maybe 100 batch operations.

Major challenge: Cross-shard queries become complex, but the write scaling is worth it."

---

## Scenario 2: IoT Sensor Data Collection

You're building a system to collect data from millions of IoT sensors (temperature, humidity, GPS locations, etc.). Each sensor sends data every 30 seconds. You have 5 million sensors generating approximately 14.4 million data points per hour. During peak times or sensor malfunctions, you might receive bursts of 10x normal traffic.

Your task: How do you handle this massive write volume while ensuring data isn't lost during traffic spikes?

### Solution

Step 1: Load calculation

Lets first begin by calculating the load

We have 5 million sensors generating 14.4 million data points per hour which makes it around 
14.4 / 3600 = 4000 data points per second which is a huge number.

So one single DB won't be enough.

Step 2: What are we actually writing

Here we are writing sensor data points from IoT sensors like temperature, humidity, GPS etc.

Step 3: Database selection

Since the data is sent at regular intervals over time, we can use a time series database here like InfluxDB as they are built for high-volume sequential writes with timestamps

Step 4: Optimizations

Since we will be receiving huge amount of data like 51840 million data points per second, we will need multiple databases. We can use techniques like sharding where we can shard the database by sensorId and timestamp to avoid load on one database server.

Step 5: Handling bursts

At peak times and during sensor malfunctions, we need to handle 10x traffic. We can employ a message queue to buffer the writes and process them in batches. This means lets say if we 1K writes at one time and if we batch 100 writes into one, the no of write requests goes down from 1K to just 10. This is just a small example I took to explain the relevance of batching writes here.

Load shedding strategies

During sensor malfunctions (10x traffic = 40K/second):

- Keep critical sensors (safety, security)
- Drop redundant readings (multiple temp sensors in same room)
- Implement backpressure to slow down non-critical sensors

---

## Scenario 3: Live Streaming Chat System

You're building the chat system for a platform like Twitch where popular streamers can have 100,000+ concurrent viewers all sending messages. During big events, a single stream might receive 10,000+ messages per minute. All viewers need to see messages in near real-time.

Your task: How do you handle the massive write volume of chat messages while ensuring real-time delivery to all viewers?

### Solution

Step 1: Load calculation

Lets first begin by calculating the load

System has around 1M concurrent viewers all sending messages, during big events a single stream receive 10K messages per minutes which is about 10K / 60 = 166 messages per seconds. 

One DB can be enough here

Step 2: What are we actually writing

We will be writing messages and then stream those messages in real time to concurrent viewers

Step 3: Database selection

We can use any relational database like PostgreSQL for this.

Step 4: Approach to handle write volume

Since we will be serving streaming data here i.e. messages in real time to users, we can use Hierarchial aggregation and batching techniques.

All of our viewers are looking for the same, eventually consistent view: messages from the stream.
We'll assign the users to broadcast nodes using a consistent hashing scheme. Instead of writing independently to each of them, we can write out to broadcast nodes which can forward updates to their respective viewers.

Now instead of writing to N viewers, we only have to write to M broadcast nodes.
This will help us in reducing the no of writes.

Further we can also employ batching on the broadcast nodes to reduce the write load, we can batch on userids or group messages to be delivered to same location and process them in one batch.

More enhanced

**Core Insight**: This isn't a write scaling problem (166 msg/sec is easy) - 
it's a fan-out problem (100K viewers need each message).

**Hierarchical Distribution**:

- Messages → Regional broadcast nodes (by geography)
- Broadcast nodes → WebSocket connections to viewers
- Reduces 16M operations to ~166 × 10 nodes = 1,660 operations

**Optimizations**:

- Batch messages at broadcast nodes (send 10 messages together)
- Use Redis for active chat, PostgreSQL for history
- WebSocket connections for real-time delivery

---

## Scenario 5: E-commerce Inventory & Order System

You're designing the backend for a large e-commerce platform during Black Friday. You need to handle millions of orders, inventory updates, payment processing, and order state changes. Peak traffic is 50,000+ orders per minute with frequent inventory updates as items sell out.

Your task: How do you scale writes for orders and inventory while preventing overselling and maintaining data consistency?

### Solution

Step 1: Load calculation

Lets first begin by calculating the load

Peak traffic is 50K orders per minute which makes it 50000 / 60 ~= 900 orders/seconds

So, a single DB can suffice the load here

Step 2: What are we writing

We would be writing order details as well as updating inventory of product items and changing order states.

Step 3: Database selection

We can use any relational database like PostgreSQL to store data as they offer strong ACID properties and this is what we need for this use case

Step 4: Scaling writes

A single DB can handle 900 writes per second. During peak hours, we can use a buffer like a message queue to process the writes in batches. This can help avoid overwhelming the database with too much writes.

If the writes can't be handled by a single db, we can shard the database and use customer_id as shard key. This will help distribute the writes to multiple databases and help reducing load on a single database

Step 5: Prevent overselling and maintaining data consistency

Database level

Since a single database can handle the load we computed, we can use transactions in database to perform all the operations. This will ensure all operations are atomic and the database is never in an inconsistent state.

```sql
BEGIN TRANSACTION

INSERT INTO ORDERS ...

UPDATE PRODUCT SET QUANTITY = QUANTITY - 1 WHERE ID = ...

COMMIT
```

Transactions will help make sure both operations succeed, if anyone fails, database will be rolled back to previous state.

For multiple database scenarios, we can use SAGA pattern where we can divide the operations into multiple steps which can be performed independently.

To prevent overselling under concurrent updates, we can use an optimistic concurrency control pattern (conditional update) or a stock-reservation model where decrements occur in an eventually consistent but conflict-free counter (like Redis or Spanner).

Step 6: Failure handling

We’d also employ idempotency tokens for order writes to handle retries safely in case of transient DB or service failures.

If payment succeeds but inventory update fails, SAGA compensating transactions can trigger a refund or rollback workflow to maintain global consistency

---