# Handling failures in distributed systems

In a distributed system, failures aren’t a possibility—they’re a certainty.

Your database might go down. A service might become unresponsive. A network call might time out. The question is not if these things will happen—but when.

## Types of failures in distributed system

### Network Failures

- Packets get dropped
- Connections time out
- DNS resolution fails
- Latency spikes suddenly
- Firewalls misbehave

### Node Failures

- Power failure
- OS crash
- Disk corruption
- Out-of-memory (OOM)
- Hardware failure

### Service Failures

- Code bugs (null pointers, unhandled exceptions)
- Deadlocks or resource exhaustion
- Memory leaks causing the service to slow down or crash
- Misconfigurations (e.g., bad environment variables)

### Dependency Failures

- Databases
- Caches (like Redis or Memcached)
- External APIs (payment gateways, 3rd-party auth providers)
- Message queues (like Kafka, RabbitMQ)

Example: Your checkout service calls the payment API, which calls a bank API, which calls a fraud-detection microservice. Each hop is a potential point of failure.

### Data Inconsistencies

Data replication across systems (like DB sharding, caching layers, or eventual consistency models) can introduce:

- Out-of-sync states
- Stale reads
- Phantom writes
- Lost updates due to race conditions

Example: A user updates their address, but due to replication lag, the shipping system fetches the old address and sends the package to the wrong place.

### Time-Related Issues (Clock Skew, Timeouts)

Distributed systems often rely on time for:

- Cache expiration
- Token validation
- Event ordering
- Retry logic

But system clocks on different machines can drift out of sync (called clock skew), which can wreak havoc.

## Strategies to deal with failures

### Set Timeouts for Remote Calls

A timeout is the maximum time you’re willing to wait for a response from another service. If a service doesn’t respond in that time window, you abort the operation and handle it as a failure.

Every network call whether it’s to a REST API, database, message queue, or third-party service should have a timeout.

Why?

Waiting too long can hog threads, pile up requests, and cause cascading failures. It’s better to fail fast and try again (smartly).

#### Timeout best practices

To be effective, timeouts should be:

- Short enough to fail fast
- Long enough for the request to realistically complete
- Vary depending on the operation (e.g., reads vs writes, internal vs external calls)

A good practice is to base timeouts on the service’s typical latency (e.g., use the 99th percentile response time or service SLO, plus a safety margin)​
If your downstream service has a p99 latency of 450ms:

```shell
Recommended Timeout = 450ms + 50ms buffer = 500ms
```

### Retry Intelligently, Not Blindly

Some failures are temporary like network hiccups, short-lived server errors or a momentary database overload. Retrying such operations is often the right move. But only if you do it the right way.

A retry is a re-attempt of an operation that failed. The idea is simple: maybe it’ll work the second (or third) time.

But retries, if done carelessly, can cause more harm than good—leading to cascading failures, retry storms, or duplicated side effects.

What to Retry

- Timeouts: Might succeed on a retry
- HTTP 5xx errors: Indicates server issues
- Network disconnects: Could be a brief connectivity glitch
- HTTP 429 (Rate Limited): Retry after suggested delay

What Not to Retry

- HTTP 4xx errors (e.g. 400): Client-side error, request needs to be fixed
- Validation failures: Data is invalid, retry won’t help
- Non-idempotent operations: Retrying could cause duplicates (e.g. "create new user", “process payment“)

Good Retry Practices

- Retry only Idempotent Operations
- Use Exponential Backoff
- Add Jitter
- Cap Retries

### Implement Fallbacks and Defaults

When part of your system fails, continue to serve the user with reduced functionality rather than a full-blown error.

A fallback is what your system does instead of failing when a component breaks.

Instead of failing the entire request:

- Return cached/stale data
- Show default content
- Degrade gracefully

Fallback hierarchy

```text
Primary Data → Cached Data → Hardcoded Default → Error (last resort)
```

Real-World Examples

- If your ML recommendation engine goes down, show popular items instead.
- If the live chat is unavailable, show a “Leave us a message” form.
- If a service for reviews fails, show the product without reviews.
- If a location service fails, show the default location (e.g., user’s last known city)

### Use Circuit Breakers to Avoid Cascading Failures

If a service is really down, keep retrying will only make it worse. If it’s failing repeatedly, you should stop sending traffic to it for a while.

That’s the idea behind a circuit breaker.

A circuit breaker is a fail-fast mechanism that protects your system from being overwhelmed by repeated failures. It cuts off calls to a failing dependency, allowing it time to recover and preventing your own service from going down with it.

### Use Load Shedding & Backpressure

If your service is nearing its limits (CPU, memory, threads), continuing to accept requests can push it over the edge—bringing everything down.

Instead of letting things collapse, you should shed load or apply backpressure to slow things down.

Load shedding is the practice of intentionally rejecting some requests when your system is under stress.

The idea is simple: Better to drop a few requests than crash the whole service.

Backpressure is a mechanism where a downstream system tells the upstream system to slow down because it can't keep up.

How to Handle Overload Gracefully

