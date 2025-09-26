# Redis use case

Redis (Remote Dictionary Server) is an open source, in-memory key-value data store that provides sub-millisecond latency, making it an excellent choice for high-performance applications.

Redis supports a rich set of data structures, including strings, hashes, lists, sets, and sorted sets. These structures, combined with powerful atomic operations like INCR, DECR, and ZADD,enable Redis to handle many use cases requiring low latency and high throughput.

## Caching

Caching is the most common use case of Redis.

Since web applications frequently rely on databases, querying a database on every request can be slow and inefficient, leading to high response times and increased server load.

Redis solves this problem by storing frequently accessed data in memory, significantly reducing latency and offloading queries from the database.

There are multiple caching strategies (read through, cache aside, write back etc.,) each suited for different use cases.

The cache-aside pattern is widely used because it gives the application full control over caching logic.

- When a client requests data, the application first checks Redis.
- If the data exists in Redis (cache hit), it is returned instantly.
- If data is not found (cache miss), it is fetched from the database, stored in Redis for future requests, and returned to the client.
- To prevent stale or outdated data, Redis allows setting expiration times (TTL), ensuring automatic eviction of cached entries.

### Code sample

```python
import requests
import redis

cache = redis.Redis(host='localhost', port=3579, db = 0)

def get_weather(city):
    cache_key = f"weather:{city}"

    cached_data = cache.get(cache_key)
    if cached_data:
        print("cache hit")
        return cached_date.decode("utf-8")

    print("Cache miss, fetching from API")
    response = requests.get(f"<>")

    data = response.text

    cache.setex(cache_key, 60, data)
    return data
```

## Session store

Most modern web applications are stateless, meaning they don’t store session information directly on the server. However, to keep users logged in, maintain shopping carts, or track user preferences, web applications need a reliable session management system.

Since Redis is fast and provide persistent options, it’s a great choice for storing session data.

### How it works ?

#### User logs in

- The application generates a unique session ID for the user.
- It stores session data in Redis, using the session ID as the key.
- The session ID is sent to the user's browser as a cookie.

#### User Makes a Request

- The application retrieves the session ID from the user's cookie.
- It fetches user data from redis using session ID

#### Session expiration

- If a user is inactive for too long, Redis automatically deletes the session after a set expiration time (TTL).
- This prevents stale session accumulation, optimizing memory usage.

## Rate limiting

In modern applications, APIs and services often need to control the number of requests per user/IP to prevent abuse, ensure fair usage and protect servers from overload.

Redis is an ideal choice for rate limiting because it provides atomic counter (INCR) with expiration (EXPIRE).

When a request is made:

- A counter is incremented in Redis (INCR).
- If the counter exceeds the allowed limit, the request is rejected.
- The counter resets automatically after the time window expires (EXPIRE).

## Distributed locks

In a distributed system, multiple nodes (servers) may try to modify the same shared resource at the same time. Without proper synchronization, this can lead to race conditions, inconsistencies, or data corruption.

A distributed lock ensures that only one process at a time can modify the resource.

The simplest way to implement a distributed lock in Redis is by using the atomic SETNX (Set if Not Exists) command:

```shell
SETNX lock_key "locked"
```

## Message queues

In modern distributed systems, components often need to communicate asynchronously to handle tasks efficiently. Instead of waiting for responses, systems use message queues to decouple components, ensuring scalability and fault tolerance.

Redis supports two popular approaches for implementing message queues:

- Redis Lists (FIFO Queue)
- Redis Pub/Sub

## Real time analytics

Real-time analytics solves this problem by providing instant insights, enabling businesses to react within milliseconds instead of waiting for hours or days.

Redis is a great choice for real-time analytics since it’s blazing fast, provides data structures optimized for counting (INCR, PFADD, ZINCRBY) and atomic operations to avoid race conditions. It also supports HyperLogLog data structure for approximate counting with low memory footprint.

## Social media timeline

Redis is fast and supports ordered data structures like Sorted Sets, making it ideal for building real-time social media feeds. With low-latency operations, Redis can store and retrieve posts in milliseconds, ensuring that users always see the latest updates instantly.

There are two main ways to structure a timeline in Redis:

### Fan-Out on Write (Push Model)

When a user posts, the system automatically pushes the post to all their followers’ timelines.

How It Works?

- User posts content → Redis stores the post.
- The post (postId) is copied to all followers’ feeds.
- Followers see the update instantly when they open their timeline.

It works well for smaller accounts with a manageable number of followers. However, for celebrities or popular pages with millions of followers, this method becomes inefficient, as every new post needs to be copied to an enormous number of timelines.

### Fan-Out on Read (Pull Model)

Instead of pushing posts to followers, this method fetches posts dynamically when a user opens their feed.

How It Works?

- User posts content → Post is stored in Redis once.
- Followers do not receive the post immediately.
- When a user opens their feed, Redis pulls posts from all the accounts they follow and merges them.

This approach optimizes write efficiency by storing each post only once, making it highly scalable for large accounts. Since posts aren’t duplicated across millions of followers, it significantly reduces storage costs and write overhead.

However, it comes at the cost of slightly slower reads, as the system must fetch and merge posts dynamically from multiple sources each time a user loads their feed.

### Hybrid

Many platforms use both methods – Fan-out on Write for regular users and Fan-out on Read for celebrities.

## Geospatial Indexing

Many modern applications require the ability to store, retrieve, and query location-based data efficiently. Examples include:

- Ride-sharing apps (Uber, Lyft, Ola) – Finding the nearest drivers.
- Food delivery services (Swiggy, DoorDash) – Assigning the closest restaurants/delivery agents.

Redis provides a built-in Geospatial Indexing feature with O(log N) query performance that makes storing and querying location-based data fast and scalable

It uses a Geospatial Index based on Sorted Sets (ZSET) to store location coordinates (latitude, longitude) as a single unique score.