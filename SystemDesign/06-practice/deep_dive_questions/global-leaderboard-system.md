# 🎙️ The Scenario: "The Global Gaming Leaderboard"

Interviewer: "We are launching a new competitive mobile game. We expect 10 million Daily Active Users (DAU). At the end of every match (which lasts about 5 minutes), a player's score is updated.

We need to provide two features:

- The Global Top 100: A real-time leaderboard showing the top 100 players in the world.
- 'Near Me' Rankings: A user should be able to see their own rank and the 5 players immediately above and below them (e.g., 'You are ranked #5,402').

The Constraint: The leaderboard must be 'real-time' (less than 2 seconds of lag).

The Question: How do you handle the high frequency of score updates while keeping the ranking logic fast? Specifically:

- What is your primary storage engine for the scores and ranks, and why?
- Scale Math: If 10M users play 5-minute matches throughout a 12-hour peak window, what is the Average Writes Per Second the storage engine must handle?
- Architecture: Will you use a 'Relational' approach (SQL ORDER BY) or something else?"

## 💡 Your Task

- Pick your Storage: (Redis, DynamoDB, Postgres, etc.) and justify it.
- Do the Math: Calculate the writes per second.
- Solve the "Rank" problem: How do you find someone's exact rank (e.g., #5,402) without scanning millions of rows?

---

## Solution

### Functional requirements

We are designing a global leaderboard system with two features

- The Global Top 100: A real-time leaderboard showing the top 100 players in the world.
- 'Near Me' Rankings: A user should be able to see their own rank and the 5 players immediately above and below them (e.g., 'You are ranked #5,402').

### Non functional requirments

- The leaderboard must be 'real-time' (less than 2 seconds of lag).
- Scale: 10 million Daily active users, each match is 5 minutes.
- Latency: System must support low latency for score updates and fetching ranks.
- Accuracy: System should not double count scores or display wrong scores for users
- Read to write ration: System has almost same read to write ratio.

### Scale math

10M users play 5-minute matches throughout 12 hour peak window. After every five minutes, we update the score.

Writes per 5-minute window:
10,000,000 users × 1 update = 10M writes per 5 minutes
Convert to per second:
10,000,000 / 300 = 33,333 writes/sec

### Data storage

In this leaderboard system, we should support fast score updates and fast ranking logic. So we need a data structure which would support both in quick time.

So here, we would be using redis as the data store for scores. We would also be propagating the score updates from redis to a database like PostgreSQL for permanent storage and analytics later.

#### Reasons for choosing redis

Redis has a data structure called `sorted_sets(ZSET)` which basically is a collection of entities mapped to a score. It keeps the entities sorted by their score. Under the hood `sorted_set` uses a hashmap and a skip list. It uses hashmap to map players to scores and skip_list to stores members sorted by score. HashMap gives `O(1)` lookups for a player scoe. This allows for fast insertion and updates with time complexity of O(logN)

So whenever a player's score is updated, we run below command

```
ZADD leaderboard <score> <player_id>
```

This is O(logN) operations, so even with 10 million players, it would be about log(10^7) = 7 * log(10) = 7 * 3.3 = 23.1 operations, which is very fast.

When we want to fetch the top 100 players, we can use below command

```ZREVRANGE leaderboard 0 99 WITHSCORES
```

This is O(logN + M) where M is the number of players we want to fetch, in this case 100. So it would be about 23.1 + 100 = 123.1 operations, which is also very fast.

To fetch the 'Near Me' rankings, we can use below command

```ZRANK leaderboard <player_id>
```

This is O(logN) operation, so it would be about 23.1 operations. Once we have the rank of the player, we can fetch the players around that rank using `ZREVRANGE` command.
This is quite efficient as well, as we are only fetching a small number of players around the user's rank and this is how we would find near me rankings without scanning millions of rows.


### High level design

Here is how the system would work at a high level

#### Update score flow

- The client sends a POST call to /score with the score of the player. The client generates a unique `event_id` and sends it in as well. This id would be used as an idempotency key to avoid double counting the players score.
- The API gateway receieves the call, it does basic validations, auth, and passes the request to the leaderboard service.
- The service first writes the request payload (as below) to a small outbox layer. (This layer is used later on to flush data to kafka when the kafka crashes and recovers, we would come it in a bit)

