# 🔍 Google Search & Indexing

## Question 1 — Search Query Suggestions (Two Pointers / Sliding Window + Trie)

> "At Google Search, we want to implement an intelligent autocomplete system. Given that users type queries character by character, design a system that can suggest the most relevant completions in real-time. The system should handle typos within 1-2 character differences and prioritize suggestions based on popularity scores.  
>  
> Consider that we process billions of queries daily, and the suggestion system needs to respond within 50ms. How would you handle the scenario where a user types 'goggle' but means 'google'? Also, what if we want to show suggestions that contain all the typed characters but not necessarily in sequence?"

### Follow-ups
- How would you handle trending queries that suddenly become popular?  
- What if we want to personalize suggestions based on user's search history?  
- How would you efficiently update popularity scores in real-time?  
- How would you handle multilingual queries and suggestions?

---

## Question 2 — Web Page Ranking (Binary Search + Graph Algorithms)

> "Google's search algorithm needs to rank billions of web pages. Given a directed graph representing web pages and their links, along with various quality signals (page load time, content freshness, user engagement), design an algorithm to compute and maintain page rankings.  
>  
> The challenge is that the web graph changes constantly - new pages are added, links are modified, and quality signals update in real-time. Your ranking algorithm should be able to handle incremental updates efficiently rather than recomputing everything from scratch."

### Follow-ups
- How would you handle the case where a highly authoritative site links to a spam page?  
- What if we want to personalize rankings based on user location and preferences?  
- How would you detect and handle link farms or artificial link manipulation?  
- How would you ensure rankings are computed fairly across different languages and regions?

---

# 📺 YouTube & Video Platform

## Question 3 — Video Recommendation Engine (Dynamic Programming + Prefix Sum)

> "YouTube needs to generate personalized video recommendations for each user. Given a user's watch history, video metadata (categories, duration, upload time), and interaction data (likes, comments, shares), design an algorithm that finds the optimal sequence of videos to recommend.  
>  
> The goal is to maximize user engagement time while ensuring diversity in content. You have constraints like: no more than 2 videos from the same channel in top 10 recommendations, balance between trending and personalized content, and consideration of video duration vs. available user time."

### Follow-ups
- How would you handle the cold start problem for new users?  
- What if a user's preferences change dramatically over time?  
- How would you ensure recommendations don't create filter bubbles?  
- How would you handle real-time events affecting video popularity?

---

## Question 4 — Live Stream Chat Moderation (Stack/Queue + String Processing)

> "YouTube Live streams can have thousands of concurrent viewers sending chat messages. Design a real-time content moderation system that can detect and filter inappropriate content, spam, and repetitive messages.  
>  
> The system should handle different types of violations: spam detection (repeated messages), inappropriate content, link sharing restrictions, and rate limiting per user. Consider that chat messages arrive at high velocity and moderation decisions must be made in real-time."

### Follow-ups
- How would you handle false positives in content moderation?  
- What if streamers want custom moderation rules for their channels?  
- How would you detect coordinated spam attacks from multiple accounts?  
- How would you scale this across multiple languages and cultural contexts?

---

# 🗺️ Google Maps & Location Services

## Question 5 — Route Optimization with Traffic (Dijkstra + Union Find)

> "Google Maps needs to find the optimal route between two points considering real-time traffic conditions, road closures, and user preferences (fastest vs shortest vs most fuel-efficient). Design an algorithm that can handle dynamic updates to traffic conditions and provide alternative routes.  
>  
> The system receives traffic updates every few seconds from millions of devices. Your algorithm should be able to quickly recalculate routes when significant traffic changes occur without recomputing everything from scratch."

### Follow-ups
- How would you handle the case where the fastest route changes multiple times during navigation?  
- What if we want to provide routes that avoid toll roads or highways?  
- How would you predict traffic conditions for future time slots?  
- How would you handle routing for different vehicle types (cars, bicycles, public transport)?

---

## Question 6 — Location-Based Service Discovery (Binary Search + Greedy)

> "When users search for 'restaurants near me' on Google Maps, design an algorithm that efficiently finds and ranks nearby businesses. Consider factors like distance, ratings, current open/close status, user preferences, and real-time popularity.  
>  
> The system should handle queries like 'pizza places open now within 5 miles' and return results sorted by relevance. You need to consider that business information changes frequently (hours, ratings, availability) and user location may be imprecise."

### Follow-ups
- How would you handle searches in areas with sparse business data?  
- What if we want to promote local businesses over chains?  
- How would you integrate real-time data like current wait times?  
- How would you handle multi-language business names and categories?

