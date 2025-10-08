# 📖 Scaling Reads Pattern - Cheatsheet

## 🎯 The Core Problem

Read traffic often grows 10:1 to 100:1 compared to writes. Your database gets crushed under massive read load - Instagram feeds, YouTube recommendations, Twitter timelines all need to serve millions of reads per second.

## 🔧 The Solution Progression

### Database Optimization (Start Here!)

#### 🟢 Indexing (Foundation)

Add indexes on columns you query, join, or sort by
Turns O(n) table scans into O(log n) lookups
Use when: Queries getting slower as data grows
L5 Tip: Mention indexes when outlining your schema

#### 🟡 Denormalization (Trade Storage for Speed)

```sql
-- Instead of expensive joins
SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id;

-- Store redundant data for fast single-table queries  
SELECT user_name, post_title FROM post_summary WHERE post_id = 123;
```

Use when: Joins are slowing queries, read patterns are stable
Tradeoff: Faster reads, more complex writes

#### 🟠 Materialized Views (Pre-compute Aggregations)

Calculate expensive operations once, store results
Example: Average ratings, popular products, trending topics
Use when: Complex calculations accessed frequently

### Horizontal Scaling

#### 🔴 Read Replicas

- Primary handles writes, replicas handle reads
- Distributes read load across multiple servers
- Challenge: Replication lag (users might not see own writes immediately)
- Use when: 50K+ reads/second, single DB overwhelmed

#### 🟣 Database Sharding

- Split data across multiple databases
- Functional: Users DB + Products DB
- Geographic: US DB + EU DB
- Use when: Dataset too large even with good indexes
- Warning: Adds significant complexity

### External Caching Layers

#### 🔵 Application-Level Caching (Redis/Memcached)

```text
App → Check Cache → Hit: Return data (sub-ms)
                 → Miss: Query DB + Cache result
```

- Use when: Repeated queries for same data
- TTL Strategy: Based on staleness requirements (5min profiles, 30sec search)

#### 🟨 CDN/Edge Caching

- Cache data globally at edge locations
- Tokyo user gets data from Tokyo server (10ms vs 200ms)
- Use when: Multi-user data (product pages, public posts)
- Don't cache: User-specific data (private messages, account settings)

### 🚀 Quick Decision Tree

- Slow queries as data grows? → Add indexes
- Expensive joins killing performance? → Denormalize frequently accessed data
- 50K+ reads/second? → Add read replicas or caching
- Global users? → CDN caching
- Hot keys (celebrity problem)? → Cache fanout + request coalescing

### 💡 L5 Interview Tips

- Start Simple: Always mention indexing and query optimization first
- Identify Read Patterns: "This user profile endpoint will get billions of reads"
- Match Solution to Problem: Don't cache user-specific data, do cache popular content
- Show Trade-offs: "Caching gives us speed but introduces staleness"

### 🎪 Common Interview Scenarios

- 📸 Instagram Feed: Cache recent posts, user profiles; read replicas for browsing
- 🎟️ Ticketmaster: Cache event details aggressively, but NOT seat availability
- 📺 YouTube: Cache video metadata, thumbnails; CDN for global access
- 🔗 URL Shortener: Perfect caching scenario - cache short→long URL mapping forever

### 🔥 Deep Dive Prep

- Cache Stampede: Use probabilistic early refresh or background refresh
- Hot Keys (Celebrity Problem): Cache fanout across multiple keys + request coalescing
- Cache Invalidation: TTL + versioned keys + tagged invalidation
- Replication Lag: Read-after-write consistency patterns

### 🎯 The L5 Approach

- Identify read bottlenecks early in your design
- Start with database optimization (indexes, denormalization)
- Add caching strategically (application cache → CDN)
- Consider read replicas when DB is overwhelmed
- Address consistency requirements (how stale can data be?)

### ⚡ Cache Strategy Framework

```text
Data Type → Caching Strategy
Public content (product pages) → Aggressive CDN caching (1 hour TTL)
User profiles → Application cache (5 min TTL)
Search results → Short TTL (30 seconds)
Real-time data (stock prices) → No caching or very short TTL
Private data → Don't cache at CDN level
```
