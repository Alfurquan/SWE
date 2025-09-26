# Stateful vs. Stateless Architecture

When a client interacts with a server, there are two ways to handle it:

- Stateless: The client includes all necessary data in each request, so the server doesn’t store any prior information.
- Stateful: The server retains some data from previous requests, making future interactions dependent on past state.

## Stateful architecture

In a stateful architecture, the system remembers client or process data (state) across multiple requests.
Once a client connects, the server holds on to certain details—like user preferences, shopping cart contents, or authentication sessions—so the client doesn’t need to resend everything with each request.

Stateful systems typically store the state data in a database or in-memory storage.

### Common patterns in stateful architecture

#### Sticky sessions

If you use in-memory session storage (i.e., each app server keeps its own sessions locally), you can configure your load balancer for “sticky sessions.” Once a client is assigned to Server A, all subsequent requests from that client are routed to Server A.

**Trade-Off: If Server A fails, the user’s session data is lost or the user is forced to re-log in. Sticky sessions are also less flexible when scaling because you can’t seamlessly redistribute user traffic to other servers.**

#### Centralized session store

A more robust approach is to store session data in a centralized or distributed store (e.g., Redis). This allows:
Shared access: All servers can access and update session data for any user. Any server can handle any request, because the session data is not tied to a specific server’s memory.

**Trade-Off: You introduce network overhead and rely on an external storage. If the centralized storage fails, you lose session data unless you have a fallback strategy.**

### Example Use Cases

- E-commerce Shopping Carts – Stores cart contents and user preferences across multiple interactions, even if the user navigates away and returns.

- Video Streaming Services (Netflix, YouTube) – Remembers user watch progress, recommendations, and session data for a seamless experience.

- Messaging Apps (WhatsApp, Slack) – Maintains active user sessions and message history for real-time communication.

## Stateless architecture

In a stateless architecture, the server does not preserve client-specific data between individual requests.

- Each request is treated as independent, with no memory of previous interactions.
- Every request must include all necessary information for processing.
- Once the server responds, it discards any temporary data used for that request.

Example: Most RESTful APIs follow a stateless design. For instance, when you request weather data from a public API, you must provide all required details (e.g., location) in each request. The server processes it, sends a response, and forgets the interaction.

### Common patterns in stateless architecture

#### Token-Based Authentication (JWT)

A very popular way to implement statelessness is through tokens, particularly JWTs (JSON Web Tokens):

- Client Authenticates Once: The user logs in using credentials (username/password) for the first time, and the server issues a signed JWT.
- Subsequent Requests: The client includes JWT token in each request (e.g., Authorization: Bearer token header).
- Validation: The server validates the token’s signature and any embedded claims (e.g., user ID, expiry time).
- No Server-Side Storage: The server does not need to store session data; it just verifies the token on each request.

Many APIs, including OAuth-based authentication systems, use JWTs to enable stateless, scalable authentication.

#### Idempotent APIs

Stateless architectures benefit from idempotent operations, ensuring that repeated requests produce the same result. This prevents inconsistencies due to network retries or client errors.

### Example use cases

- Microservices Architecture: Each service handles requests independently, relying on external databases or caches instead of maintaining session data.
- Public APIs (REST, GraphQL): Clients send tokens with each request, eliminating the need for server-side sessions.
- Mobile Apps: Tokens are securely stored on the device and sent with every request to authenticate users.
- CDN & Caching Layers: Stateless endpoints make caching easier since responses depend only on request parameters, not stored session data. A CDN can cache and serve repeated requests, improving performance and reducing backend load.

## Choosing right approach

There's no one-size-fits-all answer when choosing between stateful and stateless architectures.

The best choice depends on your application’s needs, scalability goals, and user experience expectations.

### When to choose stateful architecture ?

Consider a stateful approach if your application:

- Requires personalization (e.g., user preferences, session history)
- Needs real-time interactions (e.g., chat applications, multiplayer gaming)
- Manages multi-step workflows (e.g., online banking transactions, checkout processes)
- Must retain authentication sessions for security and convenience

### When to choose stateless architecture ?

- Handles a high volume of requests and needs to scale efficiently
- Doesn’t require storing client-specific data between requests
- Needs fast, distributed processing without server dependencies
- Must ensure reliability and failover readiness.

### Hybrid Approaches: The Best of Both Worlds

Many modern applications blend stateful and stateless components for flexibility.

This hybrid approach allows:

- Stateless APIs for core functionality, ensuring high scalability
- Stateful sessions for personalization, improving user experience
- External session stores (e.g., Redis) to manage state while keeping app servers stateless

Example: A video streaming platform (e.g., Netflix) uses a stateless backend for streaming but retains stateful user sessions to track watch history and recommendations.
