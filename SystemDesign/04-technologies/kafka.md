# Kafka

Apache Kafka is an open-source distributed event streaming platform that can be used either as a message queue or as a stream processing system. Kafka excels in delivering high performance, scalability, and durability. It’s engineered to handle vast volumes of data in real-time, ensuring that no message is ever lost and that each piece of data is processed as swiftly as possible.

## Basic terminology

A Kafka cluster is made up of multiple brokers. These are just individual servers (they can be physical or virtual). Each broker is responsible for storing data and serving clients. The more brokers you have, the more data you can store and the more clients you can serve.

Each broker has a number of partitions. Each partition is an ordered, immutable sequence of messages that is continually appended to -- think of like a log file. Partitions are the way Kafka scales as they allow for messages to be consumed in parallel.

A topic is just a logical grouping of partitions. Topics are the way you publish and subscribe to data in Kafka. When you publish a message, you publish it to a topic, and when you consume a message, you consume it from a topic. Topics are always multi-producer; that is, a topic can have zero, one, or many producers that write data to it.

**So what is the difference between a topic and a partition?**

A topic is a logical grouping of messages. A partition is a physical grouping of messages. A topic can have multiple partitions, and each partition can be on a different broker. Topics are just a way to organize your data, while partitions are a way to scale your data.

Producers are the ones who write data to topics, and consumers are the ones who read data from topics. While Kafka exposes a simple API for both producers and consumers, the creation and processing of messages is on you, the developer. Kafka doesn't care what the data is, it just stores and serves it.

## How Kafka works ?

- When an event occurs, the producer formats a message, also referred to as a record, and sends it to a Kafka topic. A message consists of one required field, the value, and three optional fields: a key, a timestamp, and headers. The key is used to determine which partition the message is sent to, and the timestamp is used to order messages within a partition. Headers, like HTTP headers, are key-value pairs that can be used to store metadata about the message.

- When a message is published to a Kafka topic, Kafka first determines the appropriate partition for the message. This partition selection is critical because it influences the distribution of data across the cluster. This is a two-step process:

    - **Partition Determination:** Kafka uses a partitioning algorithm that hashes the message key to assign the message to a specific partition. If the message does not have a key, Kafka can either round-robin the message to partitions or follow another partitioning logic defined in the producer configuration. This ensures that messages with the same key always go to the same partition, preserving order at the partition level.

    - **Broker Assignment:** Once the partition is determined, Kafka then identifies which broker holds that particular partition. The mapping of partitions to specific brokers is managed by the Kafka cluster metadata, which is maintained by the Kafka controller (a role within the broker cluster). The producer uses this metadata to send the message directly to the broker that hosts the target partition.

- Each partition in Kafka functions essentially as an append-only log file. Messages are sequentially added to the end of this log, which is why Kafka is commonly described as a distributed commit log. This append-only design is central to Kafka’s architecture, providing several important benefits:

    - **Immutability:** Once written, messages in a partition cannot be altered or deleted. This immutability is crucial for Kafka’s performance and    reliability. It simplifies replication, speeds up recovery processes, and avoids consistency issues common in systems where data can be changed.
    
    - **Efficiency:** By restricting operations to appending data at the end of the log, Kafka minimizes disk seek times, which are a major bottleneck in many storage systems.
    
    - **Scalability:** The simplicity of the append-only log mechanism facilitates horizontal scaling. More partitions can be added and distributed across a cluster of brokers to handle increasing loads, and each partition can be replicated across multiple brokers to enhance fault tolerance.

- Each message in a Kafka partition is assigned a unique offset, which is a sequential identifier indicating the message’s position in the partition. This offset is used by consumers to track their progress in reading messages from the topic. As consumers read messages, they maintain their current offset and periodically commit this offset back to Kafka. This way, they can resume reading from where they left off in case of failure or restart.

- Once a message is published to the designated partition, Kafka ensures its durability and availability through a robust replication mechanism. Kafka employs a leader-follower model for replication, which works as follows:

    - **Leader Replica Assignment:** Each partition has a designated leader replica, which resides on a broker. This leader replica is responsible for handling all read and write requests for the partition. The assignment of the leader replica is managed centrally by the cluster controller, which ensures that each partition’s leader replica is effectively distributed across the cluster to balance the load.

    - **Follower Replication:** Alongside the leader replica, several follower replicas exist for each partition, residing on different brokers. These followers do not handle direct client requests; instead, they passively replicate the data from the leader replica. By replicating the messages received by the leader replica, these followers act as backups, ready to take over should the leader replica fail.

    - **Synchronization and Consistency:** Followers continuously sync with the leader replica to ensure they have the latest set of messages appended to the partition log. This synchronization is crucial for maintaining consistency across the cluster. If the leader replica fails, one of the follower replicas that has been fully synced can be quickly promoted to be the new leader, minimizing downtime and data loss.

    - **Controller's Role in Replication:** The controller within the Kafka cluster manages this replication process. It monitors the health of all brokers and manages the leadership and replication dynamics. When a broker fails, the controller reassigns the leader role to one of the in-sync follower replicas to ensure continued availability of the partition.

