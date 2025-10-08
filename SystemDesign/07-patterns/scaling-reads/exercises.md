# Practice Exercises

This section contains exercises to test your understanding of scaling read patterns. Try to answer each question before checking the provided solution.

## Scenario 1: Instagram-like Social Media Feed

You're designing the feed system for a social media app like Instagram. Users follow other users and see their posts in a chronological feed. Popular users have millions of followers. When a celebrity posts, millions of people might view their feed within minutes. Each feed load requires fetching posts, user info, like counts, and comments preview.

Your task: How do you handle the massive read load for feeds? What's your scaling strategy?

### Solution

1. **Database Optimization**:
   - **Indexing**: Ensure indexes on user_id, post_id, and timestamp columns to speed up feed queries.
   - **Denormalization**: Create a denormalized `feed` table that stores pre-joined data (post content, user info, like counts) to avoid expensive joins during feed retrieval.
   - **Materialized Views**: Use materialized views to precompute popular posts or trending content for quick access.

2. **Horizontal Scaling**:

    - **Read Replicas**: Set up read replicas to distribute read traffic. The primary database handles writes, while replicas serve read requests.
    - **Database Sharding**: Shard the database by user_id to distribute data across multiple servers, ensuring that no single server becomes a bottleneck.
  
3. **External Caching Layers**:

    - **Application-Level Caching**: Use Redis or Memcached to cache frequently accessed feeds. When a user requests their feed, first check the cache. If it's a miss, fetch from the database and store the result in the cache for future requests.
    - **CDN Caching**: For static assets like images and videos, use a Content Delivery Network (CDN) to offload traffic from your servers.
    - **Edge Caching**: Implement edge caching for dynamic content that doesn't change frequently, such as user profiles or post metadata.

4. **Additional Strategies**:
    - **Asynchronous Processing**: Use background jobs to precompute and update feeds for users, especially for high-profile users. This way, when a user requests their feed, it's already prepared.

### Enhanced Solution

**Feed Architecture**: Hybrid Push/Pull Model

- Push: Pre-generate feeds for active users (< 1000 following)
- Pull: On-demand generation for inactive users
- Background workers update feeds when new posts arrive

**Database Optimization**:

- Indexes on (user_id, timestamp) for timeline queries
- Denormalized feed table with user info, post content
- Partition by user_id ranges for better performance

**Caching Strategy**:

- Personal feeds: Redis cache with 10-minute TTL
- Celebrity posts: Cache fanout across multiple keys
- Popular content: Edge caching with 5-minute TTL

**Celebrity Problem Solution**:

- Detect high-follower accounts (> 1M followers)
- Use separate queues for celebrity post distribution
- Request coalescing for identical post requests

---

## Scenario 2: E-commerce Product Search

You're building the search functionality for an Amazon-like e-commerce platform. Users search for products using keywords, filters (price, brand, category), and sorting options. Popular search terms like "iPhone" or "Christmas gifts" get searched thousands of times per minute. Each search needs to return product details, prices, ratings, and availability.

Your task: How do you scale search to handle millions of queries while keeping results fast and relevant?

### Solution

**Database Optimization**:

- Indexes on (prices, brand, category) for faster retrieval
- Denormalized data for category to fetch all details instead of joins which slow down queries.
- Materialized views to pre compute ratings and popular content, instead of computing them on the go.

**Search engines**:

- Databases can become slow for search related queries.
- To handle search related queries, we can use a search engine like elastic search to speed up query results.
- MySQL for transactional data (orders, inventory)
- Kafka for real-time sync between DB and ElasticSearch

**Caching Strategy**:

- Cache search results for popular items like "iphone" etc to avoid load on main database and serve users faster.
- TTL based on data freshness: 30 seconds for inventory, 1 hour for product details
- Trending items: Cache fan out across multiple keys
- Popular product: Edge caching for popular product items

### Enhanced solution

**Search Architecture**: Elasticsearch + MySQL Hybrid

**Search Engine Layer**:

- Elasticsearch for full-text search with relevance scoring
- Auto-complete index for type-ahead suggestions
- Faceted search indexes for filters (brand, category, price ranges)
- Real-time sync via Kafka from MySQL to Elasticsearch

**Caching Strategy**:

- Search results: Cache with composite keys including filters
  - Key: "search:iphone:brand=apple:price=500-1000:sort=rating"
  - TTL: 5 minutes (balance freshness vs performance)
- Auto-complete: Aggressive caching (1 hour TTL)
- Product details: CDN caching for individual product pages

**Database Optimization**:

- MySQL: Transactional data (orders, inventory, pricing)
- Read replicas for product catalog queries
- Indexes on filterable columns in MySQL as backup

**Inventory Challenge**:

- Cache search results but fetch real-time inventory for displayed products
- Separate API call for availability after showing cached results

---

## 📰 Scenario 3: News Website During Breaking News

You're designing a news website like CNN or BBC. During major breaking news events (elections, disasters, sports finals), millions of users simultaneously try to read the same articles. Your homepage gets refreshed constantly, and popular articles can receive 100,000+ page views per minute.

Your task: How do you handle traffic spikes when everyone wants to read the same content?

### Solution

**CDN/Edge Layer** (Your cache fanout + global distribution):

- Cache articles at edge locations worldwide
- Cache fanout: Store popular articles across multiple edge keys
- TTL: 2-5 minutes for breaking news, 1 hour for older content

**Application Cache** (Your Redis layer):

- Cache article metadata and homepage content
- Homepage: 30-second TTL (constantly refreshed)
- Article content: 5-minute TTL

**Database Optimization**:

- Read replicas for non-cached requests
- Indexes on (publish_time, category, popularity)

---

## 📺 Scenario 4: Video Streaming Platform Recommendations

You're building the recommendation engine for a YouTube-like platform. Each user's homepage shows personalized video recommendations based on their watch history, subscriptions, and trending content. The system needs to serve billions of recommendation requests daily while keeping suggestions fresh and relevant.

Your task: How do you scale personalized recommendations while maintaining good performance?

## Solution

**Application Cache** (Your Redis layer):

- Cache personalized recommendations per user
- Key structure: "recommendations:user_id:timestamp"
- Homepage: 1 hour TTL is fine as the data does not change that often.
- Trending content: We can cache trending content as well for faster reads, with a TTL of 1 day for daily trending contents.
- Watch history: Cache user watch history with a TTL of 1 week to provide better recommendations.

**Database Optimization**:

- Read replicas for non-cached requests
- Indexes on columns used in recommendation queries (user_id, video_id, watch_time)
- Denormalization of user preferences and video metadata for faster access

## Enhanced Solution

**Hybrid Architecture**: Pre-computation + Caching

**Background Processing**:

- ML pipeline pre-computes recommendations every 2-4 hours
- Store results per user: "recommendations:user_123"
- Immediate serving from cache (no real-time ML)

**Caching Strategy**:

- User recommendations: 4-hour TTL (matches ML pipeline)
- Trending content: 6-hour TTL (shared across users)
- User features/embeddings: 1-day TTL (for real-time adjustments)

**Database Optimization**:

- Read replicas for user behavior data
- Separate ML feature store for fast model serving
- Indexes on (user_id, timestamp) for behavior tracking

---