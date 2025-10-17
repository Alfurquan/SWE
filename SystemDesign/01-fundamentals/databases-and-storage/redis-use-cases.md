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

### Example: Fixed Window Counter

This is the simplest method where Redis maintains a counter for each user/IP within a time window.

```python
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def is_request_allowed(user_id, max_requests=5, time_window=60):
    key = f"rate_limit:{user_id}"

    request_count = redis_client.incr(key)

    if request_count == 1:
        redis_client.expire(key, time_window)

    return request_count <= max_requests
```

## Distributed locks

In a distributed system, multiple nodes (servers) may try to modify the same shared resource at the same time. Without proper synchronization, this can lead to race conditions, inconsistencies, or data corruption.

A distributed lock ensures that only one process at a time can modify the resource.

The simplest way to implement a distributed lock in Redis is by using the atomic SETNX (Set if Not Exists) command:

```shell
SETNX lock_key "locked"
```

### How It Works

- Client 1 requests a lock
  - It executes SETNX lock_key "locked" to create the lock.
  - If the key does not exist, Redis sets the key and returns 1, indicating that the lock has been acquired.
- Client 1 performs its task
- Client 1 releases the lock
  - Once done, it deletes the key (DEL lock_key) to release the lock.
- Client 2 tries to acquire the lock
  - If the key is already set, SETNX returns 0, meaning another process is holding the lock.
  - Client 2 will need to wait and retry until the lock is released.

### Code Sample

```python
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def acquire_lock(lock_name, timeout=10):
    """
    Try to acquire a distributed lock
    """
    success = redis_client.set(lock_name, 'locked', ex=timeout, nx=True)
    return success is not None

def release_lock(lock_name):
    """
    Release the distributed lock
    """
    redis_client.delete(lock_name)

lock_name = "resource_lock"

if acquire_lock(lock_name):
    print("Lock acquired, processing task...")
    time.sleep(5)
    release_lock(lock_name)
    print("Lock released")
else:
    print("Lock is already held by another process")
```

## Real Time Leaderboard

Leaderboards are a common feature in many applications.

- Gaming Apps (e.g., PUBG, Fortnite, Call of Duty) – Rank players based on their scores, or win rates.
- E-Commerce (e.g., Amazon, Flipkart) – Display top sellers or most popular products.
- Social Media (e.g., Twitter, TikTok, Instagram) – Rank trending hashtags, or viral posts.

Implementing a scalable and efficient leaderboard is challenging, especially when dealing with millions of users and frequent score updates in real time.

Redis’ Sorted Set (ZSET) data structure provides a powerful and efficient way to manage leaderboards with fast ranking and retrieval operations.

A Sorted Set is a collection of unique elements, each with a score associated with it. The elements are sorted by score. Internally, Redis implements Sorted Sets using a combination of a hash table and a skip list, enabling O(log N) time complexity for insertions, deletions, and ranking operations.

### Code Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def add_player(player, score):
    redis_client.zadd("game_leaderboard", {player: score})

def get_top_players(n):
    """
    Fetch top n players based on scores
    """
    return redis_client.zrevrange("game_leaderboard", 0, n - 1, withscores=True)

def update_player(player, score_increment):
    """
    Increase player score
    """
    redis_client.zincrby("game_leaderboard", score_increment, player)
```

## Message queues

In modern distributed systems, components often need to communicate asynchronously to handle tasks efficiently. Instead of waiting for responses, systems use message queues to decouple components, ensuring scalability and fault tolerance.

Redis provides lightweight message queuing mechanisms, making it an excellent choice for:

- Job queues (e.g., processing image uploads, sending emails)
- Asynchronous API calls (e.g., logging, analytics)
- Background tasks (e.g., scheduled notifications, billing jobs)
- Simple chat applications

Redis supports two popular approaches for implementing message queues:

- Redis Lists (FIFO Queue)
- Redis Pub/Sub

### Redis Lists (FIFO Queue)

Redis Lists can function as simple First-In-First-Out (FIFO) queues, where messages are added to the left side and consumed from the right side.

#### How it works

- Producers push messages into a Redis List using LPUSH queue message.
- Consumers fetch messages from the queue using BRPOP (blocking pop).
- Messages are removed once consumed to prevent duplication. Use BRPOPPUSH to persist messages in a backup queue (like Kafka).

#### Code example

Producer

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def produce_message(queue_name, message):
    redis_client.lpush(queue_name, message)

produce_message("email_queue", "Send welcome email to user@example.com")
produce_message("email_queue", "Send password reset email to user@example.com")
```

Consumer

```python
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def consume_message(queue_name):
    while True:
        _, message = redis_client.brpop(queue_name)
        print(f"Processing message: {message.decode('utf-8')}")

consume_message("email_queue")
```

A limitation of this approach is the lack of built-in consumer groups, which means messages cannot be efficiently distributed among multiple consumers.

### Redis Pub/Sub

Redis provides Publish-Subscribe (Pub/Sub) messaging, allowing instant event broadcasting to multiple consumers.

#### How it works

- A publisher sends messages to a channel using the PUBLISH channel message command.
- Subscribers listening to the channel instantly receive the message.
- Messages are not stored; they are only delivered if subscribers are online.

#### Code example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def publish_message(channel, message):
    redis_client.publish(channel, message)
publish_message("notifications", "New user signed up: user@example.com")

