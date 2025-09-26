# News-feed system (L5 strong answer)

## 1) Requirements (short)

**Functionals** - Post text/image/video, follow/unfollow, personalized
feed, like/comment/share, notifications.\
**Non-functionals** - Scale: \~10M daily active users, up to 100M
posts/day (example).\
- Throughput: thousands of posts/sec.\
- Latency: feed load p95 \< 200--500 ms.\
- Availability: high (SLOs), eventual consistency acceptable for feeds.\
- Read-heavy (reads ≫ writes).

## 2) High-level approach summary

-   Use a **hybrid feed generation**: *push (fan-out on write)* for
    low-fanout authors, *pull (fan-out on read)* for high-fanout
    authors.\
-   Kafka as the streaming backbone for all events (posts, likes,
    comments, follows).\
-   Materialize per-user timelines in a wide-row store
    (Cassandra/Bigtable) for most users; use pull from AuthorRecentPosts
    for celebrity / heavy-hitter authors.\
-   Media in object storage (S3/GCS) + CDN. Redis for hot caches and
    session/state.

------------------------------------------------------------------------

## 3) Data model & storage choices (mapping to scale)

### User

-   store: Relational or strongly consistent store (Spanner/Postgres)
-   fields:
    `user_id, username, name, bio, created_at, follower_count, ...`

### Post

-   store: NoSQL / wide row (Cassandra) or document store for post body;
    store immutable body + metadata
-   minimal row:
    `{post_id, author_id, created_at, content_ref, media_urls[], visibility, score_meta}`

### Followers / Following

-   store: wide-row store (Cassandra) or sharded RDBMS keyed by
    `user_id` → list of follower ids
-   reason: extremely high throughput and predictable access pattern
    (list fans)

### Timeline / Feed (materialized)

-   store: Cassandra wide-rows keyed by `user_id` containing ordered
    `(post_id, created_at, ranking_score)`
-   TTL / size cap (e.g., keep N most recent 10k entries to bound
    storage)
-   hot shards: for very active users, keep some entries in Redis

### Likes / Comments

-   store: separate tables. Comments as records
    `{comment_id, post_id, author_id, text, created_at}` sharded by
    `post_id`. Likes as small writes (or HLL if approximate). Maintain
    `likes_count` in Post (denormalized), updated asynchronously if
    strict real-time isn't required.

### Search

-   store: Elasticsearch, asynchronously indexed by an indexer consumer

### Media

-   S3/GCS + CDN; store URLs in Post records (signed URL for uploads).

------------------------------------------------------------------------

## 4) Eventing & pipeline (concrete)

-   **Kafka topics**: `posts`, `follows`, `likes`, `comments`,
    `media-uploads`
-   On `POST /posts`:
    1.  API writes post to Post store (durable).
    2.  Publish `PostCreated(post_id, author_id, created_at)` to Kafka.
    3.  Consumers:
        -   Feed Fanout Workers
        -   Search Indexer
        -   Notification service
-   Fanout workers are horizontally scalable consumer groups that write
    into per-user timeline store, batched and idempotent.

------------------------------------------------------------------------

## 5) Fan-out strategy (hybrid, with thresholds)

-   Maintain `follower_count` in User row.
-   Define `FANOUT_THRESHOLD ≈ 5k` (tunable).
-   On PostCreated:
    -   if `follower_count < threshold` → **Push**: fan out post_id to
        each follower's timeline via batched writes (worker pools).\
    -   else → **Pull**: mark post as `pullable` and write to
        `AuthorRecentPosts` (small table of recent posts per author).
        Optionally push notifications only. Followers' feeds will merge
        these pullable posts on read.
-   For medium-size authors near threshold, use hybrid: partial fanout
    (to top-K active followers) + pull for rest.
-   Rationale: avoids write amplification for celebrities while still
    keeping low-latency feed for most users.

------------------------------------------------------------------------

## 6) Feed read flow & ranking

-   `GET /feed?cursor=&limit=50`:
    1.  Read materialized timeline entries from Cassandra (fast).
    2.  For each followed heavy author, fetch recent posts from
        `AuthorRecentPosts` and merge.
    3.  Enrich top N posts (parallel fetch post bodies + media refs +
        like counts from cache).
    4.  Apply lightweight ranking (recency + social affinity +
        engagement signals); for more complex ranking call an online
        ranker service.
-   **Ranking**:
    -   Offline features computed in batch (user affinity, post quality,
        topical relevance).\
    -   Online ranker uses precomputed features + real-time signals
        (recent engagement) and returns final reorder for top K.
    -   Keep ranking deterministic and cache high-frequency decisions.

