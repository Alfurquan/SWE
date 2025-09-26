# System Design Topics: Grouped by Category with Company Blog Mapping

## 1. Database & Storage Systems

### Core Topics:
- Database types
- ACID properties
- SQL vs NoSQL
- Object storage
- Query optimization
- Change Data Capture (CDC)
- Bloom filters
- Indexing
- Sharding
- Vertical partitioning
- Sharding vs partitioning
- Replication
- Denormalization
- Data compression
- Data structures used in distributed databases
- How databases guarantee durability

### Company Blog Examples:
- **Netflix**: [How Netflix uses Cassandra for global streaming](https://netflixtechblog.com/tagged/cassandra)
- **Uber**: [Schemaless: Uber's distributed datastore](https://eng.uber.com/schemaless-part-one/)
- **Airbnb**: [Avoiding double payments in a distributed payments system](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)
- **Amazon**: [Amazon DynamoDB deep dive](https://aws.amazon.com/blogs/database/amazon-dynamodb-deep-dive-advanced-design-patterns/)
- **Facebook/Meta**: [MyRocks: LSM-Tree database storage engine](https://engineering.fb.com/2016/08/31/core-data/myrocks-a-space-and-write-optimized-mysql-database/)
- **Pinterest**: [Sharding Pinterest: How we scaled our MySQL fleet](https://medium.com/pinterest-engineering/sharding-pinterest-how-we-scaled-our-mysql-fleet-3f341e96ca6f)
- **Dropbox**: [How Dropbox stores billions of files](https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform)

---

## 2. Caching & Content Delivery

### Core Topics:
- What is caching
- Read-through vs write-through cache
- Caching strategies
- Cache eviction policies
- Distributed caching
- Content Delivery Networks (CDN)
- Redis use cases

### Company Blog Examples:
- **Netflix**: [Application data caching using SSDs](https://netflixtechblog.com/application-data-caching-using-ssds-5bf25df851ef)
- **Twitter**: [How Twitter uses Redis](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2014/redis-at-twitter)
- **Instagram**: [Caching at Instagram](https://instagram-engineering.com/tagged/cache)
- **Slack**: [Scaling Slack's job queue](https://slack.engineering/scaling-slacks-job-queue/)
- **LinkedIn**: [Couchbase at LinkedIn](https://engineering.linkedin.com/blog/2016/03/making-it-easier-to-monitor-couchbase-at-linkedin)
- **Spotify**: [How Spotify handles millions of playlists](https://engineering.atspotify.com/2022/03/how-spotify-handles-millions-of-playlists/)

---

## 3. Networking & Communication

### Core Topics:
- Load balancers
- Load balancing algorithms
- Proxy vs reverse proxy
- DNS
- HTTP/HTTPS
- TCP vs UDP
- Checksums
- What is an API
- Data formats
- API architectural styles
- REST API design
- WebSockets
- WebHooks
- WebRTC
- API gateways
- Rate limiting
- Idempotency

### Company Blog Examples:
- **Cloudflare**: [Load balancing without load balancers](https://blog.cloudflare.com/load-balancing-without-load-balancers/)
- **GitHub**: [How we built our API](https://github.blog/2016-09-07-introducing-the-graphql-api/)
- **Stripe**: [API design best practices](https://stripe.com/blog/payment-api-design)
- **Discord**: [How Discord handles millions of concurrent voice users](https://blog.discord.com/how-discord-handles-two-and-half-million-concurrent-voice-users-using-webrtc-ce01c3187429)
- **Zoom**: [Building a scalable video platform](https://blog.zoom.us/building-a-scalable-video-platform/)
- **Shopify**: [Rate limiting at Shopify](https://shopify.engineering/building-resilient-graphql-apis-rate-limiting-and-query-complexity-analysis)

---

## 4. Message Queues & Event Processing

### Core Topics:
- Publish/Subscribe (PUB/SUB)
- Message queues
- Kafka use cases
- Batch vs stream processing
- ETL pipelines
- MapReduce

### Company Blog Examples:
- **Kafka/Confluent**: [Building event streaming applications](https://www.confluent.io/blog/event-streaming-platform-1/)
- **LinkedIn**: [How LinkedIn uses Kafka](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
- **Uber**: [Building reliable reprocessing and dead letter queues](https://eng.uber.com/reliable-reprocessing/)
- **Netflix**: [Kafka inside Keystone Pipeline](https://netflixtechblog.com/kafka-inside-keystone-pipeline-dd5aeabaf6bb)
- **Airbnb**: [Scaling Kafka to support PayPal's data growth](https://medium.com/paypal-tech/kafka-consumer-lag-monitoring-at-paypal-4c6d88c29d04)
- **Slack**: [Scaling Slack's job queue](https://slack.engineering/scaling-slacks-job-queue/)

---

## 5. System Architecture & Design Patterns

### Core Topics:
- Vertical vs horizontal scaling
- Concurrency vs parallelism
- Long polling vs sockets
- Stateful vs stateless architecture
- Strong vs eventual consistency
- Push vs pull architecture
- Monolith vs microservices
- Synchronous vs asynchronous communications
- REST vs GraphQL
- Client-server architecture
- Microservices
- Serverless
- Event-driven architecture
- Peer-to-peer (P2P)

### Company Blog Examples:
- **Netflix**: [Microservices at Netflix](https://netflixtechblog.com/tagged/microservices)
- **Uber**: [Microservice architecture at Uber](https://eng.uber.com/microservice-architecture/)
- **Amazon**: [Serverless architectures with AWS Lambda](https://aws.amazon.com/lambda/resources/)
- **Spotify**: [Event delivery at scale](https://engineering.atspotify.com/2016/02/discovering-millions-of-datasets-at-spotify/)
- **Airbnb**: [Avoiding microservice megadisasters](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)

---

## 6. Distributed Systems & Consensus

### Core Topics:
- Heartbeats
- Consensus algorithms
- Leader election
- Distributed transactions
- Gossip protocol
- Two-phase commit
- Vector clocks
- Handling failures in distributed systems
- Service discovery
- Sidecar patterns
- Circuit breaker pattern
- SAGA pattern
- Service mesh

### Company Blog Examples:
- **Google**: [The Chubby lock service for loosely-coupled distributed systems](https://research.google/pubs/pub27897/)
- **Consul/HashiCorp**: [Service discovery with Consul](https://www.consul.io/use-cases/service-discovery-and-health-checking)
- **Netflix**: [Hystrix: Circuit breaker pattern](https://netflixtechblog.com/hystrix-62ee8aa4c45e)
- **Uber**: [Introducing Cadence](https://eng.uber.com/cadence/)
- **Lyft**: [Service mesh at Lyft](https://eng.lyft.com/announcing-envoy-c-l7-proxy-and-communication-bus-92520b6c8191)
- **Airbnb**: [Avoiding distributed system disasters](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)

---

## 7. Data Processing & Analytics

### Core Topics:
- Batch vs stream processing
- ETL pipelines
- MapReduce
- Data lakes
- Data warehousing
- Quad trees (for geospatial data)

### Company Blog Examples:
- **Netflix**: [Data pipeline evolution at Netflix](https://netflixtechblog.com/evolution-of-the-netflix-data-pipeline-da246ca36905)
- **Uber**: [Real-time data infrastructure at Uber](https://eng.uber.com/real-time-data-infrastructure-at-uber/)
- **Airbnb**: [Data quality at Airbnb](https://medium.com/airbnb-engineering/data-quality-at-airbnb-e582465f3ef7)
- **LinkedIn**: [Data infrastructure at LinkedIn](https://engineering.linkedin.com/blog/2016/02/the-evolution-of-schema-at-linkedin)
- **Spotify**: [Event delivery at Spotify](https://engineering.atspotify.com/2016/02/discovering-millions-of-datasets-at-spotify/)
- **Pinterest**: [Building Pinterest's A/B testing platform](https://medium.com/pinterest-engineering/building-pinterests-a-b-testing-platform-ab4934ace9f4)

---

## 8. Security & Authentication

### Core Topics:
- Authentication & Authorization
- OAuth/OAuth2
- JWT (JSON Web Tokens)
- SSL/TLS
- RBAC (Role-Based Access Control)

### Company Blog Examples:
- **Auth0**: [OAuth 2.0 and OpenID Connect best practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-oauth-2-security-best-practices/)
- **Okta**: [Building secure APIs](https://developer.okta.com/blog/2018/10/31/jwts-with-java)
- **GitHub**: [Token authentication requirements](https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/)
- **Slack**: [How Slack built shared channels](https://slack.engineering/how-slack-built-shared-channels/)
- **Dropbox**: [Security practices at Dropbox](https://dropbox.tech/security)
- **Netflix**: [Security at Netflix](https://netflixtechblog.com/tagged/security)

---

## Additional Resources by Company

### Netflix Tech Blog
- Focus: Microservices, streaming, caching, chaos engineering
- URL: https://netflixtechblog.com/

### Uber Engineering
- Focus: Real-time systems, microservices, distributed systems
- URL: https://eng.uber.com/

### Airbnb Engineering
- Focus: Data systems, payments, search, machine learning
- URL: https://medium.com/airbnb-engineering

### High Scalability
- Focus: Architecture case studies from various companies
- URL: http://highscalability.com/

### AWS Architecture Center
- Focus: Cloud architecture patterns and best practices
- URL: https://aws.amazon.com/architecture/

### Google Cloud Architecture Center
- Focus: Distributed systems, cloud patterns
- URL: https://cloud.google.com/architecture

---

## Study Approach Recommendations

1. **Start with Fundamentals**: Begin with database and caching concepts
2. **Progress to Architecture**: Move to system design patterns and microservices
3. **Deep Dive into Distributed Systems**: Study consensus and failure handling
4. **Practice with Real Examples**: Read company blogs for practical implementations
5. **Hands-on Implementation**: Try building small versions of these systems

## Interview Preparation Tips

- For each topic, understand both the theory and real-world applications
- Be able to explain trade-offs and when to use each approach
- Study how different companies solved similar problems
- Practice drawing system diagrams for each concept
- Understand failure scenarios and how systems recover
