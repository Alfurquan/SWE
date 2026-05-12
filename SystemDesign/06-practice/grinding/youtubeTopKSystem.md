# Problem

Design a system that tracks and displays the Top K most viewed videos on YouTube.

## Answer

## Functional Requirements

- System should display top k most viewed videos on YouTube. For simplicity I am assuming k to be a fixed number like 100. 
- System should display top 100 most viewed videos for last hour. Again for simplicity and scope of this problem I am not adding more time windows.

## Non functional requirements

- Scale: System should be able to handle 10 million video views per second. This is a very high write throughput and system should be designed to handle this scale. Peak views can be 100 million per second during major events like World Cup or Olympics.
- Latency: Top 100 video updates should be near real time. So the latency should be less than 30-60 seconds.
- Accuracy: System should be able to provide accurate top 100 videos based on the number of views. However, approximate results are fine in exchange of sub second speed.
- Read to write ratio: System should be optimized for write heavy workload as there will be a very high number of video views (writes) compared to the number of times top 100 videos are read.

These are some of the requirements I could think of for the system. In a real interview, I would ask the interviewer if they have any specific requirements or constraints in mind that I should consider while designing the system.

## Data models

Next up we will list down the data models that we will be using in our system.

### Video

- video_id: string (unique identifier for the video)
- title: string
- channel_id: string (identifier for the channel that uploaded the video)
- upload_time: timestamp
- media_url: string (URL to access the video)
- thumbnail_url: string (URL for the video thumbnail)

### ViewEvent

- video_id: string (identifier for the video that was viewed)
- timestamp: timestamp (time when the view event occurred)
- user_id: string (identifier for the user who viewed the video, optional)

### TopKVideo

- video_id: string (identifier for the video)
- view_count: integer (number of views for the video in the last hour)

## API Design

Next up we will design the APIs for our system.

### Video View API

**Endpoint:** POST /api/view
**Description:** This API will be called whenever a video is viewed. It will record the view event in the system.

**Request Body:**
```json
{
  "video_id": "string",
  "timestamp": "timestamp",
  "event_id": "string" (Unique identifier for the view event for idempotency)
}
```

The user id would be extracted from the authentication token, so we don't need to pass it in the request body.

### Get Top K Videos API

**Endpoint:** GET /api/topk?k=100&time_window=1h
**Description:** This API will return the top K most viewed videos in the last hour.

**Query Parameters:**

- k: integer (number of top videos to return, default is 100)
- time_window: string (time window for which to calculate top videos, e.g., "1h" for last hour, default is "1h")

**Response Body:**
```json
{
    [
        {
            "video_id": "string",
            "view_count": "integer"
        },
    ...
  ]
}
```

We have kept the APIs to accept k and time_window as query parameters to make it flexible for future extensions. For example, we can later add support for different time windows like last 24 hours, last week, etc. without changing the API contract.

## High level design

Next up we will go through the high level design for the system. We will go layer by layer and discuss how data will be flowing across them.

### Video view event flow

When a user views a video, a view event is generated. This view event contains the video_id, timestamp, user_id and a unique event_id for idempotency.

### Event generation layer

Event generation starts when the user actually clicks on the play button to play a video. Here is how the flow works out

- The client sends a POST request to the `/api/view` endpoint with the video id and a unique event id. This event id would be used for idempotency downstream.
- The request is received by the API gateway, that checks auth, rate limiting etc. It extracts the user_id from the `JWT` passed in the headers and adds it to the request payload.
- The API gateway also generates an `event_time` which is basically derived from the timestamp sent in the request. Since we cannot rely on client_time, we need this check here. If the clients passed time is too much different from the server time, we take event_time to be the server timestamp, else we take event_time to the client_timestamp.

Once the request is received by the API gateway, we go on to the next layer

### Ingestion layer

We have around 10M video views/sec which we need to ingest. So we need to design the ingestion layer to handle this load. 
We will use `kafka` as the tool to ingest this view data. We have chosen kafka as its an append only commit log and allows faster writes. Kafka also provides at-least once guarantees via its offset tracking. Moreover we can partition the kafka to scale and have the view events being processed in parallel by consumer group of workers.

Paritioning strategy:

We can partition the kafka topic based on video_id. The issue with this approach is that we might end up with some hot partitions for very popular videos. To solve this, we can add a random suffix to the video_id while partitioning. For example, we can use `video_id + random_suffix` as the key for partitioning. This way we can distribute the load more evenly across partitions while still ensuring that all events for a video go to the same partition. The tradeoff here is that we would need to aggregate the counts for a video across multiple partitions, but we can handle this in the processing layer.

