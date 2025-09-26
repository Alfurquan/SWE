# Heartbeats

In a distributed system, things fail.

Hardware malfunctions, software crashes, or network connections drop.

Whether you're watching your favorite show online, making an online purchase, or checking your bank balance, you're relying on a complex network of interconnected services.

But, how do we know if a particular service is alive and working as expected?
This is where heartbeats come into play.

## What exactly is a Heartbeat?

In distributed systems, a heartbeat is a periodic message sent from one component to another to monitor each other's health and status.

## Why Do We Need Heartbeats?

Without a heartbeat mechanism, it's hard to quickly detect failures in a distributed system, leading to:

- Delayed fault detection and recovery
- Increased downtime and errors
- Decreased overall system reliability

Heartbeats can help with:

- Monitoring: Heartbeat messages help in monitoring the health and status of different parts of a distributed system.

- Detecting Failures: Heartbeats enable a system to identify when a component becomes unresponsive. If a node misses several expected heartbeats, it's a sign that something might be wrong.

- Triggering Recovery Actions: Heartbeats allow the system to take corrective actions. This could mean moving tasks to a healthy node, restarting a failed component, or letting a system administrator know that they need to step in.

- Load Balancing: By monitoring the heartbeats of different nodes, a load balancer can distribute tasks more effectively across the network based on the responsiveness and health of each node.

## How Do Heartbeats Work?

The heartbeat mechanism involves two primary components:

- Heartbeat sender (Node): This is the node that sends periodic heartbeat signals.
- Heartbeat receiver (Monitor): This component receives and monitors the heartbeat signals.

Process

- The node sends a heartbeat signal to the monitor at regular intervals (e.g., every 30 seconds).
- The monitor receives the heartbeat signal and updates the node's status as "alive" or "available".
- If the monitor doesn't receive a heartbeat signal within the expected timeframe, it marks the node as "unavailable" or "failed".
- The system can then take appropriate actions, such as redirecting traffic, initiating failover procedures, or alerting administrators.

While conceptually simple, heartbeat implementation has a few nuances:

- Frequency: How often should heartbeats be sent? There needs to be a balance. If they're sent too often, they'll use up too much network resources. If they're sent too infrequently, it might take longer to detect problems.

- Timeout: How long should a node wait before it considers another node 'dead'? This depends on expected network latency and application needs. If it's too quick, it might mistake a live node for a dead one, and if it's too slow, it might take longer to recover from problems.

- Payload: Heartbeats usually just contain a little bit of information like a timestamp or sequence number. But, they can also carry additional data like how much load a node is currently handling, health metrics, or version information.