- Last up, consumers read messages from Kafka topics using a pull-based model. Unlike some messaging systems that push data to consumers, Kafka consumers actively poll the broker for new messages at intervals they control.

## When to use Kafka in your interview

Kafka can be used as either a message queue or a stream.
The key difference between the two lies in how consumers interact with the data. In a message queue, consumers typically pull messages from the queue when they are ready to process them. In a stream, consumers continuously consume and process messages as they arrive in real-time, similar to drinking from a flowing river.

**Consider adding a message queue to your system when:**

- You have processing that can be done asynchronously. YouTube is a good example of this. When users upload a video we can make the standard definition  video available immediately and then put the video (via link) a Kafka topic to be transcoded when the system has time.

- You need to ensure that messages are processed in order. We could use Kafka for our virtual waiting queue in Design Ticketmaster which is meant to ensure that users are let into the booking page in the order they arrived.

- You want to decouple the producer and consumer so that they can scale independently. Usually this means that the producer is producing messages faster than the consumer can consume them. This is a common pattern in microservices where you want to ensure that one service can't take down another.

**Streams are useful when:**

- You require continuous and immediate processing of incoming data, treating it as a real-time flow.

- Messages need to be processed by multiple consumers simultaneously. In Design FB Live Comments we can use Kafka as a pub/sub system to send comments to multiple consumers.

## What you should know about Kafka for System Design Interviews

### Scalability

Let's start by understanding the constraints of a single Kafka broker. It's important in your interview to estimate the throughput and number of messages you'll be storing in order to determine whether we need to worry about scaling in the first place.
First, there is no hard limit on the size of a Kafka message as this can be configured via message.max.bytes. However, it is recommended to keep messages under 1MB to ensure optimal performance via reduced memory pressure and better network utilization.

**It's a common anti-pattern in system design interviews to store large blobs of data in Kafka. Kafka is not a database, and it's not meant to store large files. It's meant to store small messages that can be processed quickly.
For example, when designing YouTube, we need to perform post-processing on videos after uploading to chunk and transcode them. Naively, you might place the videos in Kafka so that the chunk/transcoding worker can pull them off the queue asynchronously and process them. This is not a good idea. Instead, you should store the videos in a distributed file system like S3 and place a message in Kafka with the location of the video in S3. This way, the Kafka message is small and serves as a pointer to the full video in S3.**

**How can we handle hot partitions?**

Interviewers love to ask this question. Consider an Ad Click Aggregator where Kafka stores a stream of click events from when users click on ads. Naturally, you would start by partitioning by ad id. But when Nike launches their new Lebron James ad, you better believe that partition is going to be overwhelmed with traffic and you'll have a hot partition on your hands.

There are a few strategies to handle hot partitions:

- **Random partitioning with no key:** If you don't provide a key, Kafka will randomly assign a partition to the message, guaranteeing even distribution. The downside is that you lose the ability to guarantee order of messages. If this is not important to your design, then this is a good option.

- **Random salting:** We can add a random number or timestamp to the ad ID when generating the partition key. This can help in distributing the load more evenly across multiple partitions, though it may complicate aggregation logic later on the consumer side. This is often referred to as "salting" the key.

- **Use a compound key:** Instead of using just the ad ID, use a combination of ad ID and another attribute, such as geographical region or user ID segments, to form a compound key. This approach helps in distributing traffic more evenly and is particularly useful if you can identify attributes that vary independently of the ad ID.

- **Back pressure:** Depending on your requirements, one easy solution is to just slow down the producer. If you're using a managed Kafka service, they may have built-in mechanisms to handle this. If you're running your own Kafka cluster, you can implement back pressure by having the producer check the lag on the partition and slow down if it's too high.

### Fault Tolerance and Durability

Kafka ensures data durability through its replication mechanism. Each partition is replicated across multiple brokers, with one broker acting as the leader and others as followers. When a producer sends a message, it is written to the leader and then replicated to the followers. This ensures that even if a broker fails, the data remains available. Producer acknowledgments (acks setting) play a crucial role here. Setting acks=all ensures that the message is acknowledged only when all replicas have received it, guaranteeing maximum durability.

**But what happens when a consumer goes down?**

When a consumer fails, Kafka's fault tolerance mechanisms help ensure continuity:

- **Offset Management:** Remember that partitions are just append-only logs where each message is assigned a unique offset. Consumers commit their offsets to Kafka after they process a message. This is the consumers way of saying, "I've processed this message." When a consumer restarts, it reads its last committed offset from Kafka and resumes processing from there, ensuring no messages are missed or duplicated.

