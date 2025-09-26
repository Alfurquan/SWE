# Phase 1: Foundation & Fundamentals 📚

**Duration**: Week 1-2  
**Goal**: Master the core building blocks of system design

## 📋 Learning Objectives

By the end of this phase, you should be able to:
- Explain fundamental system design concepts
- Identify and describe core system components
- Apply basic scalability principles
- Understand trade-offs in system design decisions

## 🏗️ Topics Covered

### 1. System Design Basics (Days 1-2)

#### 1.1 Introduction to System Design
- [ ] What is System Design?
- [ ] Why System Design Matters in Interviews
- [ ] Approach to System Design Problems
- [ ] Communication Best Practices

#### 1.2 Scalability Fundamentals
- [ ] Vertical vs Horizontal Scaling
- [ ] Performance vs Scalability
- [ ] Latency vs Throughput
- [ ] Availability vs Consistency

#### 1.3 Reliability and Availability
- [ ] Fault Tolerance
- [ ] Redundancy
- [ ] Disaster Recovery
- [ ] SLA, SLO, SLI

### 2. Core Building Blocks (Days 3-8)

#### 2.1 Load Balancing ⚖️
- [ ] **Types of Load Balancers**
  - Layer 4 (Transport) vs Layer 7 (Application)
  - Hardware vs Software Load Balancers
- [ ] **Load Balancing Algorithms**
  - Round Robin
  - Weighted Round Robin
  - Least Connections
  - IP Hash
  - Consistent Hashing
- [ ] **Health Checks and Failover**
- [ ] **Session Persistence (Sticky Sessions)**
- [ ] **Global Server Load Balancing (GSLB)**

**Practice Exercise**: Design load balancing for a web application with 1M users

#### 2.2 Caching 🗄️
- [ ] **Caching Levels**
  - Browser Cache
  - CDN (Content Delivery Network)
  - Reverse Proxy Cache
  - Application Cache
  - Database Cache
- [ ] **Cache Strategies**
  - Cache-aside (Lazy Loading)
  - Write-through
  - Write-behind (Write-back)
  - Refresh-ahead
- [ ] **Cache Invalidation**
  - TTL (Time To Live)
  - Cache Eviction Policies (LRU, LFU, FIFO)
  - Cache Coherence
- [ ] **Distributed Caching**
  - Redis
  - Memcached
  - Consistent Hashing for Cache Distribution

**Practice Exercise**: Design caching strategy for an e-commerce platform

#### 2.3 Database Fundamentals (Days 5-6)
- [ ] **SQL vs NoSQL**
  - ACID Properties
  - CAP Theorem
  - BASE Properties
- [ ] **Database Types**
  - Relational (PostgreSQL, MySQL)
  - Document (MongoDB, CouchDB)
  - Key-Value (Redis, DynamoDB)
  - Column-Family (Cassandra, HBase)
  - Graph (Neo4j, Amazon Neptune)
- [ ] **Database Scaling**
  - Read Replicas
  - Master-Slave vs Master-Master
  - Database Federation
  - Functional Partitioning

#### 2.4 Data Partitioning/Sharding 🔄
- [ ] **Partitioning Strategies**
  - Horizontal Partitioning (Sharding)
  - Vertical Partitioning
  - Functional Partitioning
- [ ] **Sharding Techniques**
  - Range-based Sharding
  - Hash-based Sharding
  - Directory-based Sharding
  - Consistent Hashing
- [ ] **Challenges**
  - Rebalancing
  - Celebrity Problem (Hot Spots)
  - Cross-shard Queries
  - Shard Key Selection

**Practice Exercise**: Design sharding strategy for Twitter-like social media platform

#### 2.5 Rate Limiting 🚦
- [ ] **Rate Limiting Algorithms**
  - Token Bucket
  - Leaky Bucket
  - Fixed Window Counter
  - Sliding Window Log
  - Sliding Window Counter
- [ ] **Implementation Approaches**
  - Client-side vs Server-side
  - Distributed Rate Limiting
  - Rate Limiting in Microservices
- [ ] **Rate Limiting Strategies**
  - Per-user Rate Limiting
  - Per-IP Rate Limiting
  - API Rate Limiting
  - Geographic Rate Limiting

**Practice Exercise**: Implement rate limiting for API gateway

#### 2.6 Data Replication 📋
- [ ] **Replication Types**
  - Synchronous vs Asynchronous
  - Single-leader Replication
  - Multi-leader Replication
  - Leaderless Replication
- [ ] **Replication Strategies**
  - Master-Slave Replication
  - Master-Master Replication
  - Chain Replication
- [ ] **Consistency Models**
  - Strong Consistency
  - Eventual Consistency
  - Weak Consistency
- [ ] **Handling Replication Lag**

### 3. Fundamental Concepts (Days 9-10)

#### 3.1 Consistency Patterns
- [ ] Strong Consistency
- [ ] Weak Consistency  
- [ ] Eventual Consistency
- [ ] Causal Consistency

#### 3.2 Availability Patterns
- [ ] Active-Passive Failover
- [ ] Active-Active Failover
- [ ] Circuit Breaker Pattern

#### 3.3 Performance Metrics
- [ ] Response Time
- [ ] Throughput
- [ ] Availability (99.9%, 99.99%, 99.999%)
- [ ] Consistency

## 🎯 Week 1-2 Milestones

### End of Week 1
- [ ] Complete System Design Basics
- [ ] Master Load Balancing concepts
- [ ] Understand Caching strategies
- [ ] Practice 2 basic system design problems

### End of Week 2  
- [ ] Complete Database Fundamentals
- [ ] Master Partitioning/Sharding
- [ ] Understand Rate Limiting and Replication
- [ ] Practice 3 intermediate system design problems

## 📝 Practice Problems

### Basic Level
1. Design a URL Shortener (like bit.ly)
2. Design a Simple Chat Application
3. Design a Basic Social Media Feed

### Intermediate Level  
1. Design a Distributed Cache
2. Design a Rate Limiter
3. Design a Load Balancer

## 📚 Recommended Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 1-5)
- "System Design Interview" by Alex Xu (Chapters 1-4)

### Articles
- High Scalability Blog
- AWS Architecture Center
- Google Cloud Architecture Framework

### Videos
- System Design Interview questions on YouTube
- Distributed Systems courses (MIT 6.824)

## ✅ Self-Assessment Checklist

Before moving to Phase 2, ensure you can:
- [ ] Explain when and why to use each caching strategy
- [ ] Design a load balancing solution for different scenarios
- [ ] Choose appropriate partitioning strategy for given requirements
- [ ] Implement different rate limiting algorithms
- [ ] Explain trade-offs between consistency and availability
- [ ] Solve basic system design problems in 45 minutes

---

**Next**: [Phase 2: Intermediate Components](../02-intermediate/README.md)
