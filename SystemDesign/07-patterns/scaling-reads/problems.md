# Problems

## Question 1: The "Too Many Indexes" Trap

Scenario: You are designing a logging system that is extremely write-heavy (100k writes/sec). A junior engineer suggests adding indexes on the timestamp, log_level, and service_name columns to speed up the dashboard reads.

Question: based on the notes, why might you hesitate to add all three indexes here, specifically regarding the "Read vs. Write Tension"? Conversely, if this were a read-heavy e-commerce app, how would your answer change?

Key Concept: Understanding when index overhead on writes is actually a problem vs. when it is "dramatically overblown".

---

## Answer

In a write-heavy logging system, adding indexes on multiple columns will have a negative impact on write latency. Now for every write to every row, we will need to update the indexes. This will slow down the writes. For a write-heavy logging system, we would need writes to be faster and have low latency as there would be millions of write requests coming per second. Adding these many indexes would be slowing down the writes hence we should avoid adding them.

If this were a read-heavy ecommerce app, then adding indexes would be beneficial. It would speed up the reads as instead of doing full table scan we can use the indexes to directly to the row having the record. Also we should be indexing columns which are used frequently in the queries to serve read requests.

---

## Question 2: The Denormalization Trade-off

Scenario: You have an Orders table and a Users table. Your "Order History" page is slow because it joins these tables to display the user_name alongside every order. You decide to denormalize by adding a user_name column directly to the Orders table.

The Question:
Six months later, a user changes their name.

Describe the exact sequence of updates required now (Pseudocode or step-by-step is fine).

What happens if the update fails halfway through? How does this impact the user experience?

## Answer

These are the sequence of steps needed

- Begin a transaction
- Update the user name in the users table
- Update the user name in the orders table.
- Commit the transaction
- if any step fail, rollback the transaction

If the update fails halfway like, the user name got updated in users table, but failed to get updated in orders table, then we would rollback the transaction. This rollback is needed if we want the system to be strongly consistent,

This will impact the user experience as the user will not see the updated name in the order history page until the transaction is successfully committed. If the transaction fails and rolls back, then the user will not see any change in their name in both users and orders table. This can lead to confusion for the user as they might think that their name change was successful when it was not.
To mitigate this, we can implement a retry mechanism for the transaction to ensure that it eventually succeeds, or we can use an eventual consistency model where the user name in the orders table is updated asynchronously after the user name in the users table is updated. This way, the user will see the updated name in the users table immediately, and the orders table will eventually reflect the change without blocking the user experience.

---

## Question 3: Materialized View Lag

Scenario: You are using a Materialized View to precompute the "Average Product Rating" for an Amazon-like page. This avoids running an expensive AVG() query on the Reviews table (which has millions of rows) every time a user loads a product page.

The Situation:
A user submits a 1-star review for a product. They immediately refresh the page to see the new score, but the "Average Rating" hasn't changed.

The Questions:

Is this a bug? Why or why not?

The Product Manager files a high-priority ticket saying "The site is broken, ratings aren't updating." How do you explain to them—in simple terms—why we designed it this way and why "fixing" it might crash the site?

## Answer

This is not a bug as we are precomputing the average product rating in a materialized view using a background job at certain intervals. So even if the user submits a rating, he may not see the average rating change immediately. This precomputing is needed to avoid running an expensive AVG() query on reviews table every time a user loads a product page.

I would explain them that we are precomputing the average product rating in a materialized view using a background job at certain intervals. This is needed to avoid running an expensive AVG() query on the Reviews table (which has millions of rows) every time a user loads a product page. If we did not do this, then every time the user opens the product page, we would be running an AVG() query on million of rows, this would slow down the reads and for a read heavy system like the ecommerce app it would lead to a very bad user experience as it would take a long time to load the product page. Also since the system is read heavy, we would have a lot of users trying to load the product page at the same time, this would lead to a lot of AVG() queries running at the same time which would crash the database.