```json
{
    "event_id": <>,
    "player_id":<>,
    "score":<>,
    "timestamp":<>
}
```
- The service updates redis and returns back to the client
- A background publisher reads from outbox, publishes to kafka and marks events as sent.
- We have used kafka here as a bridge to update the database when redis is updated. Kafka is an append only commit log which allows for faster writes. It also allows at least once gurantees using offset tracking by consumers.
- We partition the kafka by player_id to make sure that each player's score is processed in order.
- Consumer groups of workers consume from these partitions to update the database with the player's score.

Here we have chosen redis first and then kafka -> database, because we have the requirement of keeping score updates fast and redis helps doing it. Also database will be used for analytics purpose so even a slight lag there is fine.

Now there can be failure situations here and here is how we would handle them

#### Failure conditions in update score flow

- Worker crashes after updating redis but before writing to kafka: In this case, we would have the score updated in redis but not in database. To handle this, we have the outbox layer where we write the payload before updating redis. So if the worker crashes after updating redis but before writing to kafka, we can replay the outbox and update kafka and database later on.

- Kafka crashes: If kafka crashes, we would have the score updated in redis but not in database. To handle this, we can replay the outbox and update kafka and database later on when kafka recovers.

- Consumer worker crashes after consuming the message from kafka but before updating the database: In this case, we would have the score updated in redis but not in database. To handle this, we can use kafka's offset tracking to make sure that we reprocess the message when the worker recovers.

- Redis crashes: If redis crashes, we would lose the scores in redis. To handle this, we can use redis persistence options like RDB or AOF to persist the data to disk and recover it later on when redis recovers. We can also have a backup redis instance to switch to in case of a crash.

#### Idempotency

We are using the `event_id` generated by the client as an idempotency key to avoid double counting the player's score.

Here is how we would handle idempotency across different components

- Redis: When we receive a score update, we use the `ZADD` command to update the player's score in redis. If a duplicate `event_id` comes in for the same player, we can ignore it as the score would already be updated in redis. How do we check for duplicate `event_id`? We can maintain a separate set in redis to store the `event_id`s that have been processed. Before processing a score update, we can check if the `event_id` is already in the set. If it is, we can ignore the update. If it is not, we can process the update and add the `event_id` to the set.

- Database: We would add a unique constraint on the `event_id` column in the database to ensure that duplicate `event_id`s are not inserted into the database. If a duplicate `event_id` comes in, the database would throw an error and we can catch that error to ignore the update. So even if the consumer worker crashes after consuming the message from kafka but before updating the database, we would not have duplicate entries in the database as the unique constraint on `event_id` would prevent that.

#### Getting the top 100 players flow

- The client sends a GET call to /leaderboard/top100
- The API gateway receives the call, does basic validations, auth, and passes the request to the leaderboard service.
- The service then fetches the top 100 players from redis using `ZREVRANGE` command and returns the response to the client.

#### Getting 'Near Me' rankings flow

- The client sends a GET call to /leaderboard/nearby with the player_id
- The API gateway receives the call, does basic validations, auth, and passes the request to the leaderboard service.
- The service then fetches the rank of the player using `ZRANK` command and then fetches the players around that rank using `ZREVRANGE` command and returns the response to the client.

---
## 🎙️ The Final "Stress Test" Question
You've built a robust system. I have one final follow-up for this design:

Interviewer: "Your system handles a 500-second window for the 50M notifications (from the last problem) and 33k writes/sec here. But what happens during 'The Midnight Reset'? If this is a daily leaderboard that resets at midnight, 10 million users might all hit the system at once to see their final rank and start the new day. How do you prevent a Thundering Herd from crashing your Redis or API Gateway at exactly 12:00:00 AM?"

How would you handle a massive, synchronized spike in reads/writes at a specific time?

### Answer

To solve the "Thundering Herd" problem during the "Midnight Reset", we can use a combination of techniques to ensure that our system can handle the spike in traffic without crashing. We can use request coalescing to allow only one request to go through and build the redis cache from the database. Once its built, we can serve the rest of the requests from redis.

How would this work in practice?
- At midnight, when the reset happens, the API gateway would receive a large number of requests to fetch the leaderboard data. Instead of allowing all these requests to hit the Redis cache at once, we can implement a locking mechanism at the API gateway level.
- The first request that comes in would acquire a lock (e.g., using a distributed locking mechanism like Redis' SETNX command). This request would then be responsible for fetching the latest leaderboard data from the database and populating the Redis cache.
- While the first request is fetching and populating the cache, any subsequent requests that come in during this time would check for the lock. If the lock is present, they would wait for a short period (e.g., 100ms) and then check again. This way, we are effectively coalescing the requests and preventing a thundering herd from hitting Redis at once.

