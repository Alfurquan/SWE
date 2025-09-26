# CAP Theorem

CAP stands for Consistency, Availability, and Partition Tolerance, and the theorem states that:

```text
It is impossible for a distributed data store to simultaneously provide all three guarantees.
```

- Consistency (C): Every read receives the most recent write or an error.
- Availability (A): Every request (read or write) receives a non-error response, without guarantee that it contains the most recent write.
- Partition Tolerance (P): The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.