So we have to precompute the average rating and update it at certain intervals, this way we can ensure that the product page loads quickly while still providing reasonably up-to-date average ratings.

---

## Question 4: The Replication Lag Edge Case

Scenario: You have configured a standard Leader-Follower replication topology. A user updates their profile picture (Write to Leader), then immediately refreshes the page. The request goes to a Follower (Read Replica), which hasn't received the data yet, so the user sees their old picture.

The Question:
This is "Replication Lag". Without changing your database infrastructure to synchronous replication (which kills write latency), how can you modify your application routing logic to ensure the user sees their own update immediately?

## Answer

When a user updates their profile page and then refreshes the page, we would use something called `read your writes` consistency. We would route the user's request to the leader. In this way the user would see their own update immediately as the read request would go to the leader which has the most up-to-date data. This way we can ensure that the user sees their own update immediately without changing our database infrastructure to synchronous replication. 

Other users who are trying to read the same profile picture would still be routed to the followers, so they might see the old picture until the replication lag is resolved. This is a trade-off we have to make in order to ensure that the user who made the update sees their own update immediately while still allowing other users to read from the followers without impacting write latency.

Another approach could be to use a cache layer like Redis or Memcached to store the most recent updates. When a user updates their profile picture, we can update the cache with the new picture URL. Then when the user refreshes the page, we can check the cache first for the most recent picture URL before querying the database. This way we can ensure that the user sees their own update immediately while still allowing other users to read from the followers without impacting write latency.

---

## Question 5: Sharding vs. Replication

Scenario: Your database is handling 20,000 read queries per second (QPS) just fine. The CPU load is low (20%). However, your monitoring triggers a critical alert: Disk Storage is 95% full (The dataset has grown to 50TB).

The Question:
You have two options to fix this immediately:

Add 3 more Read Replicas.
Shard the database into 3 shards.

Which option do you choose? Explain strictly why the other option would fail to solve the problem.

## Answer

To solve the disk storage 95% full problem, we would need to shard the database into 3 shards. Read replicase here won't solve the problem as the issue here is with the database size and not read latency. If read latency would have increased then adding more read replicas would have been a good solution. But since the issue is with the disk storage being full, adding more read replicas would not solve the problem as they would still be replicating the same data and hence would also run out of disk storage.

Sharding the database into 3 shards would solve the problem as it would distribute the data across multiple servers, thus reducing the disk storage usage on each server. Each shard would contain a subset of the data, so the total disk storage used across all shards would be less than 95%. This way we can ensure that we have enough disk storage to handle the growing dataset while still maintaining good read performance.

---

## Question 6: The "Justin Bieber" Problem (Hot Keys)
Scenario: A celebrity tweets. Suddenly, 500,000 requests/sec hit your cache for that specific tweet ID (tweet:12345).

Your cache cluster handles 10M QPS total, but it is sharded by key.

This specific key (tweet:12345) hashes to Node A.

Node A can only handle 50,000 QPS. It crashes.

The Question:
You mentioned "Cache Key Fanout" in your notes.

Write the pseudocode (or step-by-step logic) for how you would write this key to the cache.

Write the pseudocode for how you would read this key from the cache to ensure Node A doesn't crash.

## Answer

To write the key to the cache, we can use a technique called "Cache Key Fanout". This involves writing the same data to multiple keys in the cache, each with a different hash. This way, when we read the data, we can read from multiple keys and distribute the load across multiple nodes.

Step-by-step logic for writing the key to the cache:
1. Generate multiple keys for the same data, for example: tweet:12345:1, tweet:12345:2, tweet:12345:3, etc.
2. Write the same data (the tweet) to each of these keys in the cache.
function writeToCache(tweetId, tweetData) {
    for (let i = 1; i <= 10; i++) {
        let cacheKey = `tweet:${tweetId}:${i}`;
        cache.set(cacheKey, tweetData);
    }
}

