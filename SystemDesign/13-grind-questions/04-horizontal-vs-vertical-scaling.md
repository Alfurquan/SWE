# Question 4: What are the real trade-offs between vertical and horizontal scaling?

As our application grows in user base, we need to scale our application to keep serving the users in a quick and reliable manner.

There are two ways we can scale up our application

- Horizontal Scaling: By adding more servers we can reduce load on a single server and hence scale our app to serve growing user traffic
- Vertical Scaling: By making the single server more powerful, by increasing the compute and storage power of our server, we can scale it up to serve growing user traffic

Both these scaling methods come with tradeoffs

## Horizontal scaling

### Pros

- No single point of failure
- Load is distributed across multiple servers
- A server can only by scaled up to a certain limit, after which we need to scale it out.
- Provides redundancy which helps in fault tolerance and availability

### Cons

- Horizontal scaling introduces Network Latency and Partial Failures. In a distributed system, the network will fail. Handling that (retries, timeouts, circuit breakers) is the real "complexity," not just making the call.
- We can only scale out our servers if we keep them stateless
- Achieving strong consistency is difficult
- Operational overhead, managing 100 servers is difficult than manahging one server

## Vertical scaling

### Pros

- Simple to implement and keeps the architecture simpler
- Helps to achieve strong consistency and ACID guarantees
- Best for stateful databases

### Cons

- Single point of failure - If the server dies, the whole application collapses
- More costly compared to horizontal scaling, A machine with 128 cores costs more than 4 machines with 32 cores.
- A server can only by scaled up to a certain limit, after which we need to scale it out.

## What to choose and when ?

It depends on our use case,

- For stateless servers, we can scale them out horizontally, for stateful databases, we scale them vertically as much as we can
- Vertical scaling preserves the ACID gurantees and keeps architecture simpler, we only shard when we hit the limit on one single server
- For applications with high read traffic, we can use horizontal scaling by using read replicas, for applications with high write traffic, we can use vertical scaling by using a powerful machine to handle the writes.
- For applications with high availability requirements, we can use horizontal scaling by using multiple servers to provide redundancy and fault tolerance, for applications with low availability requirements, we can use vertical scaling by using a single powerful server to handle the traffic.
- For applications which are simpler and in initial stages of development, we can use vertical scaling to keep the architecture simpler, and we keep scaling vertically until we hit the limit of one single server, after which we can switch to horizontal scaling by sharding our database and adding more servers to handle the traffic.

In general, we can start with vertical scaling and then switch to horizontal scaling when we hit the limits of vertical scaling. This way we can keep our architecture simpler in the initial stages of development and then scale it out as our application grows.

---