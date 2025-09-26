# Tips for system design

The good news is that once you understand the basic concepts, the building blocks, and trade-offs, and learn how to connect them effectively, system design interviews become far less intimidating.

## What interviewers want to see ?

In a system design interview, the interviewer evaluates your ability to think critically, design effectively, and communicate clearly.

Here’s what they are looking for:

- Clarify Requirements: Can you ask the right questions to clarify functional and non-functional requirements?

- System Architecture: Can you outline the main components of the system (e.g., clients, APIs, databases, caching, load balancers) and explain how they interact?

- Scalability: Can your design handle increased traffic or scale with user growth?

- Fault Tolerance: Can you address single points of failure and ensure fault tolerance?

- Trade-Offs: Can you explain the pros and cons of your decisions and justify your choices?

- Detailing Components: Can you dive into the details of critical components (e.g., database schema, caching strategy, API design)?

- Bottlenecks and Edge Cases: Can you identify potential issues and propose strategies to mitigate them?

- Clear Communication: Can you articulate your ideas clearly and engage in a constructive discussion with the interviewer?

- Adaptability: Are you receptive to feedback and able to refine your design?

- Time Management: Can you manage your time effectively and focus on high-impact components?

- Patterns: Are you familiar with common system design patterns (e.g., sharding, replication, caching)?

- Tools: Can you discuss tools or technologies relevant to the problem?

## Allocate Time Wisely

System design interviews typically last 45-60 minutes, which means managing your time effectively is crucial.

A well-structured approach ensures you cover all key aspects of the design while leaving room for discussion and feedback with the interviewer.

Use a framework to structure your answers

## Clarify Functional Requirements First

A common mistake many candidates make is jumping directly into designing the system without fully understanding what needs to be built.

System design questions are intentionally open-ended and often underspecified. Interviewers deliberately withhold details, expecting you to ask the right questions to uncover the information you need.

To succeed, start by clarifying the functional requirements—the core features and use cases the system must support.

At this stage, avoid thinking about design, implementation, or technical specifics. The primary goal is to define what needs to be built, not how to build it or the scale it needs to support. Focus purely on understanding the "what."

Questions to Ask:

- What specific features does the system need?
- Are there any must-have or optional features?
- What are the main objects and their relations?
- How the objects will interact with each other and access pattern?
- Can the system’s objects be modified after creation?
- What types of data will the system handle?

Example: For a chat application:

- Users should be able to send and receive messages.
- The primary objects are users and messages.
- Users should view all messages in chronological order.
- Messages may be edited or deleted after being sent.
- Messages may include text, images, and videos.

## Consider Non-Functional Requirements

Once functional requirements are well-defined, shift your focus to non-functional requirements (NFRs).

These describe how the system should perform its functions.

The most common non-functional requirements you should consider in a system design interview are:

- Performance: How quickly should the system respond to user requests?
- Availability: Should the system tolerate downtime? If yes, how much?
- Consistency: Is strong or eventual consistency required?
- Security: Are there any special security considerations or workflows?

Questions to Clarify NFRs:

- What is the scale of the system?
- How many users should it support?
- How many requests per second should the server handle?
- Is downtime acceptable? What is the cost of downtime for this system?
- Is the system read-heavy or write-heavy? What is the read-to-write ratio?
- Should updates be visible to users instantly, or is a delay acceptable?
- Are there any specific security concerns?

Example: For a chat application:

- Scale: 1 million daily active users, with up to 10,000 concurrent users per server.
- Availability: Aim for 99.99% uptime (no more than ~52 minutes of downtime per year).
- Read-to-Write Ratio: High read volume as users fetch messages frequently compared to writing messages.
- Consistency: Messages should appear in real-time for recipients.

## 80/20 Rule in System Design Interviews

In system design interviews, 80% of the questions typically revolve around just 20% of the core concepts.

By focusing your preparation on these 15 key areas, you can maximize your chances of performing well in the majority of interviews

1. Scalability: Horizontal and Vertical Scaling, Load Balancing

2. Databases: SQL vs NoSQL, Replication, Partitioning/Sharding, Indexing, Consistent Hashing, CAP Theorem

3. Caching: In-Memory Caching, Cache Invalidation, Caching Strategies, CDN (Content Delivery Network)

4. Load Balancers: Layer 4 vs. Layer 7 Load Balancers, Load Balancing Algorithms, Health Checks

5. Asynchronous Processing: Message Queues, Background Jobs

6. APIs: REST vs GraphQL, Endpoints, Rate Limiting, Idempotency

7. File Storage: Blob Storage, File Upload and Download, Replication

8. Monitoring and Logging: Metrics Collection, Centralized Logging

