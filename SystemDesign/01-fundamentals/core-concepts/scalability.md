# Scalability

A system that can continuously evolve to support a growing amount of work is scalable.

## How can a System Grow?

- Growth in user Base
- Growth in features
- Growth in data volume
- Growth in complexity
- Growth in geographic reach

## How to scale a system ?

### Vertical scaling (Scale up)

This means adding more power to your existing machines by upgrading server with more RAM, faster CPUs or additional storage. It's a good approach for simpler architectures but has limitations in how far you can go.

### Horizontal Scaling (Scale out)

This means adding more machines to your system to spread the workload across multiple servers.
It's often considered the most effective way to scale for large systems.

**Example:** Netflix uses horizontal scaling for its streaming service, adding more servers to their clusters to handle the growing number of users and data traffic.

### Load balancing

Load balancing is a process of distributing traffic across several servers so that none of the server becomes loaded.

**Example:** Google employs load balancing extensively across its global infrastructure to distribute search queries and traffic evenly across its massive server farms.

### Caching

Caching is a technique to store frequently accessed data in-memory (like RAM) to reduce the load on the server or database.

Implementing caching can dramatically improve response times.

**Example:** Reddit uses caching to store frequently accessed content like hot posts and comments so that they can be served quickly without querying the database each time.

### CDN

CDN distributes static assets (images, videos, etc.) closer to users. This can reduce latency and result in faster load times.

**Example:** Cloudflare provides CDN services, speeding up website access for users worldwide by caching content in servers located close to users.

### Sharding

Sharding means splitting data or functionality across multiple nodes/servers to distribute workload and avoid bottlenecks.

**Example:** Amazon DynamoDB uses sharding to distribute data and traffic for its NoSQL database service across many servers, ensuring fast performance and scalability.

### Asynchronous communication

Asynchronous communication means deferring long-running or non-critical tasks to background queues or message brokers.
This ensures your main application remains responsive to users.

**Example:** Slack uses asynchronous communication for messaging. When a message is sent, the sender's interface doesn't freeze; it continues to be responsive while the message is processed and delivered in the background.

### Microservices Architecture

Micro-services architecture breaks down application into smaller, independent services that can be scaled independently.

This improves resilience and allows teams to work on specific components in parallel.

**Example:** Uber has evolved its architecture into microservices to handle different functions like billing, notifications, and ride matching independently, allowing for efficient scaling and rapid development.
