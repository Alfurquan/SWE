# Load balancers

Load Balancer is a system that spreads incoming network traffic across multiple backend servers (often called “worker nodes” or “application servers”).

It ensures that no single server becomes a bottleneck due to an overload of requests. By distributing the load, applications can handle higher volumes of traffic and remain robust in the face of server failures.

## Why do we need a load balancer ?

- Scalability: As traffic grows, you can add more servers behind the load balancer without redesigning your entire architecture.
- High availability: If one server goes offline or crashes, the load balancer automatically reroutes traffic to other healthy servers.
- Performance optimization: Balancing load prevents certain servers from overworking while others remain underutilized.

## Types of load balancers

### Hardware vs Software

- Hardware Load Balancer: Specialized physical devices often used in data centers (e.g., F5, Citrix ADC). They tend to be very powerful but can be expensive and less flexible.

- Software Load Balancer: Runs on standard servers or virtual machines (e.g., Nginx, HAProxy, Envoy). These are often open-source or lower-cost solutions, highly configurable, and simpler to integrate with cloud providers.

### Layer 4 vs. Layer 7

- Layer 4 (Transport Layer): Distributes traffic based on network information like IP address and port. It doesn’t inspect the application-layer data (HTTP, HTTPS headers, etc.).

- Layer 7 (Application Layer): Can make distribution decisions based on HTTP headers, cookies, URL path, etc. This is useful for advanced routing and application-aware features.

## How load balancers works ?

- Traffic reception
- Decision logic (Routing algorithm)
- Server health checks
- Response handling