9. Security: Authentication and Authorization, Data Encryption, Rate Limiting and DDoS Protection

10. High Availability: Replication and Failover, Redundancy

11. Fault Tolerance: Retries, Circuit Breakers

12. Real-Time Communication: WebSockets, Polling vs. Long Polling

13. Microservices: REST vs. gRPC, Service Discovery

14. Search Systems: Inverted Index, Search Tools

15. Data Flow: ETL Pipelines, Data Streams

## Avoid Over-Engineering

Over-engineering happens when you introduce unnecessary complexity or design features that extend beyond the scope of the problem.

In system design interviews, simplicity is key—it shows clarity in thought and practicality in solving the problem.

If there’s a simple way and a complex way to solve a problem, choose the simple path. Not because it’s always correct, but because simpler designs rely on fewer assumptions and are easier to understand and implement.

### How to avoid over engineering ?

- Start Simple and Iterate: Propose a basic solution first and refine it as needed.

Example: Use a single database initially; add caching or sharding later as the system scales.

- Solve for Current Needs: Design for the system’s current scale and requirements rather than hypothetical future scenarios.

Example: A monolith may suffice for a small user base; microservices can come later.

- Avoid Premature Optimization: Focus on solving actual problems, not optimizing for unlikely bottlenecks.

Example: Skip caching until database reads become a performance issue.

- Justify Simplicity: Explain why your design meets the requirements without adding unnecessary layers.

Example: "A monolithic architecture works for this MVP as it simplifies deployment and minimizes operational overhead."

## “Why” Is More Important Than “What”

In system design interviews, explaining why you make decisions is far more important than simply listing technologies or approaches.

Interviewers cares less about whether your design is good in itself, and more about whether you are able to talk about the trade-offs (positives and negatives) of your decisions.

They want to understand how you think and how well your decisions align with the problem’s requirements.

### How to Effectively Explain “Why” ?

- **Tie It to Requirements:** Connect your decisions to the functional and non-functional requirements you clarified at the start of the interview.

Example: **“I’m choosing a NoSQL database because this system requires high write throughput and a flexible schema.”**

- **Highlight Trade-Offs:** Acknowledge the downsides of your choice and explain why you think the benefits outweigh the drawbacks.

Example: **“Using WebSockets enables real-time updates, but it introduces additional complexity in connection management. However, it’s necessary for the low-latency requirements of a chat application.”**

- **Use Real-World Analogies:** Relate your reasoning to real-world systems or similar problems you’ve studied or worked on.

Example: **“I’m proposing a content delivery network (CDN) because companies like Netflix and YouTube use CDNs to serve static content efficiently to users worldwide.”**

- **Leverage Metrics:** Back up your “why” with numbers or estimations where possible.

Example: **“I’m suggesting horizontal scaling with sharding because we expect 1 million active users, and a single database node won’t handle the write throughput of 10,000 requests per second.”**

- **Balance Simplicity and Functionality:** Show how your choice meets the needs without unnecessary complexity.

Example: **“While we could use microservices for this system, a monolithic architecture will be easier to implement and maintain for the given scale of 10,000 daily users.”**

## Focus on Patterns, Not Tools

Interviewers are more interested in your understanding of concepts and the reasoning behind your choices than in your ability to name-drop technologies.

While tools are important, focusing on patterns and trade-offs shows you understand the underlying principles of system design and can adapt your choices to fit different scenarios.

### How to Focus on Patterns ?

- Discuss Alternatives First, Then Decide: Explain the problem, list a few possible solutions (patterns), and justify your choice.

Example:

Instead of: "I’ll use Cassandra for our database."

Say: "This system needs high write throughput and horizontal scalability. We could use a NoSQL database like DynamoDB or Cassandra. Based on the trade-offs, Cassandra is a better fit for handling our write-heavy workload."

- Avoid Name-Dropping Without Context: Don’t mention a tool unless you’re prepared to explain why it’s appropriate and how it works.

Example:

Instead of: "I’ll use Kafka for message queuing."

Say: "We need a message queue to decouple services. Kafka or RabbitMQ could work, but Kafka’s high throughput and durability make it ideal for our use case."

- Use Broad Categories First: Refer to the type of tool (e.g., NoSQL database, message queue) rather than naming a specific product initially.

Example:

Instead of: "We’ll use Elasticsearch for search."

Say: "We need a search system to index and query large datasets efficiently. Tools like Elasticsearch or Solr could fulfill this requirement."

## Choose the Right Database

Selecting the right database is one of the most critical decisions in system design.

Your choice should align with the system's requirements, including scalability, consistency and query patterns.
