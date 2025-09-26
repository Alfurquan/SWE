# Mock Interview Questions 🎯

A comprehensive collection of system design interview questions organized by difficulty and company patterns.

## 📋 How to Use This Section

1. **Time yourself** - Stick to 45-60 minute limits
2. **Practice out loud** - Simulate real interview conditions
3. **Draw diagrams** - Use whiteboard or digital tools
4. **Follow the framework** - Requirements → Design → Scale → Optimize
5. **Record yourself** - Review communication and approach

## 🟢 Beginner Level (Weeks 1-2)

### Question 1: Design a URL Shortener (Bit.ly)

**Time Limit**: 45 minutes

**Key Requirements to Explore**:

- URL shortening and expansion
- Custom aliases (optional)
- Analytics (optional)
- 100:1 read to write ratio
- 1B URLs created per month

**Expected Discussion Points**:

- Database choice (SQL vs NoSQL)
- URL encoding strategies (Base62)
- Caching for popular URLs
- Rate limiting
- Basic load balancing

**Sample Solution Outline**:

1. **API Design**: POST /shorten, GET /{shortUrl}
2. **Database**: URL mapping table
3. **Components**: Web servers, Database, Cache
4. **Algorithm**: Base62 encoding vs Hash + collision handling

### Question 2: Design a Simple Chat Application

**Time Limit**: 45 minutes

**Key Requirements to Explore**:

- 1-on-1 messaging
- Message history
- Online status
- 10M active users
- Real-time delivery

**Expected Discussion Points**:

- WebSocket vs HTTP polling
- Message storage strategy
- Online presence management
- Basic notification system

### Question 3: Design a Pastebin Service

**Time Limit**: 45 minutes

**Key Requirements to Explore**:

- Create and share text snippets
- Expiration time options
- Syntax highlighting (optional)
- 1M pastes per day

**Expected Discussion Points**:

- Storage optimization
- CDN for static content
- Database cleanup strategies
- Simple analytics

## 🟡 Intermediate Level (Weeks 3-4)

### Question 4: Design a Notification System

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Push notifications, SMS, Email
- 100M users
- Priority levels
- Delivery rate limiting
- Analytics and tracking

**Expected Discussion Points**:

- Message queue architecture
- Multiple delivery channels
- Rate limiting per user/channel
- Retry and fallback strategies
- Template management

### Question 5: Design Twitter

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Tweet creation and viewing
- User timeline and home timeline
- Follow/unfollow functionality
- 200M daily active users
- 100M tweets per day

**Expected Discussion Points**:

- Fan-out strategies (push vs pull vs hybrid)
- Timeline generation algorithms
- Celebrity user problem
- Media handling
- Trending topics

**Key Components to Design**:

1. User Service
2. Tweet Service  
3. Timeline Service
4. Media Service
5. Notification Service

### Question 6: Design a Web Crawler

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Crawl 1B web pages
- Avoid duplicate content
- Respect robots.txt
- Politeness policy
- Content parsing and storage

**Expected Discussion Points**:

- Distributed crawling
- URL frontier management
- Duplicate detection
- Rate limiting per domain
- Content storage and indexing

## 🔴 Advanced Level (Weeks 5-6)

### Question 7: Design YouTube

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Video upload and streaming
- 2B users, 1B hours watched daily
- Multiple video qualities
- Global content delivery
- Recommendation system

**Expected Discussion Points**:

- Video processing pipeline
- CDN strategy for global delivery
- Metadata storage and search
- Recommendation algorithms
- Analytics and monetization

**Deep Dive Areas**:

- Video encoding and transcoding
- Adaptive bitrate streaming
- Global storage distribution
- Comment and engagement systems

### Question 8: Design WhatsApp

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Real-time messaging
- Group chats (up to 256 users)
- Media sharing
- 2B users globally
- End-to-end encryption

**Expected Discussion Points**:

- Real-time communication protocols
- Message delivery guarantees
- Group message distribution
- Media storage and delivery
- Security and encryption

### Question 9: Design Uber

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Rider-driver matching
- Real-time location tracking
- Trip management
- Pricing and payments
- 100M riders, 5M drivers

**Expected Discussion Points**:

- Geospatial indexing and queries
- Real-time location updates
- Matching algorithms
- Payment processing
- Dynamic pricing

## 🔥 Expert Level (Weeks 7-8)

### Question 10: Design a Distributed Search Engine

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Index 100B web pages
- Handle 100K queries per second
- Sub-second query response
- Relevance ranking
- Real-time index updates

**Expected Discussion Points**:

