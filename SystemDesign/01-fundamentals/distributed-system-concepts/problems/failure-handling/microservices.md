# Microservices Communication

## Question

In a microservices architecture where Service A calls B, which calls C:

- How would you implement timeouts and retries across this chain?
- What circuit breaker pattern would you apply?
- How would you prevent cascading failures?

## Answer

We are designing a microservices architecture where Service A calls B, which calls C.

### How would you implement timeouts and retries across this chain

- We will be applying timeouts on each service call, A->B, B->C.
- For timeouts, we will choose a value depending on system experience and microservice response time. Choosing a high value will be straining network resources when the upstream service is really down. Choosing a low value will lead to false positives where we will be failing fast and waiting for some more time would have lead to successful request being processed. So a moderate value would suffice here.
- For retries we will be following exponential backoff and not retry aggressively. We will also add randomness with jitter to even out retries. Further we will also cap the no of retries to not keep retrying indefinitely.

### What circuit breaker pattern would you apply?

- We will apply circuit breaker pattern to avoid cascading failures. 
- For example if service C is down, then requests from B to C will fail despite all retries. So we will be applying circuit breaker pattern here and fail fast. We will fail the requests from A to B itself to avoid the requests reaching C and give it time to heal and recover.
- The pattern will transition between states like closed (When everything is working fine), open(Stop requests as system is failing), half-open(Testing, system in recovering stage)

### How would you prevent cascading failures?

We will prevent cascading failures by using circuit breaker pattern as mentioned above.

## L5-Level Answer

To ensure reliability and resilience in a microservices chain (A→B→C), I would implement the following strategies:

### 1. Timeouts and Retries

- **Timeout Propagation**: Each request from A to B to C carries a context with a deadline, ensuring downstream services do not waste resources on requests that have already timed out upstream.
- **Configurable Timeouts**: Set timeouts at each service boundary based on historical latency and SLOs, balancing between failing fast and allowing for transient delays.
- **Safe Retries**: Retries are only applied to idempotent operations, using exponential backoff with jitter and a capped number of attempts to avoid retry storms.

### 2. Circuit Breaker Pattern

- **Per-Service Circuit Breakers**: Each service boundary (A→B, B→C) implements a circuit breaker that tracks error rates and latency. If failures exceed a threshold, the breaker transitions to 'open', immediately failing requests and preventing further load on the downstream service.
- **State Transitions**: Circuit breakers move between 'closed' (normal), 'open' (fail fast), and 'half-open' (test recovery) states, with health checks to determine when to resume traffic.

### 3. Preventing Cascading Failures

- **Bulkheading**: Isolate resources (threads, connection pools) for each service to prevent failures in one service from exhausting resources in others.
- **Fallbacks and Graceful Degradation**: When a downstream service is unavailable, upstream services provide fallback responses (e.g., cached data, default values) or degrade non-critical functionality.
- **Monitoring and Alerting**: Continuously monitor error rates, latency, and circuit breaker states. Trigger alerts and auto-scaling when thresholds are breached.
- **Request Prioritization**: Critical requests are prioritized over non-essential ones during partial outages.

By combining timeout propagation, safe retries, circuit breakers, bulkheading, and monitoring, the system remains resilient, prevents cascading failures, and provides a consistent user experience even during partial outages.