# Microservices

In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery.

## When should we use microservices ?

Microservices provide benefits

- Strong module boundaries: Microservices reinforce modular structure, which is particularly important for larger teams.
- Independent deployment: Simple services are easier to deploy, and since they are autonomous, are less likely to cause system failures when they go wrong.
- Technology diversity: With microservices you can mix multiple languages, development frameworks and data-storage technologies.

But come with costs

- Distribution: Distributed systems are harder to program, since remote calls are slow and are always at risk of failure.
- Eventual Consistency: Maintaining strong consistency is extremely difficult for a distributed system, which means everyone has to manage eventual consistency.
- Operational Complexity: You need a mature operations team to manage lots of services, which are being redeployed regularly.

So, microservices are not a silver bullet. They are a powerful tool, but they come with trade-offs. You should consider using microservices when the benefits outweigh the costs for your specific use case. Some common scenarios where microservices can be beneficial include:

- Large and complex applications: If your application is growing in size and complexity, breaking it down into microservices can help manage that complexity.

- Independent development and deployment: If you have multiple teams working on different parts of the application, microservices can allow them to work independently and deploy their services without affecting others.

- Scalability: If different parts of your application have different scalability requirements, microservices can allow you to scale them independently. For example, if you have a service that handles user authentication and another service that handles product catalog, you can scale the authentication service independently of the product catalog service based on their respective loads.

- Technology diversity: If you want to use different technologies for different parts of your application, microservices can allow you to do that. For example, you might want to use a different programming language or database for a specific service that has unique requirements. For instance, you might choose to use Node.js for a service that handles real-time data processing, while using Python for a service that handles machine learning tasks.

- Organizational structure: If your organization is structured around small, cross-functional teams, microservices can align well with that structure. Each team can own and manage a specific service, which can lead to better collaboration and faster development cycles.

- Need for resilience: If you need to build a resilient system that can continue to function even if some parts fail, microservices can help by isolating failures to individual services. For example, if one service goes down, it won't necessarily bring down the entire application. Say you have an e-commerce application with separate services for user authentication, product catalog, and order processing. If the order processing service experiences an issue, the user authentication and product catalog services can continue to operate, allowing users to browse products and log in without interruption.


## How to break a monolith into microservices ?

### What to decouple and when

Deciding what capability to decouple when and how to migrate incrementally are some of the architectural challenges of decomposing a monolith to an ecosystem of microservices.
To clarify this, we will use an example of an multitier online retail application.

#### Warm Up with a Simple and Fairly Decoupled Capability

Start with capabilities that are fairly decoupled from the monolith, they don’t require changes to many client facing applications that are currently using the monolith and possibly don’t need a data store.

As an example, for an online retail application, the first service can be the ‘end user authentication’ service that the monolith could call to authenticate the end users, and the second service could be the ‘customer profile’ service, a facade service providing a better view of the customers for new client applications.

#### Minimize Dependency Back to the Monolith

A major benefit of microservices is to have a fast and independent release cycle. Having dependencies to the monolith - data, logic, APIs - couples the service to the monolith's release cycle, prohibiting this benefit.

Consider in a retail online system, where ‘buy’ and ‘promotions’ are core capabilities. ‘buy’ uses ‘promotions’ during the checkout process to offer the customers the best promotions that they qualify for, given the items they are buying. If we need to decide which of these two capabilities to decouple next, I suggest to start with decoupling ‘promotions’ first and then 'buy'. Because in this order we reduce the dependencies back to the monolith. In this order ‘buy’ first remains locked in the monolith with a dependency out to the new ‘promotions’ microservice.

#### Decouple Capabilities with Data Dependencies

When decoupling capabilities that have data dependencies, we need to consider how to migrate the data. There are two main strategies: database per service and shared database.

- Database per service: Each microservice has its own database, which it manages independently. This approach provides strong data encapsulation and allows each service to choose the most appropriate database technology for its needs. However, it can lead to data duplication and eventual consistency challenges.

- Shared database: Multiple microservices share a common database. This approach simplifies data management and can reduce duplication, but it can also lead to tight coupling between services and make it harder to evolve the database schema.

When decoupling capabilities with data dependencies, it is often beneficial to start with the database per service approach. This allows each service to have full control over its data and reduces dependencies on the monolith. In our example of the online retail application, when decoupling the 'customer orders' capability, we can create a new 'orders' microservice with its own database to manage order data independently from the monolith.

However, it is important to carefully plan the data migration process to ensure data consistency and integrity.

#### Consider Event-Driven Communication

When decoupling capabilities, consider using event-driven communication between services. This approach allows services to communicate asynchronously, reducing dependencies and improving scalability. For example, when a customer places an order, the order service can publish an event that the inventory service listens to in order to update stock levels. This decouples the two services and allows them to evolve independently.

#### Incremental Migration

Decomposing a monolith into microservices should be done incrementally. Start with a small number of services and gradually add more as needed. This allows you to learn from the process and make adjustments as necessary. It also reduces the risk of disruption to the existing system. In our online retail application example, we can start by decoupling the 'authentication' and 'customer profile' services, and then gradually move on to other capabilities like 'promotions', 'orders', and 'inventory'.

