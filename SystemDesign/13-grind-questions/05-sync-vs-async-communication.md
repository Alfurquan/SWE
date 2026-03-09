# Question 5: How do I choose between synchronous and asynchronous communication?

## Answer

In order for us to choose between synchronous and asynchronous communication, we need to consider different factore

- User: First by default we will need to consider user experience as a factor. If the user needs the data to proceed, like lets say login to a app, we need to choose synchronous commnunication. If the user just needs acknowledgement, like lets say your image is being formatted in an image formatting app, we can choose asynchronous communication.

- Availability: Synchronous calls reduce availability, lets say service A calls service B. If service B fails, service A also fails. But asynchronous calls improves availability. Here service A puts a message in a queue for service B to consume and returns back. If service B is down, the message will stay on the queue.

- Latency: Synchronous calls are better suited for low latency apps like video calling apps, gaming apps etc. Asynchronous calls are not so suited for low latency applications.

- Resilience and Throughput: Synchronous calls are not so resilient and have low throughput. Asynchronous calls are more resilient and have higher throughput. Once again, if service A calls service B synchronously and service B is down, service A also fails. But if service A calls service B asynchronously, if service B is down, the message will stay on the queue and service A will not fail. Also, in synchronous communication, service A has to wait for service B to respond before it can process the next request. But in asynchronous communication, service A can process the next request without waiting for service B to respond, giving it higher throughput.

- Complexity: Synchronous communication is simpler to implement and debug. Asynchronous communication is more complex to implement and debug. In asynchronous communication, we need to handle message queues, message formats, message ordering, message retries etc.

In conclusion, we need to consider user experience, availability, latency, resilience and throughput, and complexity when choosing between synchronous and asynchronous communication.