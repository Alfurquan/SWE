# Vertical vs Horizontal Scaling

When your application gets bigger, it needs more resources.
To handle this growth, two common approaches are vertical and horizontal scaling.

## Vertical Scaling (Scaling Up)

Vertical scaling, also known as "scaling up" involves boosting the power of an existing machine within your system to handle increased loads.
This can mean upgrading the CPU, RAM, Storage, or other hardware components to boost the server's capacity.

### Pros of vertical scaling

- Simplicity
- Lower latency
- Reduced software costs
- No major code changes

### Cons of vertical scaling

- Limited scaling
- Single point of failure
- Downtime

## Horizontal Scaling (Scaling Out)

Horizontal scaling, or scaling out, involves adding more servers or nodes to the system to distribute the load across multiple machines.
Each server runs a copy of the application, and the load is balanced among them often using a load balancer.

### Pros of horizontal scaling

- Near-Limitless Scalability
- Improved fault tolerance
- Cost-effective

### Cons of horizontal scaling

- Complexity
- Increased latency