No of partitions:

We have to ingest 10M events/sec and we want to keep the load on each partition manageable. Assuming each partition can handle around 100K events/sec, we would need around 100 partitions to handle the load. This is a rough estimate and we can adjust the number of partitions based on the actual load and performance of the system. To handle peak load and since adding partitions is not an instant operation, we can start with 150-200 partitions to have some buffer for growth and peak load.

This is how the flow would look like in the ingestion layer:

- The API gateway receives the view event and sends it to the kafka topic with the appropriate partition key (video_id + random_suffix).
- The kafka topic is partitioned based on the partition key and the events are distributed across partitions.
- Once the events are in the kafka topic, they are ready to be consumed by the processing layer.

### Processing layer

Since we have 10M views/sec, such high volume of write cannot be processed at a single server. What we will do here is to have regional aggregation of the view counts and then have a global aggregation layer that aggregates the counts from different regions to calculate the top K videos globally.

#### Pre-aggregation layer

- The regional nodes receive the view events from the kafka topic and maintain a count of views for the videos in that region. Every time a view event is processed, the count for the corresponding video is updated.
- The regional nodes can use in memory data structures like hashmap or redis to maintain the counts for the videos. This allows for fast updates and retrievals. Also for redis, we can optionally add persistence to disk to prevent data loss in case of failures.
- We use time windowing to maintain the counts for the last hour. For example, we can use a sliding window of 1 hour with a slide interval of 1 minute. This way we can maintain the counts for the last hour and update them every minute. This allows us to efficiently calculate the top K videos for the last hour without having to store all the view events for the last hour.
- Every 30 seconds or 1 minute, the regional nodes send the aggregated counts for the videos to the global aggregation layer.
- This way we are reducing the load on the global aggregation layer by doing some pre-aggregation at the regional level. If we have 100 regional nodes, then the central aggregation layer is receiving 100 messages every minute instead of 10M view events every second. This makes the system more scalable and efficient.


#### Global aggregation layer

- The global aggregation layer receives the aggregated counts from the regional nodes and maintains a global count for each video. 
- The global aggregation layer uses a streaming processing framework like `Apache Flink` or `Apache Spark Streaming` to process the incoming counts and maintain a global count for each video.
- It uses approximately counting algorithms like `Count-Min Sketch` to maintain the counts for the videos in a memory efficient way. This allows us to handle the large number of videos and their counts without running out of memory.
- Every time the global counts are updated, the global aggregation layer calculates the top K videos based on the counts and updates the storage layer with the new top K videos.

### Storage layer

For ths storage layer we can have different options depending on query patterns, latency requirements etc. For this use case, we can use a key-value store like `Redis` or a NoSQL database like `Cassandra` to store the top K videos.

Redis has an in memory data structure called `Sorted Set` which can be used to maintain the top K videos based on their view counts. The view count can be used as the score for the sorted set and the video_id can be used as the member. This allows us to easily retrieve the top K videos in O(log N) time.

For persistence and durability, we can persist the events to a database like `PostgreSQL` or `Cassandra`. This way we can have a backup of the data in case of failures and also allows us to do historical analysis if needed.

### Fetch top 100 video views 

- Client calls the GET API call to retrieve the top 100 videos
- The API gateway receives the request, verifies auth, rate limiting etc and forwards request to the server
- The server fetches the result from redis and returns the response from the cache.

## Failure scenarios 

"If one of your regional aggregation nodes crashes exactly 55 seconds into its 1-minute aggregation cycle (right before it sends its batch to the global Flink job), how does your system ensure that those 55 seconds of view counts aren't permanently lost, while simultaneously guaranteeing we don't double-count those views when the node spins back up"

It would be solved using a combination of checkpointing and offsets in Kafka.

- The regional aggregation nodes would be consuming the view events from the Kafka topic and maintaining their counts in memory.
- The regional nodes would periodically checkpoint their state (the counts for the videos) as well as kafka offsets to a durable storage like HDFS or S3. This way if a node crashes, it can recover its state from the last checkpoint and continue processing from there.
- Additionally, the regional nodes would be tracking their offsets in the Kafka topic. When a node crashes and restarts, it can use the offsets to determine which events it has already processed and which events it needs to reprocess. This ensures that we don't double count the views when the node spins back up.


