# Latency vs Throughput

Imagine you're at a popular new fast-food joint. You walk up to the counter and place your order.

- Latency is the time you personally wait from placing your order to getting your burger in hand. It's about how fast the system responds to a single request.
- Throughput is the number of total burgers the kitchen can produce and serve per hour. It’s a measure of how much work the system can handle over time.

## Latency

Latency is the time it takes for a request to complete. Its a delay between cause and effect.

Unit of measurement: Typically measured in milliseconds(ms) or seconds(s)

Latency is often reported in percentiles rather than just average:

- p50 (median): 50% of requests are faster than this value
- p95, p99, p99.9: Represents the worst-performing 5%, 1% and 0.1% of requests

**Example:** A p99 latency of 200ms means 99% of requests complete faster than 200ms, but the slowest 1% may take much longer.

Latency represents the experience of a single user or a single request. Lower latency is generally better.

### Strategies to Improve Latency

### Reduce Network Hops

- Fewer hops mean faster round trips.
- Use Content Delivery Networks (CDNs) to serve static assets like images, videos, and stylesheets from edge locations closer to the user.
- Leverage edge computing to run compute-heavy tasks or APIs geographically closer to end-users.

### Optimize Database Queries

- Use indexes to speed up read-heavy queries.
- Avoid full table scans by writing efficient SQL queries with proper filtering and joins.
- Implement connection pooling to reduce the overhead of establishing new DB connections for every request.

### Implement Caching

- Cache frequently accessed data in-memory using systems like Redis or Memcached.
- Use multi-layered caching: application-level, database query results, or CDN-based caching for static responses.
- Invalidate and refresh caches appropriately to avoid stale data.

### Use Efficient Algorithms & Data Structures

- Reduce CPU processing time by choosing the right data structures and optimizing your logic.
- Avoid unnecessary loops, redundant operations, and expensive computations during critical request paths.

### Enable Connection Keep-Alive

- Use persistent (keep-alive) connections to reuse TCP connections across multiple HTTP requests.
- This avoids the latency overhead of establishing new connections for every request.

### Use Compression (with Trade-offs)

- Compress responses (e.g., using gzip or brotli) to reduce payload size and improve transfer speed.
- Be mindful: Compression reduces bandwidth usage but adds CPU overhead for compression/decompression—evaluate the trade-off based on use case.
  
### Parallelize Independent Subtasks

- Break down complex operations into independent steps and execute them concurrently using threads, async calls, or task queues.
- This is especially useful in microservices where multiple internal APIs can be called in parallel.

### Choose Server Locations Strategically

- Deploy servers or regions closer to users to reduce propagation delays.
- Use multi-region deployments for global apps to ensure low-latency access across continents.

## Throughput

Throughput measures the rate at which a system processes requests or operations over time. It reflects the overall capacity or bandwidth of the system, how much work it can handle efficiently.

Measured In: Operations per second (ops/sec), requests per second (RPS), transactions per second (TPS), data processed per second (e.g., MB/s, GB/s).

**Examples:**

- Number of search queries Google handles per second.
- Number of orders an e-commerce site can process per minute.
- Amount of video data Netflix can stream per second.
- Number of messages a queue can process per hour.

Throughput represents a system’s processing power under load. Higher throughput generally means:

- More users can be served simultaneously
- Higher resource efficiency
- Better scalability

### Strategies to Improve Throughput

- Horizontal Scaling (Scale Out)
- Vertical Scaling (Scale Up)
- Asynchronous Processing
- Load Balancing
- Batch Processing

## Relationship between them

### Can you have Low Latency and High Throughput?

Yes! This is the ideal scenario.

Imagine a wide, empty superhighway where cars can drive fast and in large numbers. Each car (request) reaches its destination quickly (low latency), and many cars travel simultaneously (high throughput).

### Can you have Low Latency and Low Throughput?

Yes.
Think of a single-lane road with no traffic. Your car (request) gets through quickly, but only one or two cars can travel at a time.
This might be a system that's fast for one user but can't handle many concurrent users.

### Can you have High Latency and High Throughput?

Yes, this is common in batch processing systems.

Think of a cargo ship. It takes a long time for one specific container (request) to cross the ocean (high latency), but the ship carries thousands of containers at once (high throughput). Similarly, a data pipeline might take hours to process a day's worth of data, but it processes terabytes.

### Can you have High Latency and Low Yes. This is the worst-case scenario.

Imagine a narrow road filled with traffic and potholes. Cars move slowly (high latency), and very few can get through per hour (low throughput).

A system that is both slow and can't handle much load. Often caused by bottlenecks, poor design, or resource exhaustion.