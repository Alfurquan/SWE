# Comprehensive System Design Practice Questions

---

## Question 1: Video Streaming Platform
**Scenario:** Design a video streaming platform like YouTube that allows users to upload videos, view content, and interact with videos (likes, comments, subscriptions).

- Which databases would you use for different components of the system?  
- How would you handle video metadata vs. actual video content?  
- How would you implement search functionality for videos?  

---

## Question 2: Ride-Sharing Service
**Scenario:** Design a ride-sharing service that matches riders with nearby drivers in real-time.

- What database would you choose to store and query location data efficiently?  
- How would you handle ride history and payment transactions?  
- What caching strategy would you implement for real-time driver locations?  

---

## Question 3: E-commerce Platform During Flash Sale
**Scenario:** Design an e-commerce platform that can handle a flash sale with 100,000 users trying to purchase a limited stock item simultaneously.

- Which database would best handle inventory updates and prevent overselling?  
- How would you ensure the system remains available under heavy load?  
- What database would you use for user session management during the sale?  

---

## Question 4: Social Network Feed
**Scenario:** Design a social media feed system that shows personalized content to users based on their connections and interests.

- What database would you use to store user connections and relationships?  
- How would you implement the feed generation algorithm?  
- How would you balance between real-time updates and system performance?  

---

## Question 5: Real-time Chat System
**Scenario:** Design a real-time chat application like Slack or WhatsApp supporting one-on-one and group messaging.

- How would you ensure message delivery with offline recipients?
- What database architecture supports efficient message history retrieval?
- How would you implement real-time typing indicators and read receipts?
- How would you scale to support millions of concurrent users?

---

## Question 6: Distributed File Storage Service
**Scenario:** Design a cloud file storage service like Dropbox or Google Drive.

- What database would you use to store file metadata vs. actual file content?  
- How would you implement file sharing and permissions?  
- How would you handle synchronization across multiple devices?
- How would you approach file versioning and conflict resolution?

---

## Question 7: Ticketmaster Event Booking System
**Scenario:** Design a ticket reservation system like Ticketmaster that can handle high-demand events where thousands of users try to purchase tickets simultaneously.

- How would you prevent overselling of limited seats?
- What database would you choose for transaction processing and seat inventory?
- How would you handle the surge of traffic when tickets for popular events go on sale?
- What strategies would you implement to prevent ticket scalping and bots?

---

## Question 8: Online Auction System
**Scenario:** Design an auction platform like eBay that handles concurrent bidding from thousands of users.

- How would you ensure bid consistency and prevent race conditions?
- What database would you use to track auctions, bids, and user activities?
- How would you implement real-time price updates to all viewers?
- What mechanisms would you use to prevent auction sniping?

---

## Question 9: Video Conferencing System
**Scenario:** Design a video conferencing system like Zoom supporting many participants.

- How would you architect the media streaming infrastructure?
- What strategies would you employ for bandwidth optimization?
- How would you implement features like screen sharing and recording?
- How would you ensure security and privacy in the system?

---

## Question 10: IoT Monitoring System
**Scenario:** Design a system that collects and analyzes data from millions of IoT devices sending temperature readings every minute.

- What database would be most appropriate for storing this time-series data?  
- How would you implement anomaly detection on the collected data?  
- How would you design the system to handle device failures and data gaps?
- How would you approach data aggregation for analytics?

---

## Question 11: Distributed Task Scheduler
**Scenario:** Design a distributed job scheduling system that ensures reliable execution across multiple data centers.

- How would you ensure jobs run exactly once despite node failures?
- What database would you use to track job state and history?
- How would you implement dependencies between jobs?
- How would you handle scheduling at massive scale (millions of jobs)?

---

## Question 12: Content Delivery Network (CDN)
**Scenario:** Design a global content delivery network that caches and serves content efficiently.

- How would you determine optimal edge server locations?
- What strategies would you use for cache invalidation?
- How would you handle dynamic content vs. static content?
- What metrics would you track to optimize the CDN's performance?

---

## Question 13: Rate Limiting Service
**Scenario:** Design a distributed rate limiting service that restricts API usage across a microservice architecture.

- How would you implement rate limiting that works across multiple service instances?
- What database or data structure would you use to track request counts?
- How would you handle different rate limit policies (per user, IP, endpoint)?
- How would you ensure minimal latency impact on API calls?

---

## Question 14: Recommendation Engine
**Scenario:** Design a recommendation system like those used by Netflix or Amazon.

- What data storage would you use for user behavior and item catalogs?
- How would you architect the recommendation algorithm processing pipeline?
- How would you balance between real-time and batch processing?
- How would you handle the cold start problem for new users/items?

---

## Question 15: Location-Based Service
**Scenario:** Design a location-based service like Yelp or Google Maps that helps users find nearby places of interest.

- What database would you use for efficient geospatial queries?
- How would you implement real-time location updates?
- What caching strategies would you employ for popular areas?
- How would you handle varying density of locations in different regions?

---

## How to Approach These Questions

For each question:  
1. **Start with Requirements:** Clarify functional and non-functional requirements.  
2. **Identify Data Characteristics:** Determine what kind of data you're dealing with.  
3. **Select Appropriate Databases:** Apply your knowledge of database types.  
4. **Design High-Level Architecture:** Draw the main components and how they interact.  
5. **Address Scalability & Reliability:** Explain how your design handles failures.  
6. **Justify Your Choices:** Always explain why you made specific decisions.  

---

## Tips
- Explain trade-offs clearly  
- Start simple and iterate  
- Focus on patterns rather than specific tools  
- Connect your decisions to requirements  
- Use quantitative reasoning where possible
- Consider the full lifecycle of data (creation, storage, access, update, deletion)
- Address both happy path and failure scenarios
- Be prepared to discuss alternative approaches

---