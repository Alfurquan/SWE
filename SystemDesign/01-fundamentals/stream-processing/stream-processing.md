# Stream Processing

Stream processing is a paradigm shift that focuses on processing data in real-time as it is generated, rather than waiting for it to accumulate in large batches. This approach allows for instant analysis, decision-making, and response to events as they occur, making it particularly well-suited for applications where real-time insights are critical.

Examples of such applications include:

- fraud detection
- real-time log analytics
- IoT (Internet of Things)
- online game event streaming
- machine states in industrial automation
- video processing

## Key Concepts

### What is a Stream?

A stream refers to data that is incrementally made available over time. This dynamic nature of data streams differentiates them from static data sources, such as batch data, which are processed at discrete intervals. In the context of stream processing, the data is organized into an event stream, which represents an unbounded, incrementally processed counterpart to batch data. Each event in the stream carries information about a specific occurrence, which can be anything from a user's interaction with a website to sensor readings in an IoT system.

### How are streams presented and transported?

To transport streams, various messaging systems and data streaming platforms are employed. Apache Kafka, Amazon Kinesis, and Google Cloud Pub/Sub are some of the popular platforms that facilitate stream transportation. These systems provide a distributed, fault-tolerant, and scalable infrastructure for transporting data streams efficiently across various components of a stream processing pipeline.

### Windowing

As streams are unbounded, it is often necessary to divide them into smaller, manageable chunks for processing. Windowing is a technique that segments an event stream into finite windows based on time, count, or session. Time-based windows can be further categorized into tumbling windows, sliding windows, and hopping windows. Windowing enables processing tasks like aggregation or pattern matching to be performed on these smaller, well-defined subsets of the stream.

#### Tumbling Windows

Tumbling windows divide the event stream into non-overlapping, fixed-size time intervals. When a window is closed, the next one starts immediately without any overlap. Tumbling windows are often used when you need to compute an aggregate value for each window independently, without considering the events from other windows. Example: Assume you want to count the number of requests per minute for a web service. You can create tumbling windows of size 1 minute, and at the end of each minute, compute the request count within that window.

#### Sliding Windows

Sliding windows also divide the event stream into fixed-size time intervals but with a specified overlap between consecutive windows. Sliding windows are useful when you need to compute an aggregate value for each window while considering the events from the surrounding windows. Example: Suppose you want to calculate a moving average of stock prices for the last 5 minutes, updated every minute. You can create sliding windows of size 5 minutes with a 1-minute slide. This means that every minute, a new window will be created, and the average stock price will be calculated for that 5-minute window.

#### Session Windows

Session windows are based on the activity pattern of the events rather than a fixed time interval. They are used to capture bursts of activity separated by periods of inactivity. Session windows are particularly useful when analyzing user behavior, as they can group events related to a single user session. Example: Imagine an e-commerce website where you want to analyze user interactions within a single shopping session. You can create session windows by grouping events from the same user that are close in time (e.g., within 30 minutes of each other) and separated by a period of inactivity (e.g., no events for at least 30 minutes).

#### Global Windows

 Global windows treat the entire stream as a single window. They are typically used in conjunction with triggers to determine when to emit the results of the computation. Global windows are useful when you need to process the entire dataset as a whole or when you want to compute a value based on all events in the stream. Example: Suppose you want to find the longest common prefix among all the incoming events in a stream. You can create a global window that accumulates all the events and apply a trigger to emit the result when a certain condition is met, such as the arrival of a special end-of-stream event.

### Watermarking

Watermarking is a common method used to address the inconsistency between the time of event occurrence and processing, managing out-of-order events, delayed data, and determining if the data within a specific time period is complete.

In real-time data stream processing, data is usually processed according to the time the event occurred, known as event time. However, due to network delays, system failures, or the concurrent nature of data processing, data may not arrive at the processing system in the order of event time. This leads to a problem: how can the processing system know when it is safe to close a time window and perform aggregation calculations without missing any subsequently arriving delayed data?

Watermarking technology offers a solution by allowing the system to estimate the event time within the data stream, defining a point in time at which it is assumed that all data prior to this point has arrived and window aggregation calculations can be performed. If data with an event time later than this watermark arrives, the system may choose to ignore these delayed data, as they fall outside the processing window defined by the watermark.

### Stream joins

Stream joins are operations that combine two or more event streams based on specified conditions, similar to relational database joins. These conditions can be based on time or key attributes of the events. For example, a time-based join might merge two streams based on the timestamps of their events, while a key-based join might combine streams based on a common identifier, such as a user ID or device ID. An example is how Google Ads joins impression and click streams using adID to calculate click-through rate (CTR).
