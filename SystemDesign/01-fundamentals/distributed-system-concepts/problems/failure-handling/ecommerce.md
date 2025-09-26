# E-Commerce Product Catalog

## Question

Your product catalog service is becoming overwhelmed with requests during a flash sale. Design a system that:

- Remains available even under extreme load
- Prioritizes purchase-related queries over browsing
- Degrades gracefully when dependencies fail

## Answer

We want to design a highly available and fault tolerant e-commerce product catalog system that is resilient to failures. Here are some of the strategies we can take to achieve our goal

- Replicate data across multiple nodes, and distribute requests across these nodes so that a single node does not get overwhelmed.
- Replicating the data also serves the case that when one of the nodes goes down, requests can still be served from other nodes, and the whole system as a whole will not go down.
- Under extreme load, we can prioritize purchase related queries over browsing by auto scaling the purchase service so that it can serve higher load.
- If external dependencies like payment gateway fail, we can add retries to those operations from our payment service. We can also queue the failed requests to be processed asynchronously later when the payment gateway is up. We show a order processing page to the users. When payment is finally completed, we send SMS/email to them. In case of critical payments, we can fallback to another payment gateway.
- We fallback to defaults if some services fail, for e.g if recommendation service fails, we can just show top products to the user instead of not showing them anything, if review service fails, we can fallback and just show product without reviews etc. This way we can fallback and give the users something instead of nothing.
- If load is too much on any service, we can load shed it and give it some time to recover so that with bursts of requests it does not degrade further. During this time we can fallback to defaults and keep the app up and running.
- We can also deploy monitoring and alerting to monitor key metrics like failure rates, uptime of services etc. and alert us if they go below a threshold value.
- We can also deploy auto heal to auto heal the services if it recovers instead of manual intervention. For e.g if failure rates have a threshold of lets say 100 failures/hour and if the system recovers and it has value above it, we can use an orchestrator like kubernetes to auto restart the system and heal it.


## L5-Level Answer

To build a highly available, resilient product catalog system for flash sales, I would use the following strategies:

### 1. High Availability and Scalability

- **Multi-region replication**: Product data is replicated across multiple regions and nodes. Requests are routed using a load balancer to healthy nodes, ensuring continued availability if any node or region fails.
- **Aggressive caching**: Product catalog data is cached at multiple layers (CDN, edge cache, in-memory cache like Redis) to serve browsing requests with minimal backend impact.
- **Auto-scaling**: Services are auto-scaled based on real-time metrics (CPU, RPS, latency) to handle traffic spikes.

### 2. Request Prioritization

- **API Gateway with priority queues**: Requests are tagged at the gateway. Purchase-related requests are routed to dedicated, high-priority queues with reserved resources, ensuring they are processed first.
- **Rate limiting and traffic shaping**: Browsing endpoints are rate-limited per user/IP, and excess requests are dropped (HTTP 429) or served from cache. Purchase endpoints have higher rate limits and guaranteed capacity.

### 3. Graceful Degradation

- **Fallbacks for dependencies**: If recommendation or review services fail, serve cached popular products or show products without reviews. If payment gateway fails, queue requests for asynchronous processing and notify users of order status.
- **Static and cached pages**: For browsing, serve static or cached pages if backend services are slow or unavailable.
- **Load shedding**: Non-critical requests (e.g., analytics, personalization) are dropped during overload to preserve core functionality.

### 4. Backpressure and Flow Control

- **Backpressure signals**: Use protocols like HTTP/2 or gRPC to signal upstream systems to slow down when overwhelmed, preventing cascading failures.

### 5. Monitoring, Alerting, and Auto-Healing

- **Service-level objectives (SLOs)**: Monitor p99 latency, error rates, and request throughput. Trigger auto-scaling, failover, or load shedding when thresholds are breached.
- **Auto-healing**: Use orchestrators (e.g., Kubernetes) to automatically restart unhealthy services and roll back failed deployments.

### 6. Trade-offs and CAP Theorem

- **Consistency vs. availability**: For browsing, favor availability and serve eventually consistent data. For purchase flows, favor consistency using distributed transactions and idempotency keys to ensure order integrity.

---

This approach ensures the product catalog remains available, prioritizes critical purchase flows, and degrades gracefully under failure, meeting the expectations for a senior engineer at Google.