Step-by-step logic for reading the key from the cache:
1. Generate random keys for the same data, for example: tweet:12345:1, tweet:12345:2, tweet:12345:3, etc.
2. Read from one of these keys randomly to distribute the load across multiple nodes.

function readFromCache(tweetId) {
    let randomIndex = Math.floor(Math.random() * 10) + 1; // Random number between 1 and 10
    let cacheKey = `tweet:${tweetId}:${randomIndex}`;
    return cache.get(cacheKey);
}

In this way, when a celebrity tweets and we have a sudden spike in requests for that specific tweet ID, the load will be distributed across multiple nodes in the cache cluster, preventing Node A from crashing. Each node will handle a portion of the requests, allowing us to serve the data efficiently without overwhelming any single node.

---

## Question 7: The Thundering Herd (Cache Stampede)

Scenario: Your homepage cache expires every 60 minutes. At minute 60:01, latency spikes to 10 seconds and the DB CPU hits 100%.

The Question:
You want to implement "Probabilistic Early Refresh" to fix this.

If a user requests the page at minute 55, and your random number generator hits the "refresh" probability (e.g., you rolled a 1 on a d100), what exactly does the application do?

Crucially: Does the user wait for the refresh to finish? Why or why not?

## Answer

If a user requests the page at minute 55 and the random number generator hits the "refresh" probability, the application will trigger a refresh of the cache for the homepage. This means that it will start a background process to fetch the latest data from the database and update the cache.

The user does not wait for the refresh to finish. This is because the "Probabilistic Early Refresh" technique is designed to prevent a thundering herd of requests from overwhelming the database when the cache expires. By allowing the user to continue with their request while the cache is being refreshed in the background, we can ensure that the user experience remains smooth and responsive, even during cache refreshes. The user will receive the old cached data while the new data is being fetched and updated in the cache, thus avoiding any latency spikes or database overload.

This way we can ensure that the user experience remains consistent and that the database is not overwhelmed by a sudden surge of requests when the cache expires.

---

## Question 8: Versioned Caching vs. Invalidation

Scenario: You are building an inventory system where data must be consistent. You are currently using "write-through invalidation" (updating the DB, then deleting the cache key), but you are seeing race conditions where stale reads re-populate the cache with old data right after you delete it.

The Question:

How does switching to "Versioned Keys" (e.g., changing the key from product:123 to product:123:v4) eliminate the need for complex invalidation logic and race conditions?

The Trade-off: What is the specific cost of this approach regarding the number of round trips to the cache/DB for every single read request?

## Answer

Switching to "Versioned Keys" eliminates the need for complex invalidation logic and race conditions because instead of deleting the cache key when the data is updated, we simply create a new version of the key. For example, if we have a product with ID 123, instead of using a single key like product:123, we can use versioned keys like product:123:v1, product:123:v2, etc. When we update the product information, we create a new version of the key (e.g., product:123:v4) and write the updated data to that key. This way, we never delete any keys, and there is no chance for stale reads to re-populate the cache with old data because the old keys still exist but are not used for reads.


The specific cost of this approach is that it requires an additional round trip to the cache/DB for every single read request. When a read request comes in, we first need to check the cache for the latest version of the key (e.g., product:123:v4). If it is not found in the cache, we then need to query the database to get the latest data and write it back to the cache with a new versioned key. This means that for every read request, we may have to perform two operations: one to check the cache and another to query the database if the cache miss occurs. This can increase latency for read requests, especially if there are frequent updates leading to multiple versions of keys being created.

This trade-off is important to consider because while versioned keys can simplify cache management and eliminate race conditions, it can also lead to increased latency for read requests due to the additional round trip to the cache/DB. It is essential to weigh the benefits of simplified cache management against the potential performance impact on read requests when deciding whether to use versioned keys in a caching strategy. Also it can lead to increased memory usage in the cache as we are not deleting old keys, so we need to have a strategy for cleaning up old versions of keys to prevent the cache from being filled with stale data.

---

