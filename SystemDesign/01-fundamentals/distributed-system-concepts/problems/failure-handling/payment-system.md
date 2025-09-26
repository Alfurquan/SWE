# Payment System

## Question

Your payment service occasionally experiences timeouts when calling a third-party payment gateway. How would you implement a reliable solution that:

- Doesn't charge customers twice
- Ensures successful payments are recorded
- Handles temporary outages without degrading user experience

## Answer

Here we want to design a reliable payment service that handles failures gracefully.

### Doesn't charge customers twice

In order to not charge customer twice, we can follow this strategy

- Add idempotency keys in payment request made by the client

- When the client makes a request to payment service, we check if we have seen this idempotency key before, if yes we drop the request, else we store the idempotency key for later and process the payment request by forwarding it to the third-party payment gateway.

- We store the idempotency key for sometime lets say 24hrs and then delete it.

- For handling timeouts with payment gateway, our payment service can retry with exponential backoff and a bit of randomness with jitter so as to not overwhelm the payment gateway. We can also cap the no of retries to an appropriate number like between 5 to 10.

- If payment does not go through even after the retries is exhausted, we record the payment as failure and send an appropriate error message to the client.

### Ensures successful payments are recorded

In order to make sure successful payments are recorded, we can use a relational database like postgres with follows ACID principles, and makes sure data is persisted in reliable way.

Here, in terms of CAP theorem, we will favour consistency over availability when failures happen.

Postgres SQL follows ACID principles, uses Write ahead logging to make sure data is persisted, even if the database crashes before recording it.

If the database itself is down for sometime, we can store the requests in a message queue and then once database is up, we can write the pending requests to the database.

### Handles temporary outages without degrading user experience

In order to handle temporary outages without degrading user experience, we can design a system in reliable way with fallbacks in case failures happen.

Below is the strategy we can follow to design a reliable system

- Add idempotency keys to request from client, to make sure customers are not double charged in case some failures happen.
- Add retries with exponential backoff and randomness with jitter on each request to every layers, services, message queues, dbs etc.
- We monitor the reliability of system by recoding metrics like failure rates, latency etc.
- For database, we can replicate it and if one of the replicas is down, gradually failover to a healthy one.
- Use circuit breakers to fail fast if the system is failing and let it heal.
