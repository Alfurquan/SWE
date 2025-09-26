# Questions to solidify

## Scenario 1: E-Commerce Platform

Question: You're designing an e-commerce system with these components:

- Product catalog with descriptions and images
- Inventory management system tracking stock levels
- Shopping cart functionality
- Order processing and payment system
- User reviews and ratings

For each component, decide which consistency model (strong or eventual) would be appropriate. Justify your choices with tradeoffs and explain any hybrid approaches you might implement. Also, describe how you would handle specific edge cases like inventory updates during flash sales.

## Answer

So for this scenario we are designing and e-commerce platform. For each component, I will list down the consistency model we can take along with the reason.

### Product catalog with descriptions and images

For this component, Eventual consistency works well.

Reasons for this

- No strong data criticality, its fine if some users see stale description and images.
- High availability, we do not want the system to go down if we are not able to fetch latest product description and images
- Low latency, we do not want the system to slow down in an attempt to fetch latest product description and images.
- For this I will favour availability > consistency for CAP theorem

### Inventory management system tracking stock levels

For this component, Strong consistency works well.

Reasons for this

- Strong data criticality, We do not want users to see wrong or stale inventory of items.
- Its fine to bear some latency in this case, as we do not want users to see and work on stale data for inventory
- For this I will favour consistency > availability for CAP theorem

### Shopping cart functionality

For this component, we can take a Hybrid approach with strong consistency for adding to cart functionality and eventual consistency for syncing cart state across user's multiple devices.

Reason for strong consistency

- We do not want user to update wrong data while adding/modifying items to cart.
- For this I will favour consistency > availability for CAP theorem

Reason for eventual consistency

- Syncing of cart state across user's multiple devices (like web app or mobile app) can happen in background.
- No strong data criticality needs.
- We do not want high latency while user is updating items in cart, just because we want to sync cart state across their multiple devices.
- For this I will favour availability > consistency for CAP theorem

### Order processing and payment system

For order processing and payment system we need strong consistency

Reason for this

- Data criticality, we do not want customers to do double payment if something goes wrong.
- Some amount of latency to ensure consistency is fine here.
- For this I will favour consistency > availability for CAP theorem

### User reviews and ratings

For this eventual consistency works well

- No strong data criticality, its fine if some users see stale reviews and ratings.
- High availability, we do not want the system to go down if we are not able to fetch latest reviews and ratings
- Low latency, we do not want the system to slow down in an attempt to fetch latest reviews and ratings
- For this I will favour availability > consistency for CAP theorem
- Also we can use read your writes consistency, so that users can see their writes immediately.

### Inventory updates during flash sales

We need strong consistency for inventory updates of product items. During flash sales when load is quite high, we will scale the system to support low latency writes. We can use sharding of databases, and partitioning to make sure the system can handle the peak load. Also we can use batching to update inventory items to handle bulk updates.

We can also use write-through cache for low latency writes and also use queues to handle batch updates in background to ensure the system has low latency during peak times.
