# Top-K Heavy Hitters in Real-Time Stream Processing

In real-time stream processing, identifying the top-K most frequent items (heavy hitters) is a common requirement. This can be particularly useful in scenarios such as tracking the most played songs on a music platform, the most viewed articles on a news site, or the most active users in a social network.

## Windowing Strategy

### Global Windows

Global window is a window that covers the entire period of data. For example, if we set up a global window, all events will be in the same window regardless of time. In the context of this problem, global window means the top K songs of all time.

### Tumbling Windows

Tumbling window is a fixed size window that does not slide. Events in the same window are not overlapping and set by a start and end time. For example, if we set up a tumbling window of 10 minutes, all events in the last 10 minutes will be in the same window. At 10:00:00, the window starts and at 10:10:00, the window ends. And the next window will start at 10:10:00 and end at 10:20:00. In the context of this problem, tumbling window means top K songs at predefined time intervals.

### Sliding Windows

Sliding window is a dynamic window that slides over time. For example, if we set up a sliding window of 10 minutes with a slide interval of 1 minute, all events in the last 10 minutes will be in the same window, but every minute, the window will slide forward by 1 minute. At 10:00:00, the window starts and at 10:10:00, the window ends. At 10:01:00, the window will slide forward to 10:11:00 and so on. In the context of this problem, sliding window means top K songs in the last 10 minutes, updated every minute.

### Which type of window to use?

Obviously, if you encounter this problem in an interview, you should clarify with the interviewer which type of sliding window they are asking for.

In the context of the Top K problem, depending on the scenario, we can choose different types of windows. In the real world, a tumbling window of 24 hours is a good choice. For example, Spotify's Top Songs Playlist is updated every 24 hours. The same is likely true for Amazon's Top products per day, YouTube's Top videos etc. Consumers are unlikely care about the top songs or videos of down to the minute or even hour.

However, if the interviewer insists on a more complex scenario, such as the top K songs in the last X minutes using a sliding window, we still need to be able to handle it.

## How Top K Would Be Implemented in Production

### Stream processor implementation

In production, we could use a stream processor like Apache Flink, Spark Streaming, Kafka Streams, Google Cloud Dataflow, AWS Kinesis, Azure Stream Analytics, or whatever favorite stream processor to implement the top K aggregator. It's a very popular technology and there are many providers out there.

The typical data flow in a stream processor is to read data from a stream (Kafka, Pulsar, Kinesis, etc.), apply transformations and aggregations, and write the result to a stream (Kafka, Pulsar, Kinesis, etc.).

We would write MapReduce style code to:

- Apply transformations (filter, map, aggregate, join, etc.).
- Group or partition the data based on keys (e.g., by user_id or item_id).
- Use windowing logic (tumbling, sliding, or custom windows).

For example, in Flink, we can use .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1))) to set up a sliding window of 10 minutes with a slide interval of 1 minute and write a custom ProcessWindowFunction to compute the top K items within the window.

### Redis sorted set implementation

If the question asks for the top K songs in a Global window, we have an even simpler implementation using Redis's sorted set (ZSET). A sorted set is a data structure that stores elements with a score. Elements are automatically ordered by their score in ascending order. Internally, it's implemented as a hash map and a skip list. The time complexity of the basic operations (add ZADD, remove ZREM) is O(log n). To find the top K elements, we can use ZREVRANGE which has a time complexity of O(log n + K).

We can use the song ID as the element and the play count as the score. Every time a user plays a song, we increment the score of the song in the sorted set using ZINCRBY. To get the top K songs, we can use ZREVRANGE with a range of 0 to K-1.