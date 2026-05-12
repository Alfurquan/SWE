# 🎙️ The Scenario: "The High-Volume Notification Service"
Interviewer: "We need to design a notification system for a global social media platform. When a celebrity with 50 million followers posts a photo, we need to send a push notification to all their followers.

However, we have a constraint: some users want notifications instantly, while others have 'Quiet Hours' enabled. Also, our third-party Push Provider (Apple/Google) can only handle 100,000 requests per second before they start rate-limiting us.

The Question: How would you design the pipeline to handle this 'Fan-out' without crashing our internal services or getting blocked by the external Push Provider? Give me the high-level components and tell me: One massive job to handle everything, or a decoupled multi-stage pipeline?"

💡 Your Task
State your choice: (One job vs. Decoupled).

Justify it: Give me at least two pros and one con.

Scale Math: If we have 50M users to notify, and the provider limit is 100k/sec, how long will it take to clear the queue? How would you handle that in the design?

---

# Solution

We are designing a notification system where when a celebrity posts a photo, we need to send push notifications to all the followers.

First of all for designing the solution we should avoid using a single job due to these cons

- Difficult to scale as one job has limited processing capacity.
- A single job becomes a Single point of failure, where if the job crashes, everything comes to a halt and system crashes as well.

So in order to architect the system in a more robust and scalable way here is how I would design it

- First of all I would make this system asynchronous and separate out post creation logic from notification sending logic.
- The bridge here would be a message queue like kafka.
- The system would put a message in the queue to send the notification.
- The message would contain the post_id and the user_id.
- Multiple workers would consume from this queue, process the message, query the followers from the db to send the notification by calling the third-party Push Provider.

This will make the system more robust and scalable due to these reasons

- Each worker commits the offset in the message queue, so when the worker crashes, a new one can start processing the messages from the last committed offset.
- We can scale the notification sending by partitioning the message queue and have consumer group of workers consume from these partition. The partition key here would be user_id or we can use round robin to spread the tasks across the workers. For calculating the number of partitions, we will need to see how many messages we are putting in the queue per second and how many messages each worker can process per second. For example, if we are putting 100,000 messages in the queue per second and each worker can process 1,000 messages per second, we will need at least 100 partitions to handle the load.
- By applying a queue and not synchronously calling the third-party Push Provider, we can buffer and control the rate of API calls/sec to the third-party Push Provider which can handle 100,000 requests per second before they start rate-limiting us.
- For users with quiet hours, the workers can put the notifications in a delay store and the delayed notifications can be processed by a separate set of workers after the quiet hours are over.


Only con I see here is that there will be some delay in sending the notifications due to the asynchronous nature of the system, but this is a trade-off we have to make for scalability and robustness. ALso the complexity of the system increases due to the introduction of message queues and multiple workers, but this is necessary to handle the scale of notifications we need to send.

If we have 50M users to notify, and the provider limit is 100k/sec, how long will it take to clear the queue? How would you handle that in the design?

If we have 50 million users to notify and we have partitioned the message queue into 100 partitions, we can have 100 workers consuming from these partitions. Each worker can process 1,000 messages per second, so in total we can process 100,000 messages per second (100 workers * 1,000 messages/worker/second). Since the provider limit is also 100,000 requests per second, we can process the messages at the rate of 100,000 messages per second without hitting the rate limit. So it would take 50 million / 100,000 = 500 seconds to clear the queue.

To handle this in the design, we can implement a rate limiter in our workers to ensure that we do not exceed the provider limit of 100,000 requests per second. This can be done by keeping track of the number of requests sent in the current second and delaying the processing of messages if we are approaching the limit. Additionally, we can also implement a retry mechanism for messages that fail to send due to rate limiting, so that they can be retried after a certain delay. This way, we can ensure that all notifications are eventually sent without overwhelming the third-party Push Provider.
