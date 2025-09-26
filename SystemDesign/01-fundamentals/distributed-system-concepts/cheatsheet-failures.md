
# Summary of Failure Handling Strategies in Distributed Systems

## Set Timeouts for Remote Calls

- Establish maximum wait times for responses from services
- Abort operations and handle failures after timeout expires
- Apply to all network calls (APIs, databases, message queues, third-party services)

## Retry Intelligently

- Retry: Timeouts, HTTP 5xx errors, network disconnects, rate limits (429)
- Don't Retry: HTTP 4xx errors, validation failures, non-idempotent operations
- Best Practices: Use exponential backoff with jitter, cap retry attempts, only retry idempotent operations

## Implement Fallbacks and Defaults

- Continue with reduced functionality rather than complete failure
- Examples: Return cached/stale data, show default content, degrade gracefully
- Focus on maintaining core functionality when dependencies fail

## Use Circuit Breakers

- Stop sending traffic to consistently failing services
- States: Closed (normal), Open (failing, rejecting requests), Half-open (testing recovery)
- Prevents cascading failures across the system

## Load Shedding & Backpressure

- Load Shedding: Intentionally reject requests when system is under stress
- Backpressure: Signal upstream systems to slow down
- Techniques: HTTP 429 responses, request queuing, rate limiting, traffic prioritization

## Ensure Idempotency

- Operations should be safe to repeat without side effects
- Use idempotency keys for non-idempotent operations
- Store key-response pairs to prevent duplicate processing

## Message Queue Strategies

- Producers: Enable retry logic with backoff, track failed publish attempts
- Consumers: Implement immediate retries, delayed retries, and dead letter queues (DLQs)
- Handle "poison pill" messages that consistently fail processing

## Failover and Replication

- Automatically switch to backup components when primary fails
- Maintain redundant copies of services and data
- Minimize downtime and maintain availability

## Consensus Algorithms

- Ensure nodes agree on shared state even when some fail
- Key algorithms: Paxos and Raft
- Handle split-brain scenarios and maintain consistency

## Monitor, Alert, and Auto-Recover

- Monitor: Reliability, latency, traffic, and saturation metrics
- Alert: Set thresholds for anomalies and degradation
- Auto-recover: Implement self-healing mechanisms like health checks with auto-restart