- **Rebalancing:** When part of a consumer group, if one consumer goes down, Kafka will redistribute the partitions among the remaining consumers so that all partitions are still being processed.

### Handling retries and errors

While Kafka itself handles most of the reliability (as we saw above), our system may fail getting messages into and out of Kafka. We need to handle these scenarios gracefully.

#### Producer retries

First up, we may fail to get a message to Kafka in the first place. Errors can occur due to network issues, broker unavailability, or transient failures. To handle these scenarios gracefully, Kafka producers support automatic retries. Here's a sneak peek of how you can configure them:

```javascript
const producer = kafka.producer({
  retry: {
    retries: 5, // Retry up to 5 times
    initialRetryTime: 100, // Wait 100ms between retries
  },
  idempotent: true,
});
```

#### Consumer retries

On the consumer side, we may fail to process a message for any number of reasons. Kafka does not actually support retries for consumers out of the box (but AWS SQS does!) so we need to implement our own retry logic. One common pattern is to set up a custom topic that we can move failed messages to and then have a separate consumer that processes these messages. This way, we can retry messages as many times as we want without affecting the main consumer. If a given message is retried too many times, we can move it to a dead letter queue (DLQ). DLQs are just a place to store failed messages so that we can investigate them later.

#### Performance optimizations

Especially when using Kafka as an event stream, we need to be mindful of performance so that we can process messages as quickly as possible.

- This first thing we can do is batch messages in the producer before sending them to Kafka. Again, this is just a simple configuration.

```javascript
const producer = kafka.producer({
  // Batch up to 100 messages or wait up to 10ms before sending
  batch: {
    maxMessages: 100,
    maxWaitTime: 10,
  },
});
```

- Another common way to improve throughput is by compressing the messages on the producer. This can be done by setting the compression option in the producer configuration. Kafka supports several compression algorithms, including GZIP, Snappy, and LZ4. Essentially, we're just making the messages smaller so that they can be sent faster.

```javascript
const producer = kafka.producer({
  compression: CompressionTypes.GZIP,
});
```

Arguably the biggest impact you can have to performance comes back to your choice of partition key. The goal is to maximize parallelism by ensuring that messages are evenly distributed across partitions. In your interview, discussing the partition strategy, as we go into above, should just about always be where you start.

#### Retention policies

Kafka topics have a retention policy that determines how long messages are retained in the log. This is configured via the retention.ms and retention.bytes settings. The default retention policy is to keep messages for 7 days.
In your interview, you may be asked to design a system that needs to store messages for a longer period of time. In this case, you can configure the retention policy to keep messages for a longer duration. Just be mindful of the impact on storage costs and performance.

## Handling failures in message queue operations

Message queues (like Kafka or RabbitMQ) decouple producers and consumers, absorb load spikes, and improve reliability.
They introduce two key points where things can fail and must be retried:

- When producing (publishing) messages to the queue
- When consuming and processing messages from the queue

### Producing with retries

When producing messages, failures can occur due to network issues, broker unavailability, or transient errors. To handle these scenarios gracefully, message queue clients typically support automatic retries. Most modern client libraries (like Kafka’s producer, RabbitMQ’s publisher confirms, etc.) offer built-in retry or reconnection logic.

Best practices for producers:

- Enable retry logic with backoff in your producer configuration
- If the client doesn’t support retries, catch exceptions and retry manually
- Add logging and metrics to track failed publish attempts
- Optionally, use a local buffer or fallback store (e.g., write to disk or Redis) to store undelivered messages in critical workflows

### Consuming with retries

On the consumer side, retries are more complex—and riskier.

If processing a message fails (e.g., due to a downstream API being unavailable), blindly retrying can lead to:

- Infinite retry loops (a.k.a. “poison pill” messages)
- Overloading the queue
- Service degradation
- Duplicate processing of messages

Common strategies for handling retries on the consumer side include:

- Immediate Retry: If a message fails, don’t acknowledge it. The broker will requeue and redeliver it shortly.
- Delayed Retry: Requeue the message to a delay queue or re-publish it with a delay. Helps reduce retry storms.
- DLQ (Dead Letter Queue): After max retry attempts, send the message to a separate queue for manual inspection or later processing.

Recommended consumer retry practices:

A robust message processing pipeline typically follows this pattern:

- Track Retry Attempts
Use a retry_count in the message header or metadata.

- Handle Failures Intelligently

  - If retry_count < max_retries: Increase the count, apply delay, requeue or forward to delay queue
  - If retry_count >= max_retries: Route the message to a Dead Letter Queue (DLQ)

- Use Increasing Delays (Exponential Backoff)

To prevent retry storms:

1st failure → Retry after 1 minute
2nd failure → Retry after 5 minutes
3rd failure → Send to DLQ
