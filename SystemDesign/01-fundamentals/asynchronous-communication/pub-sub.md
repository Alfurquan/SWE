# Pub/Sub

Publish-Subscribe (Pub/Sub) is an architectural pattern used to enable asynchronous communication between components in a distributed system.

In a Pub/Sub system, components can publish messages to a topic without needing to know who will receive them. Similarly, components can subscribe to topics to receive messages without needing to know the details of the publishers.

## Components of Pub/Sub

### Publishers

Publishers are components or services that send messages (or events) to a topic. They generate data or events and "publish" these messages without worrying about who will consume them.

Example: In an e-commerce system, a service that handles order processing might publish an "Order Placed" event whenever a new order is received.

### Subscribers

Subscribers are components or services that express interest in certain topics. They receive and process messages that are published to those topics.

Example:A notification service might subscribe to the "Order Placed" topic to send confirmation emails to customers.

### Message broker

The Message Broker (or message queue) is the core component that manages topics, receives messages from publishers, and distributes them to all the subscribers of those topics. It acts as the intermediary to ensure that messages flow efficiently between publishers and subscribers.

## How Pub/Sub works ?

- Publishers Send Messages: A publisher creates a message and sends it to a specific topic on the message broker.
- Message Broker Receives and Stores Messages: The broker receives the message and temporarily stores it in the topic. Depending on the implementation, messages may be persisted to disk for durability.
- Subscribers Receive Messages: Subscribers that have subscribed to the topic receive the message. This can happen in real time, or the subscriber may poll the broker if real-time delivery is not required.
- Processing and Acknowledgment: Subscribers process the message. In some systems, the subscriber sends an acknowledgment back to the broker to confirm that the message has been processed successfully.