- Distributed crawling and indexing
- Inverted index design
- Query processing and ranking
- Index sharding and replication
- Real-time vs batch updates

### Question 11: Design Netflix

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Video streaming to 200M users
- Content recommendation
- Global content delivery
- Multiple device support
- Offline viewing capability

**Expected Discussion Points**:

- Content delivery network design
- Recommendation algorithms
- User behavior analytics
- Regional content licensing
- Adaptive streaming protocols

### Question 12: Design a Global Payment System

**Time Limit**: 60 minutes

**Key Requirements to Explore**:

- Handle millions of transactions daily
- Multi-currency support
- Fraud detection
- Regulatory compliance
- 99.99% availability

**Expected Discussion Points**:

- Transaction processing pipeline
- Fraud detection algorithms
- Compliance and audit trails
- Multi-region deployment
- Disaster recovery

## 🏢 Company-Specific Questions

### Microsoft Interview Style

**Question 13: Design Azure Storage**

- Focus on enterprise features
- Compliance and security
- Integration with other services
- Multi-tenant architecture

**Question 14: Design Microsoft Teams**

- Enterprise collaboration
- Integration with Office 365
- Security and compliance
- Scalability for large organizations

### Google Interview Style

**Question 15: Design Google Drive**

- File synchronization
- Collaborative editing
- Version control
- Global scale storage

**Question 16: Design Google Maps**

- Real-time traffic data
- Route optimization
- Location services
- Global map data storage

### Amazon Interview Style

**Question 17: Design Amazon Prime Video**

- Content delivery optimization
- Recommendation engine
- Digital rights management
- Global content distribution

**Question 18: Design AWS Lambda**

- Serverless computing platform
- Auto-scaling mechanisms
- Cold start optimization
- Event-driven architecture

## 📊 Interview Evaluation Criteria

### Technical Skills (40%)

- [ ] System design knowledge
- [ ] Scalability understanding
- [ ] Trade-off analysis
- [ ] Technology choice justification

### Problem-Solving (30%)

- [ ] Requirements clarification
- [ ] Structured approach
- [ ] Handling ambiguity
- [ ] Iterative improvement

### Communication (20%)

- [ ] Clear explanation
- [ ] Diagram clarity
- [ ] Stakeholder consideration
- [ ] Question asking

### Experience & Judgment (10%)

- [ ] Real-world awareness
- [ ] Operational considerations
- [ ] Security awareness
- [ ] Cost consciousness

## 🎯 Practice Schedule

### Week 1-2: Foundation

- **Day 1-2**: URL Shortener (repeat 3 times)
- **Day 3-4**: Chat Application (repeat 3 times)
- **Day 5-6**: Pastebin (repeat 2 times)
- **Day 7**: Review and self-assessment

### Week 3-4: Intermediate

- **Day 1-2**: Notification System
- **Day 3-4**: Twitter Design
- **Day 5-6**: Web Crawler
- **Day 7**: Mock interview with peer

### Week 5-6: Advanced

- **Day 1-2**: YouTube Design
- **Day 3-4**: WhatsApp Design
- **Day 5-6**: Uber Design
- **Day 7**: Professional mock interview

### Week 7-8: Expert + Company-Specific

- **Day 1-2**: Search Engine Design
- **Day 3-4**: Netflix Design
- **Day 5-6**: Company-specific questions
- **Day 7**: Final mock interviews

## 💡 Pro Tips for Mock Interviews

### Before the Interview

- [ ] Set up proper environment (whiteboard/screen sharing)
- [ ] Review the framework one more time
- [ ] Practice drawing clean diagrams
- [ ] Prepare clarifying questions

### During the Interview

- [ ] Think out loud
- [ ] Start simple, then add complexity
- [ ] Ask for feedback and hints
- [ ] Stay calm under pressure
- [ ] Manage time effectively

### After the Interview

- [ ] Request detailed feedback
- [ ] Identify improvement areas
- [ ] Practice weak topics
- [ ] Schedule follow-up sessions

## 📝 Self-Assessment Template

After each mock interview, rate yourself (1-5) on:

**Technical Knowledge**

- [ ] Understood requirements correctly
- [ ] Applied appropriate patterns
- [ ] Made reasonable trade-offs
- [ ] Handled scaling considerations

**Communication**

- [ ] Explained thoughts clearly
- [ ] Drew helpful diagrams
- [ ] Asked good questions
- [ ] Managed time well

**Areas for Improvement**

- What went well?
- What could be improved?
- Which topics need more study?
- What will you focus on next?

---

**Previous**: [Resources & References](../resources/README.md)  
**Back to**: [Main Roadmap](../README.md)
