# Idempotency

Imagine you're making a purchase from an online store.

You hit "pay" but the screen freezes, and you're unsure if the payment went through.

So, you refresh the page and try again.

Behind the scenes, how does the system ensure you aren’t accidentally charged twice?

## What is Idempotency ?

In mathematics, an operation is idempotent if applying it multiple times produces the same result as applying it once.
Idempotency is a property of certain operations whereby executing the same operation multiple times produces the same result as executing it once.

## Why Idempotency matters ?

Distributed systems often require fault tolerance to ensure high availability. When a network issue causes a timeout or an error, the client might retry the request.
If the system handles retries without idempotency, every retry could change the system’s state unpredictably.

By designing operations to be idempotent, engineers create a buffer against unexpected behaviors caused by retries.

This “safety net” prevents repeated attempts from distorting the outcome, ensuring stability and reliability.

## Strategies to Implement Idempotency

### Unique request identifiers

One of the simplest techniques to achieve idempotency is by attaching a unique identifier, often called an idempotency key to each request.
When a client makes a request, it generates a unique ID that the server uses to track the request. If the server receives a request with the same ID later, it knows it’s a duplicate and discards it.
Example: A payment service could require every transaction request to include a unique ID. If the client retries with the same ID, the server will skip the charge, preventing duplicate transactions.

### Database Design Adjustments (Upsert Operation)

Some database operations, such as inserting the same record multiple times, can lead to unintended duplicate entries.

Achieving idempotency in these cases often requires redesigning the database operations to be inherently idempotent.

This can involve using upsert operations (which updates a record if it exists or inserts it otherwise) or applying unique constraints that prevent duplicates from being added in the first place.

In this example, we use SQL INSERT ... ON CONFLICT to achieve an upsert operation, ensuring that duplicate entries don’t affect the database state.

### Idempotency in Messaging Systems

In a messaging system, we can enforce idempotency by storing a log of processed message IDs and checking against it for every incoming message.