def subscribe_channel(channel):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")
```

While Redis Pub/Sub is ideal for fire-and-forget messaging, it lacks reliability mechanisms such as message persistence, guaranteed delivery, and ordered message processing, making it unsuitable for mission-critical or large-scale distributed messaging systems.

## Real time analytics

Real-time analytics solves this problem by providing instant insights, enabling businesses to react within milliseconds instead of waiting for hours or days.

Redis is a great choice for real-time analytics since it’s blazing fast, provides data structures optimized for counting (INCR, PFADD, ZINCRBY) and atomic operations to avoid race conditions. It also supports HyperLogLog data structure for approximate counting with low memory footprint.

## Social media timeline

A social network timeline is one of the most complex features to build at scale. When you open X, Instagram, or Facebook, your feed displays posts from users, influencers, and brands across the globe in real time.

Redis is fast and supports ordered data structures like Sorted Sets, making it ideal for building real-time social media feeds. With low-latency operations, Redis can store and retrieve posts in milliseconds, ensuring that users always see the latest updates instantly.

There are two main ways to structure a timeline in Redis:

### Fan-Out on Write (Push Model)

When a user posts, the system automatically pushes the post to all their followers’ timelines.

How It Works?

- User posts content → Redis stores the post.
- The post (postId) is copied to all followers’ feeds.
- Followers see the update instantly when they open their timeline.

#### Code Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def post_content(user, post_content):
    post_id = f"post:{user}:{int(time.time())}"
    redis_client.set(post_id, post_content)

    followers = redis_client.smembers(f"followers:{user}")

    for follower in followers:
        redis_client.zadd(f"timeline:{follower.decode('utf-8')}", {post_id: time.time()})
    
    print(f"Post {post_id} created and pushed to followers' timelines.")
```

It works well for smaller accounts with a manageable number of followers. However, for celebrities or popular pages with millions of followers, this method becomes inefficient, as every new post needs to be copied to an enormous number of timelines.

### Fan-Out on Read (Pull Model)

Instead of pushing posts to followers, this method fetches posts dynamically when a user opens their feed.

How It Works?

- User posts content → Post is stored in Redis once.
- Followers do not receive the post immediately.
- When a user opens their feed, Redis pulls posts from all the accounts they follow and merges them.

#### Code Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def post_update(user, post_content):
    """
    Store a post without pushing to followers
    """
    post_id = f"post:{user}:{int(time.time())}"
    redis_client.set(post_id, post_content)
    redis_client.zadd(f"posts:{user}", {post_id: time.time()})
    print(f"Post {post_id} created.")

post_update("celebrity_user", "New post from celebrity!")

def get_dynamic_timeline(user, count = 10):
    """
    Fetch and merge posts from followed users
    """
    followed_users = redis_client.smembers(f"following:{user}")

    posts = []

    for followed in followed_users:
        user_posts = redis_client.zrevrange(f"posts:{followed}", 0, count - 1, withscores=True)
        posts.extend(user_posts)

    posts.sort(reverse=True, key=lambda post_id: int(post_id.decode().split(':')[-1]))

    return [redis_client.get(post_id.decode()).decode() for post_id, _ in posts[:count]]

timeline = get_dynamic_timeline("regular_user")
```

This approach optimizes write efficiency by storing each post only once, making it highly scalable for large accounts. Since posts aren’t duplicated across millions of followers, it significantly reduces storage costs and write overhead.

However, it comes at the cost of slightly slower reads, as the system must fetch and merge posts dynamically from multiple sources each time a user loads their feed.

### Hybrid

Many platforms use both methods – Fan-out on Write for regular users and Fan-out on Read for celebrities.

## Flash Sale

Flash sales, such as Black Friday, Cyber Monday, or Big Billion Day create massive spikes in traffic that can overwhelm databases and application servers.

These sales often lead to:

- High concurrency – Thousands/millions of users competing for limited stock.
- Race conditions – Multiple users trying to buy the same item at the same time.

Redis helps solve these challenges with its ultra-fast in-memory storage, atomic operations to ensure stock updates without race conditions, and distributed locking to prevent double checkouts and overselling.

### Code Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Set initial stock
redis_client.set("item_stock:iphone16", 100)

def purchase_item(user_id, item):
    stock_left = redis_client.decr(f"item_stock:{item}")

    if stock_left >= 0:
        print(f"User {user_id} successfully purchased {item}. Stock left: {stock_left}")
    else:
        redis_client.incr(f"item_stock:{item}")  # Revert the decrement
        print(f"User {user_id} failed to purchase {item}. Out of stock.")
```

- Redis stores the stock count of each product (SET item_stock:iphone16 100).
- Each purchase request decrements the stock (DECR item_stock:iphone16).
- If stock reaches zero, no further purchases are allowed.

## Geospatial Indexing

Many modern applications require the ability to store, retrieve, and query location-based data efficiently. Examples include:

- Ride-sharing apps (Uber, Lyft, Ola) – Finding the nearest drivers.
- Food delivery services (Swiggy, DoorDash) – Assigning the closest restaurants/delivery agents.

Redis provides a built-in Geospatial Indexing feature with O(log N) query performance that makes storing and querying location-based data fast and scalable

It uses a Geospatial Index based on Sorted Sets (ZSET) to store location coordinates (latitude, longitude) as a single unique score.

Redis Geospatial commands include:

- GEOADD: Add geospatial items to the index.
- GEORADIUS: Query items within a specified radius.
- GEODIST: Get the distance between two geospatial items.

### Code Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def add_location(store_name, longitude, latitude):
    redis_client.geoadd("stores", (longitude, latitude, store_name))

def get_distance(store1, store2, unit='km'):
    return redis_client.geodist("stores", store1, store2, unit=unit)

def find_nearby_stores(longitude, latitude, radius, unit='km'):
    return redis_client.georadius("stores", longitude, latitude, radius, unit=unit)
```

- Locations are stored in Redis using a Geospatial Index.
- Supports units: meters (m), kilometers (km), miles (mi), and feet (ft).
- Uses optimized geospatial algorithms to compute distances instantly.
- Useful for finding nearby stores, drivers, events, etc.

---