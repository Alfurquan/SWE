# Message Queues

A message queue is a communication mechanism that enables different parts of a system to send and receive messages asynchronously.

It acts as an intermediary that temporarily holds messages sent from producers (or publishers) and delivers them to consumers (or subscribers).

## Core components of a message queue

- Producer/Publisher

The entity that sends messages to the queue. Producers push messages into the queue without worrying about the consumer's state.

- Consumer/Subscriber

The entity that reads messages from the queue. Consumers pull messages from the queue and process them.

- Queue

The data structure that stores messages until they are consumed.

- Broker/Queue Manager

The software or service that manages the message queue, handles the delivery of messages, and ensures that messages are routed correctly between producers and consumers.

- Message

The unit of data sent through the queue. A message typically contains the payload (the actual data being sent) and metadata (such as headers, timestamps, and priority).

## How Do Message Queues Work?

The basic workflow of a message queue can be broken down into the following steps:

- Message Creation: A producer generates a message containing the necessary data and metadata.
- Message Enqueue: The producer sends the message to the queue, where it is stored until a consumer retrieves it.
- Message Storage: The queue stores the message in a persistent or transient manner based on its configuration.
- Message Dequeue: A consumer retrieves the message from the queue for processing. Depending on the queue's configuration, messages can be consumed in order, based on priority, or even in parallel.
- Acknowledgment: Once the consumer processes the message, it may send an acknowledgment back to the broker, confirming that the message has been successfully handled.
- Message Deletion: After acknowledgment, the broker removes the message from the queue to prevent it from being processed again.

