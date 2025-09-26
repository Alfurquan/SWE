# Caching

Caching is a technique used to temporarily store copies of data in high-speed storage layers (such as RAM) to reduce the time taken to access data.

The primary goal of caching is to improve system performance by reducing latency, offloading the main data store, and providing faster data retrieval.

## Why use caching ?

- Improved Performance: By storing frequently accessed data in a cache, the time required to retrieve that data is significantly reduced.

- Reduced Load on Backend Systems: Caching reduces the number of requests that need to be processed by the backend, freeing up resources for other operations.

- Increased Scalability: Caches help in handling a large number of read requests, making the system more scalable.

- Cost Efficiency: By reducing the load on backend systems, caching can help lower infrastructure costs.

- Enhanced User Experience: Faster response times lead to a better user experience, particularly for web and mobile applications.

## Types of caching

- In memory cache: In-memory caches store data in the main memory (RAM) for extremely fast access. E.g: Redis and Memcached

- Distributed Cache: A distributed cache spans multiple servers and is designed to handle large-scale systems. E.g.: Redis Cluster and Amazon ElastiCache.

- Client-Side Cache: Client-side caching involves storing data on the client device, typically in the form of cookies, local storage, or application-specific caches.

- Database Cache: Database caching involves storing frequently queried database results in a cache.

- Content Delivery Network (CDN): CDN is used to store copies of content on servers distributed across different geographical locations.
