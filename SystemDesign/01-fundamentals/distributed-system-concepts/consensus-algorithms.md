# Consensus algorithms

Consensus algorithms are protocols that enable a collection of distributed nodes (or processes) to agree on a single data value or system state, even when some nodes might fail or messages are delayed. They are foundational to ensuring consistency, reliability, and fault tolerance in distributed systems.

## Why Do We Need Consensus Algorithms?

In distributed systems, data is stored across multiple nodes to improve scalability, performance, and fault tolerance.

However, this decentralization brings challenges:

- Data Consistency: How do we ensure that every node has the same data, even if some nodes fail or become isolated due to network issues?

- Fault Tolerance: How can the system continue to operate correctly even when some nodes behave unexpectedly or go offline?

- Coordination: How do distributed processes coordinate their actions without a central authority?

Consensus algorithms provide the answers by enabling nodes to agree on data values or the order of operations, ensuring that the system behaves predictably despite failures.