#### Monitoring and Observability

As you decouple capabilities into microservices, it is crucial to implement robust monitoring and observability. This includes logging, metrics, and tracing to track the performance and health of each service. Monitoring helps identify issues early and ensures that the system remains reliable as it evolves. In our online retail application, we can use tools like Prometheus and Grafana to monitor service performance and set up alerts for any anomalies.

---

## Strangler Fig Pattern

The Strangler Fig Pattern is a strategy for incrementally migrating a monolithic application to a microservices architecture. The idea is to create new services around the edges of the existing monolith, gradually replacing parts of the monolith with new services until the monolith is completely "strangled" and can be retired.

This pattern incrementally migrates a legacy system by gradually replacing specific pieces of functionality with new applications and services. As you replace features from the legacy system, the new system eventually comprises all of the old system's features. This approach suppresses the old system so that you can decommission it.

### Context and problem

As systems age, the development tools, hosting technologies, and architectural styles used to build them may become outdated. This can make it difficult to maintain and evolve the system to meet changing business needs.

Replacing an entire complex system is a huge undertaking. Instead, many teams prefer to migrate to a new system gradually and keep the old system to handle unmigrated features. However, running two separate versions of an application forces clients to track which version has individual features. Every time teams migrate a feature or service, they must direct clients to the new location. To overcome these challenges, you can adopt an approach that supports incremental migration and minimizes disruptions to clients.

### Solution

Use an incremental process to replace specific pieces of functionality with new applications and services. Customers can continue using the same interface, unaware that this migration is taking place.

The Strangler Fig pattern provides a controlled and phased approach to modernization. It allows the existing application to continue functioning during the modernization effort. A façade (proxy) intercepts requests that go to the back-end legacy system. The façade routes these requests either to the legacy application or to the new services.

- The Strangler Fig pattern begins by introducing a façade (proxy) between the client app, the legacy system, and the new system. The façade acts as an intermediary. It allows the client app to interact with the legacy system and the new system. Initially, the façade routes most requests to the legacy system.

- As the migration progresses, the façade incrementally shifts requests from the legacy system to the new system. With each iteration, you implement more pieces of functionality in the new system.

- After you migrate all of the functionality and there are no dependencies on the legacy system, you can decommission the legacy system. The façade routes all requests exclusively to the new system.

- You remove the façade and reconfigure the client app to communicate directly with the new system. This step marks the completion of the migration.

---

## Question: How do I decide when to split a monolith into services?

I view microservices as a solution to an organizational problem, not a technical default. I only break a monolith when we hit specific bottlenecks:

- The Velocity Bottleneck: When 50+ developers are blocked on a single CI/CD pipeline, and a merge conflict in 'Inventory' stops a release in 'Payments.'

- The Scaling Conflict: When one module (e.g., Image Processing) hogs CPU and starves a latency-sensitive module (e.g., Login), preventing us from scaling them independently.

- Fault Isolation: When a memory leak in a non-critical feature crashes the core checkout flow.

How I approach the split: I follow the Strangler Fig Pattern. I never do a 'big bang' rewrite.

- I identify edge capabilities first (like Notifications or Auth) that have few dependencies.

- I define the Data Boundary before the API. If I can't separate the tables, I can't separate the service.

- I prefer Event-Driven architecture (Async) between services to reduce temporal coupling—so if the 'Inventory' service is down, the 'Order' service can still accept requests."

---

## Cheatsheet

### Microservices Trade-offs (The "Why" & "Why Not")

### When to use (Pros):

- Independent Scaling: Scale the Checkout service (CPU intensive) separately from User Profile (Memory intensive).

- Fault Isolation: A memory leak in Recommendations doesn't crash the Payment flow.

- Org Alignment: Decouples teams. The "Search" team can release daily; the "Core Platform" team can release weekly.

- Tech Heterogeneity: Use Python for ML services, Go/Java for high-throughput backend services.

### The Price You Pay (Cons):

- Operational Complexity: You now have 50 services to monitor, log, and alert on instead of 1.

- Network Latency: Every function call is now a network hop (ms vs ns).

- Data Consistency: No more ACID transactions across modules. You enter the world of Eventual Consistency and Sagas.

- Testing Difficulty: End-to-end integration testing becomes exponentially harder.

### The Strangler Fig Pattern (The "How")

Concept: Instead of rewriting a legacy monolith from scratch (Big Bang), you gradually create a new system around the edges of the old one, letting the old one grow slowly until it is "strangled."

The 3 Steps to Note Down:

- Identify: Pick a specific functionality (e.g., "User Profile") that is relatively isolated.

- Transform (The Proxy): Put a Load Balancer / API Gateway in front of the Monolith.

Old Flow: User -> Monolith.

New Flow: User -> Gateway -> (If URL is /user) -> New Microservice.

Else: User -> Gateway -> Monolith.

- Eliminate: Once the new service is stable, delete the code from the Monolith.

---