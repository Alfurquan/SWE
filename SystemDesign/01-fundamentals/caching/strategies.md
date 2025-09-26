# Caching Strategies

There are several caching strategies, depending on what a system needs - whether the focus is on optimizing for read-heavy workloads, write-heavy operations, or ensuring data consistency.

## Read through

In the Read Through strategy, the cache acts as an intermediary between the application and the database.

When the application requests data, it first looks in the cache.

If data is available (cache hit), it’s returned to the application.
If the data is not available (cache miss), the cache itself is responsible for fetching the data from the database, storing it, and returning it to the application.

This approach simplifies application logic because the application does not need to handle the logic for fetching and updating the cache.

The cache itself handles both reading from the database and storing the requested data automatically. This minimizes unnecessary data in the cache and ensures that frequently accessed data is readily available.

To prevent the cache from serving stale data, a time-to-live (TTL) can be added to cached entries. TTL automatically expires the data after a specified duration, allowing it to be reloaded from the database when needed.

**Read Through caching is best suited for read-heavy applications where data is accessed frequently but updated less often, such as content delivery systems (CDNs), social media feeds, or user profiles.**

## Cache aside

Cache Aside, also known as "Lazy Loading", is a strategy where the application code handles the interaction between the cache and the database. The data is loaded into the cache only when needed.

The application first checks the cache for data. If the data exists in cache (cache hit), it’s returned to the application.

If the data isn't found in cache (cache miss), the application retrieves it from the database (or the primary data store), then loads it into the cache for subsequent requests.

The cache acts as a "sidecar" to the database, and it's the responsibility of the application to manage when and how data is written to the cache.

**Cache Aside is perfect for systems where the read-to-write ratio is high, and data updates are infrequent. For example, in an e-commerce website, product data (like prices, descriptions, or stock status) is often read much more frequently than it's updated.**

## Write Through

In the Write Through strategy, every write operation is executed on both the cache and the database at the same time.

This is a synchronous process, meaning both the cache and the database are updated as part of the same operation, ensuring that there is no delay in data propagation.

This approach ensures that the cache and the database remain synchronized and the read requests from the cache will always return the latest data, avoiding the risk of serving stale data.

**Write Through is ideal for consistency-critical systems, such as financial applications or online transaction processing systems, where the cache and database must always have the latest data.**

## Write Around

Write Around is a caching strategy where data is written directly to the database, bypassing the cache.

The cache is only updated when the data is requested later during a read operation, at which point the Cache Aside strategy is used to load the data into the cache.

It keeps the cache clean by avoiding unnecessary data that might not be requested after being written.

**Write Around caching is best used in write-heavy systems where data is frequently written or updated, but not immediately or frequently read such as logging systems.**

## Write Back

In the Write Back strategy, data is first written to the cache and then asynchronously written to the database at a later time.
This strategy focuses on minimizing write latency by deferring database writes.

The key advantage of Write Back is that it significantly reduces write latency, as writes are completed quickly in the cache, and the database updates are delayed or batched.

**Write Back caching is ideal for write-heavy scenarios where write operations need to be fast and frequent, but immediate consistency with the database is not critical, such as logging systems and social media feeds.**
