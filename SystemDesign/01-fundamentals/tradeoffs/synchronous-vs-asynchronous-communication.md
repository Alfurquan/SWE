# Synchronous vs Asynchronous Communications

Imagine you're at a coffee shop and order a coffee. You wait in line, place your order, and wait for the barista to prepare your coffee. Once it's ready, they hand it to you, and you pay.

This is a synchronous interaction - you wait for the coffee before proceeding.

Now, imagine ordering coffee online for delivery. You place your order, pay, and continue with your day. Later, the coffee is delivered to your doorstep.

This is an asynchronous interaction - you didn't wait for the coffee to be prepared and delivered before moving on with your day.

## Synchronous communications

In synchronous communication, the sender waits for the receiver to acknowledge or respond to the message before proceeding.

It’s like a phone call: you speak, the other person listens and responds, and the conversation progresses sequentially.

When a client (such as a user’s web browser or a service in a microservices architecture) makes a synchronous request, it waits until the response is received.

The workflow remains blocked during this waiting period, unable to perform other tasks.

## Asynchronous communications

Asynchronous communication is a communication pattern where the sender does not wait for the receiver to process the message and can continue with other tasks. The receiver processes the message when it becomes available.

## Factors to consider

When deciding between synchronous and asynchronous communication, consider the following factors:

- Performance: Asynchronous communication can lead to better performance and throughput as the sender and receiver can work independently.
- Scalability: Asynchronous communication allows for better scalability as the system can handle a higher load by processing messages concurrently.
- Reliability: Asynchronous communication can provide better reliability through message persistence and retries in case of failures.
- Complexity: Asynchronous communication introduces additional complexity in terms of message ordering, error handling, and coordination between components.
- Real-time requirements: If the system requires real-time interactions or immediate responses, synchronous communication may be more suitable.
