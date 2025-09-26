# Database Selection & Design Practice Problems

## 🎯 **Overview**
This document contains targeted problems to help solidify database concepts and selection skills. These problems focus specifically on database selection and design considerations rather than full system design.

---

## 🧠 **Problem Set 1: Database Selection (Beginner)**

### **Problem 1.1: E-commerce Product Catalog**
You're designing a product catalog for an e-commerce platform. Consider these requirements:
- Products have varying attributes (electronics have specs, clothing has sizes/colors)
- Need fast text search across product names and descriptions
- Need to filter by price, category, brand, ratings
- 10M+ products, high read traffic

**Questions:**
1. Which database type(s) would you choose for storing product data? Why?
2. How would you handle the text search requirement?
3. What indexing strategy would you use?

**Time:** 15-20 minutes

---

### **Problem 1.2: Social Media Activity Feed**
Design storage for a social media activity feed:
- Store user posts, likes, comments, shares
- Need to show "friends of friends" recommendations
- Need to find mutual connections between users
- High write volume (1M posts/day)

**Questions:**
1. What database type best handles the relationship queries?
2. How would you store the activity feed data?
3. What are the trade-offs of your choice?

**Time:** 15-20 minutes

---

### **Problem 1.3: User Session Management**
Design a session management system for a web application:
- 500K concurrent users
- Sessions expire after 30 minutes of inactivity
- Need to store user preferences and shopping cart data
- Sub-100ms response time for session validation
- Sessions should survive server restarts

**Questions:**
1. What database type is most appropriate?
2. How would you handle session expiration?
3. What are the persistence requirements?

**Time:** 15-20 minutes

---

## 🔧 **Problem Set 2: Design Considerations (Intermediate)**

### **Problem 2.1: Gaming Leaderboard System**
Design a database solution for a real-time gaming leaderboard:
- Track player scores across multiple games
- Need global and regional leaderboards
- Players can play multiple games simultaneously
- Need to show rank changes over time
- 100K concurrent players, scores update every few seconds

**Questions:**
1. Which database type handles high-frequency score updates best?
2. How would you design the schema/data model?
3. What eviction policy would you use and why?
4. How would you handle persistence requirements?

**Time:** 20-25 minutes

---

### **Problem 2.2: IoT Sensor Data Platform**
Design storage for an IoT sensor monitoring system:
- 50K sensors sending temperature, humidity, pressure every 30 seconds
- Need to detect anomalies and trends
- Historical data analysis for the past 2 years
- Real-time dashboards and alerting
- Data retention: Keep raw data for 90 days, aggregated data for 2 years

**Questions:**
1. What database type is most suitable? Why?
2. How would you design your partition key and clustering strategy?
3. How would you handle the data retention requirements?
4. What indexing considerations are important?

**Time:** 20-25 minutes

---

### **Problem 2.3: Document Management System**
Design storage for a legal document management system:
- Store PDF documents, contracts, legal briefs
- Need full-text search across document content
- Documents have metadata (client, date, case number, practice area)
- Need version control and audit trails
- Documents range from 100KB to 50MB
- Strict access control requirements

**Questions:**
1. How would you separate document storage from metadata?
2. What database types would you use for each concern?
3. How would you handle document versioning?
4. What are the security considerations?

**Time:** 20-25 minutes

---

## 🏗️ **Problem Set 3: Multi-Database Architecture (Advanced)**

### **Problem 3.1: Content Management System**
Design a database architecture for a content management system like WordPress:
- Store articles with rich text, images, videos
- Need full-text search across articles
- Track user interactions (views, likes, comments)
- Need to recommend related articles
- Support multiple content types (blog posts, pages, media)

**Questions:**
1. Identify at least 3 different database types you'd use
2. What data goes in each database and why?
3. How would you handle consistency between databases?
4. Design the data flow for a "related articles" feature

**Time:** 25-30 minutes

---

### **Problem 3.2: Ride-Sharing Platform Database Design**
Design the database architecture for a ride-sharing app:
- Track driver/rider locations in real-time
- Store trip history and receipts
- Handle driver matching within radius
- Store maps and route data
- Process payments and pricing
- Need fraud detection and analytics

**Questions:**
1. Map each requirement to appropriate database types
2. How would you handle real-time location updates?
3. What are the consistency requirements for different data types?
4. How would you design for global scaling?

**Time:** 25-30 minutes

---

### **Problem 3.3: Multi-Tenant SaaS Platform**
Design database architecture for a project management SaaS:
- Each tenant has custom fields and workflows
- Need to provide analytics dashboards
- Data volume varies: small tenants (GB), large tenants (TB)
- Need real-time collaboration features
- Strict data isolation between tenants

**Questions:**
1. How would you handle schema flexibility per tenant?
2. What database types for different features?
3. Design data isolation strategy
4. How would you handle tenants with vastly different scales?

**Time:** 25-30 minutes

---

## ⚡ **Problem Set 4: Performance & Scaling Scenarios**

### **Problem 4.1: Chat Application Message Storage**
You have a chat application with these characteristics:
- 10M active users
- Average 100 messages per user per day
- Messages contain text, images, files
- Need message history search
- Need to show online status
- Group chats with up to 1000 members

**Challenge:** Your current MongoDB setup is struggling with:
- Slow query performance for message history
- High memory usage
- Expensive complex queries for group message distribution

**Questions:**
1. Analyze what's wrong with using only document database
2. Propose a multi-database solution
3. How would you migrate without downtime?
4. Design data partitioning strategy

**Time:** 30 minutes

---