---

# 📧 Gmail & Communication

## Question 7 — Email Thread Grouping (Graph DFS/BFS + Hashing)

> "Gmail automatically groups related emails into conversation threads. Design an algorithm that can identify which emails belong to the same conversation, considering factors like subject line similarity, reply chains, participant overlap, and time proximity.  
>  
> Handle edge cases like when users change subject lines, forward emails to new participants, or when automated systems generate emails with similar subjects but are unrelated."

### Follow-ups
- How would you handle email threads that span multiple years?  
- What if users manually split or merge conversations?  
- How would you detect when a conversation topic changes significantly?  
- How would you handle threading across different email providers?

---

## Question 8 — Smart Compose Suggestions (Backtracking + Dynamic Programming)

> "Gmail's Smart Compose feature suggests completions as users type emails. Design an algorithm that generates contextually appropriate suggestions based on the email content, recipient, user's writing style, and common phrases.  
>  
> The system should provide multiple suggestion options and update them in real-time as the user continues typing. Consider privacy constraints - suggestions should be generated without sending data to servers."

### Follow-ups
- How would you personalize suggestions based on user's profession or industry?  
- What if users want suggestions in multiple languages?  
- How would you handle formal vs informal tone suggestions?  
- How would you prevent inappropriate suggestions in professional contexts?

---

# ☁️ Google Cloud & Infrastructure

## Question 9 — Auto-scaling Resource Manager (Greedy + Binary Search)

> "Google Cloud needs an intelligent auto-scaling system that can predict and provision resources for customer applications. Given historical usage patterns, current load metrics, and application performance requirements, design an algorithm that optimally scales resources up or down.  
>  
> The system should minimize costs while ensuring performance SLAs are met. Consider factors like startup time for new instances, cooling-down periods to prevent oscillation, and different scaling policies for different application types."

### Follow-ups
- How would you handle sudden traffic spikes that exceed historical patterns?  
- What if different components of an application have different scaling requirements?  
- How would you predict resource needs during special events or holidays?  
- How would you handle cascading failures when scaling decisions affect dependent services?

---

## Question 10 — Distributed Cache Consistency (Union Find + Hashing)

> "Design a globally distributed caching system for Google Cloud that maintains consistency across multiple data centers. The system should handle cache invalidation, replication, and conflict resolution when the same data is updated simultaneously in different regions.  
>  
> Consider network partitions, varying latencies between regions, and the trade-off between consistency and availability. The system should intelligently route requests to the nearest available cache while maintaining data integrity."

### Follow-ups
- How would you handle the case where a data center goes offline?  
- What if different regions have different data sovereignty requirements?  
- How would you optimize cache placement based on user access patterns?  
- How would you handle cache warming for new data centers?

---

# 📱 Android & Mobile Services

## Question 11 — App Store Recommendation Engine (Monotonic Stack + Prefix Sum)

> "Google Play Store needs to recommend apps to users based on their download history, device specifications, usage patterns, and app ratings. Design an algorithm that generates personalized app recommendations while considering storage constraints and device compatibility.  
>  
> The system should balance between popular apps and niche apps that match user interests. Consider factors like app size, device RAM/storage, Android version compatibility, and regional preferences."

### Follow-ups
- How would you recommend apps for users who rarely download new apps?  
- What if we want to promote apps from smaller developers?  
- How would you handle recommendations for shared family devices?  
- How would you detect and prevent fake app ratings from affecting recommendations?

---

# 💡 Practice Approach for L5 Interviews

For each question:

1. Spend **5–7 minutes** clarifying requirements and constraints.  
2. Start with a **brute force** approach — show you understand the problem.  
3. Identify the **core pattern** and explain why it applies.  
4. **Optimize step by step** — don't jump to the final solution.  
5. Discuss **trade-offs** between different approaches.  
6. Consider **scale** — how would this work with billions of users?  
7. Handle **edge cases** systematically.  
8. Use follow-ups to show ability to **extend and adapt** solutions.

## Key L5 Expectations
- **System thinking:** Connect algorithms to real system constraints.  
- **Optimization mindset:** Always consider multiple approaches.  
- **Scalability awareness:** Think beyond toy examples.  
- **Product intuition:** Understand why Google would need this solution.  
- **Code quality:** Even in pseudocode, show clean structure.

> These questions will help you practice pattern recognition while building intuition for how these algorithms apply to real Google products. Each question can be extended into system design discussions, making them perfect preparation for L5 interviews.