------------------------------------------------------------------------

## 7) Real-time & notifications

-   Use WebSocket/Push service for live notifications
    (likes/comments/mentions).
-   Not every feed refresh needs to be pushed --- only high-priority
    notifications are pushed.

------------------------------------------------------------------------

## 8) Consistency, idempotency & correctness

-   Writes to timeline: **idempotent keys** (user_id + post_id) to avoid
    duplicates on retries.
-   Use Kafka offsets or unique request ids to handle at-least-once
    processing safely.
-   Expose read-after-write consistency for the author (immediate
    visibility of their post in their own timeline) by reading directly
    from Post store + recent posts cache.

------------------------------------------------------------------------

## 9) Hot keys, backpressure, and batching

-   Detect hot timelines (very active users) and shard them across
    multiple timeline partitions or treat as pull-only.
-   Fanout workers use **batch writes** (e.g., 1000 follower writes per
    batch) and **rate limit** to protect downstream DBs.
-   If queues/backpressure appear (consumer lag rising), degrade
    gracefully: convert more authors to pull mode, drop low-priority
    tasks, return slightly stale feeds with a "refresh" button.

------------------------------------------------------------------------

## 10) Operational considerations & reliability

-   **Monitoring**: Kafka consumer lag, timeline write errors, p95 feed
    load latency, 5xx rates.\
-   **SLOs**: feed load p95 \< 200--500ms, availability 99.9% for feed
    API.\
-   **Backfill & migrations**: offline jobs to rebuild timelines when
    ranking logic changes.\
-   **Data retention & cost**: keep only recent N entries per timeline;
    archive older posts to cheap storage.\
-   **Security & moderation**: moderation queue on Kafka, automated
    detectors + human review.\
-   **Testing**: chaos experiments (producer or consumer outage), load
    tests with synthetic celebrity traffic.

------------------------------------------------------------------------

## 11) API & schema examples (concise)

-   `POST /posts` → body
    `{author_id, content, media_refs[], visibility}` → returns
    `post_id`\
-   `POST /posts/{id}/like` → idempotent with `client_like_id`\
-   `GET /feed?cursor=<cur>&limit=50` → returns list of enriched posts +
    next_cursor

**Post minimal row**

``` json
{ "post_id": "p1", "author_id": "u1", "created_at": 1670000000, "content_ref":"s3://...", "media_urls":[], "likes_count": 12, "comments_count": 3 }
```

------------------------------------------------------------------------

## 12) Example numbers to cite (showes interviewer you thought through capacity)

-   Suppose 1k posts/sec, avg followers = 200 → naive fanout = 200k
    writes/sec. Hybrid + batching reduces writes by \~95% when many
    posts are from heavy users.\
-   Choose `FANOUT_THRESHOLD = 5k`: tuned by write bandwidth and
    capacity of timeline writer cluster.\
-   Timeline row size: keep page size to 50--200 posts per request;
    store compact (post_id + timestamp + score).

------------------------------------------------------------------------

## 13) Tradeoffs & alternatives (brief)

-   **Graph DB for followers?** Good for graph queries, but at this
    scale wide-row store is cheaper and simpler for follower lists.\
-   **Materialize everything (pure push)?** Fast reads but huge write
    amplification and operational complexity for celebrities.\
-   **Pure pull?** Simpler, lower storage, higher read latency and
    compute cost at read time.

------------------------------------------------------------------------

## 14) Short checklist to add to your diagram / talk through in interview

-   Kafka topics + fanout workers (batched, idempotent).\
-   Per-user timeline store (Cassandra) & `AuthorRecentPosts` for heavy
    authors.\
-   Redis hot cache + CDN for media.\
-   Search indexer (Elasticsearch) and notification service
    (WebSockets).\
-   Monitoring: consumer lag + p95 latency dashboards.\
-   Backfill + migration jobs.

------------------------------------------------------------------------

## 15) How to present this in 3 minutes during an interview

1.  Start with scale & constraints.\
2.  State hybrid fanout approach and the `FANOUT_THRESHOLD`.\
3.  Draw data stores: Users→RDBMS, Followers→Cassandra, Posts→NoSQL,
    Timeline→Cassandra, Media→S3+CDN.\
4.  Explain the event pipeline (Kafka) and fanout worker behavior
    (batched, idempotent).\
5.  Call out hot-key handling, ranking pipeline, and operational
    safeguards (monitoring, backfill).\
6.  End with tradeoffs and one thing you'd iterate on (e.g., move to ML
    ranker with online feature store).