### **Problem 4.2: Financial Trading Platform**
Design storage for a financial trading platform:
- Real-time stock price updates (1M updates/second)
- Historical price data (5+ years)
- User portfolios and transactions
- Risk analysis and reporting
- Regulatory compliance (audit trails)
- Sub-millisecond latency for price queries

**Questions:**
1. What combination of databases would you use?
2. How would you handle the latency requirements?
3. Design the data flow from market data ingestion to user queries
4. How would you ensure data consistency for financial transactions?

**Time:** 30 minutes

---

### **Problem 4.3: Video Streaming Platform**
Design database architecture for a video streaming platform:
- Store video metadata and user profiles
- Handle 10M+ video uploads per day
- Track viewing analytics and recommendations
- Support live streaming with chat
- Global content delivery
- Different video qualities and formats

**Questions:**
1. How would you separate video storage from metadata?
2. What databases for real-time features vs analytics?
3. How would you handle global content distribution?
4. Design the recommendation system data flow

**Time:** 30 minutes

---

## 🔍 **Problem Set 5: Edge Cases & Trade-offs**

### **Problem 5.1: Global CDN Cache Strategy**
Design a caching strategy for a global CDN serving static content:
- 100+ edge locations worldwide
- Serving images, videos, CSS, JS files
- Content ranges from 1KB to 500MB
- Some content is region-specific
- Need to handle cache invalidation
- Users expect <100ms response times

**Questions:**
1. What type of storage at each edge location?
2. How would you handle large file chunking?
3. Design your eviction policy for optimal hit rates
4. How would you handle cache consistency across regions?

**Time:** 25-30 minutes

---

### **Problem 5.2: Real-time Analytics Dashboard**
Design storage for a real-time analytics dashboard:
- Ingesting 1M events per second
- Need to show metrics with 5-second latency
- Historical analysis for past 2 years
- Custom user-defined metrics and alerts
- Different event types with varying schemas
- Need both real-time and batch processing

**Questions:**
1. What databases for hot vs cold data?
2. How would you handle schema evolution?
3. Design the real-time processing pipeline
4. What trade-offs between latency and accuracy?

**Time:** 25-30 minutes

---

### **Problem 5.3: Healthcare Records System**
Design database architecture for a healthcare records system:
- Store patient records, medical images, lab results
- Strict HIPAA compliance requirements
- Need fast lookup by patient ID, doctor, date
- Support complex medical queries
- Images can be 100MB+ (MRI, CT scans)
- 99.99% availability requirement
- Audit trail for all access

**Questions:**
1. How would you handle different data types?
2. What are the security and compliance considerations?
3. How would you design for high availability?
4. What backup and disaster recovery strategy?

**Time:** 25-30 minutes

---

## 🎯 **Solution Framework**

For each problem, structure your answer using this framework:

### **1. Requirements Analysis**
- **Data Characteristics:** Volume, velocity, variety
- **Query Patterns:** Read/write ratios, query types
- **Consistency Requirements:** Strong vs eventual consistency
- **Scalability Needs:** Current and projected scale

### **2. Database Selection Justification**
- **Primary Choice:** Main database type and reasoning
- **Alternative Considerations:** Why other options were rejected
- **Hybrid Approaches:** When multiple databases are needed

### **3. Design Considerations**
- **Schema/Data Model:** How you'll structure the data
- **Indexing Strategy:** What to index and why
- **Partitioning/Sharding:** Distribution strategy
- **Consistency & Durability:** ACID requirements

### **4. Trade-offs & Limitations**
- **Optimizations:** What you're optimizing for
- **Sacrifices:** What you're giving up
- **Bottlenecks:** Potential performance issues
- **Cost Implications:** Storage and operational costs

### **5. Alternative Approaches**
- **Other Solutions:** What else could work
- **When to Reconsider:** Conditions for changing approach
- **Migration Path:** How to evolve the solution

---

## 📝 **Practice Tips**

### **Study Approach**
1. **Start Simple:** Begin with Problem Set 1
2. **Time Management:** Use suggested time limits
3. **Think Aloud:** Practice explaining your reasoning
4. **Real Examples:** Consider actual companies with similar challenges

### **Interview Preparation**
1. **Question Assumptions:** What if scale was 10x? Different regions?
2. **Consider Edge Cases:** What could go wrong?
3. **Discuss Trade-offs:** No solution is perfect
4. **Stay Practical:** Consider operational complexity

### **Self-Assessment**
- Can you clearly explain your database choice?
- Did you consider multiple alternatives?
- Are your design decisions well-reasoned?
- Did you identify potential issues and mitigations?

---

## 📚 **Reference Quick Guide**

### **Database Type Selection Cheat Sheet**

| Requirement | Best Database Type | Why |
|-------------|-------------------|-----|
| Complex relationships | Graph | Efficient traversals |
| High write throughput | Wide-column | Optimized for writes |
| Full-text search | Text search | Inverted indexes |
| Flexible schema | Document | Schema-less design |
| Ultra-low latency | In-memory | RAM-based storage |
| Simple key lookups | Key-value | Minimal overhead |
| Time-based data | Time-series | Optimized for timestamps |
| Geospatial queries | Spatial | Geographic operations |
| Large files | Blob store | Optimized for binary data |
| Strong consistency | Relational | ACID guarantees |

### **Common Interview Traps**
- Don't default to one database for everything
- Consider data access patterns, not just storage
- Think about operational complexity
- Remember consistency vs availability trade-offs
- Consider cost implications of your choices

---

*Happy practicing! These problems will help you build the database selection intuition crucial for L5 system design interviews.*