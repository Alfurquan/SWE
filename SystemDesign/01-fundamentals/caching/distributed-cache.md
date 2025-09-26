# Distributed Caching?

Caching is used to temporarily store copies of frequently accessed data in high-speed storage layers (such as RAM) to reduce latency and load on the server or database.

When your dataset size is small, it’s usually enough to keep all the cache data on one server.

But as the system gets bigger, the cache size also gets bigger and a single-node cache often falls short when scaling to handle millions of users and massive datasets.

In such scenarios, we need to distribute the cache data across multiple servers.

This is where distributed caching comes into play.

## What is Distributed Caching?

Distributed caching is a technique where cache data is stored across multiple nodes (servers) instead of being confined to a single machine.

This allows the cache to scale horizontally and accommodate the needs of large-scale applications.