- HTTP 429 Response: Return 429 Too Many Requests when request rates exceed safe thresholds
- Request Queuing: Temporarily hold requests in a buffer/queue for delayed processing (if latency is acceptable)
- Rate Limiting: Limit requests per user, token, or IP to prevent abuse or spikes
- Traffic Prioritization: Drop or throttle non-essential traffic (e.g., analytics, personalization) while preserving critical functionality
- Backpressure Signals: Use protocols like gRPC or HTTP/2 to notify upstream systems to reduce traffic (e.g., flow control, window sizes)

### Ensure Idempotency for Safe Retries

If you're going to retry requests, they must be safe to repeat. That means the operation should not have unintended side effects.
An idempotent operation is one that can be safely called multiple times with the same result as calling it once.

This means even if the client retries the same request due to a timeout or network glitch, the state of the system remains consistent—no duplicate actions, no unintended side effects.

How to Make POST Requests Idempotent

To safely retry non-idempotent operations (like payments or order creation), require clients to send an Idempotency-Key in the request header:

```shell
POST /create-order
Headers:
  Idempotency-Key: abcd-1234
```

On the server side:

Check if you've seen this key before.

- If yes, return the previous response.
- If no, process the request, and store the response along with the key.

Real-World Example: Stripe

Stripe’s APIs require an Idempotency-Key for operations like charging a card or creating a subscription. This ensures:

- One charge per payment attempt
- One invoice per billing cycle
- One email per notification trigger

They even store the key-response pair for 24 hours, after which the key expires and a new request is treated as fresh.

### Message Queue Operations

Message queues (like Kafka or RabbitMQ) decouple producers and consumers, absorb load spikes, and improve reliability.

They introduce two key points where things can fail and must be retried:

- When producing (publishing) messages to the queue
- When consuming and processing messages from the queue

Producing with retries

When your service tries to publish a message to the queue, it may occasionally fail due to:

- Network issues
- Broker unavailability
- Temporary backpressure (e.g., Kafka partition full)

Most modern client libraries (like Kafka’s producer, RabbitMQ’s publisher confirms, etc.) offer built-in retry or reconnection logic.

Best Practices for Producers:

- Enable retry logic with backoff in your producer configuration
- If the client doesn’t support retries, catch exceptions and retry manually
- Add logging and metrics to track failed publish attempts
- Optionally, use a local buffer or fallback store (e.g., write to disk or Redis) to store undelivered messages in critical workflows

Consuming with Retries
On the consumer side, retries are more complex—and riskier.

If processing a message fails (e.g., due to a downstream API being unavailable), blindly retrying can lead to:

- Infinite retry loops (a.k.a. “poison pill” messages)
- Overloading the queue
- Service degradation

Common retry strategy for consumers

- Immediate Retry: If a message fails, don’t acknowledge it. The broker will requeue and redeliver it shortly.
- Delayed Retry: Requeue the message to a delay queue or re-publish it with a delay. Helps reduce retry storms.
- DLQ (Dead Letter Queue): After max retry attempts, send the message to a separate queue for manual inspection or later processing.

### Failover and Replication

Failover is the system’s ability to automatically switch to a backup component when the primary one fails.
Minimize downtime and maintain availability.
This is achieved through replication—maintaining redundant copies of your services or data. So when one component dies, another can step in without user impact.

### Consensus Algorithms for Agreement

In a distributed system, multiple nodes work together to maintain consistency. But what happens when some nodes fail, go offline, or become slow?

Consensus algorithms ensure that the remaining nodes can still agree on a shared value or system state—even in the face of failure.

Key algorithms

- Paxos (by Leslie Lamport)
- Raft

### Monitor, Alert, and Auto-Recover

In distributed systems, things break—often silently. And if you’re not watching, the user is the first to know.

What Should You Monitor?

Don’t just track if a service is up. Track if it’s healthy and performing well.

Here are key metrics every service should report:

- Reliability: Success Rate, Error Rate, Health Checks
- Latency: p50, p95, p99 Response Times
- Traffic: Requests per Second (RPS), Throughput
- Saturation: CPU, Memory, Thread Pool Usage, Queue Depth

Tools You Should Be Using
Modern systems use one or more of the following tools for logs, metrics, traces, and visualization:

- Metrics: Prometheus, Datadog, CloudWatch, New Relic
- Dashboards: Grafana, Datadog, Kibana
- Logs: ELK Stack (Elasticsearch, Logstash, Kibana), Fluentd, Loki
- Tracing: Jaeger, Zipkin, OpenTelemetry

Alerting: Detect Issues Before Users Do
Set up alerts for anomalies, threshold breaches, or sustained degradation.

Smart Alert Examples::

- Error rate > 5% for 5 minutes
- p95 latency > 1.5s for more than 2 mins
- Queue depth > 500 items (possible backlog)
- Service restarted 3+ times in 10 minutes

Automate Recovery
Manual intervention should be the last resort. Instead, build systems that heal themselves when possible:

- Health Check + Auto-Restart: If a service fails health checks, Kubernetes or your orchestrator should restart it.
- Rolling Deployments + Auto Rollback: Deploy one instance at a time. If errors spike, automatically roll back the release.
