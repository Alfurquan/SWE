# Multi step process

⚙️ Real production systems must survive failures, retries, and long-running operations spanning hours or days. Often they take the form of multi-step processes or sagas which involve the coordination of multiple services and systems. This is a continual source of operational and design challenges for engineers, with a variety of different solutions.

## The Problem

Consider an e-commerce order fulfillment workflow: charge payment, reserve inventory, create shipping label, wait for a human to pick up the item, send confirmation email, and wait for pickup. Each step involves calling different services or waiting on humans, any of which might fail or timeout. Some steps require us to call out to external systems (like a payment gateway) and wait for them to complete. During the orchestration, your server might crash or be deployed to. And maybe you want to make a change to the ordering or nature of steps! The messy complexity of business needs and real-world infrastructure quickly breaks down our otherwise pure flow chart of steps.

There are, of course, patches we can organically make to processes like this. We can fortify each service to handle failures, add compensating actions (like refunds if we can't find the inventory) in every place, use delay queues and hooks to handle waits and human tasks, but overall each of these things makes the system more complex and brittle. We interweave system-level concerns (crashes, retries, failures) with business-level concerns (what happens if we can't find the item?). Not a great design!

## Solutions

Let's work through different approaches to building reliable multi-step processes, starting simple and building up to sophisticated workflow systems.

### Single server Orchestration

The most straightforward solution is the one most engineers start with: it's to orchestrate everything from a single server, often in a single service call. Your API server receives the order request, calls each service sequentially, and returns the result. If you didn't know any better, this would be where you'd start!

Not all problems involve complex state management or failure handling. And for these simple cases, single-server orchestration is a perfectly fine solution. But it has serious problems as soon as you need reliability guarantees and more complex coordination. What happens when the server crashes after charging payment but before reserving inventory? When the server restarts, it has no memory of what happened. Or how can we ensure the webhook callback we get from our payment gateway makes its way back to the initiating API server? Are we stuck with a single host with no way to scale or replicate?
You might try to solve this by adding state persistence between each step and maybe a pub/sub system to route callbacks.

We'll solve the callback with pub/sub. And we can scale out our API servers now because when they start up, they can read their state from the database. But this quickly becomes complex, and we've created more problems than we've solved. As an example:

- You're manually building a state machine with careful database checkpoints after each step. What if you have multiple API servers? Who picks up the dropped work?
- You still haven't solved compensation (how do we respond to failures?). What if inventory reservation fails? You need to refund the payment. What if shipping fails? You need to release the inventory reservation.

### Event Sourcing

The most foundational solution to this problem is to use an architectural pattern known as event sourcing. Event sourcing offers a more principled approach to our earlier single-server orchestration with state persistence. Instead of storing the current state, you store a sequence of events that represent what happened.

The most common way to store events is to use a durable log and Kafka is a popular choice, although Redis Streams could work in some places.

**Event sourcing is a close, but more practical cousin to Event-Driven Architecture. Whereas EDA is about decoupling services by publishing events to a topic, event sourcing is about replaying events to reconstruct the state of the system with the goal of increasing robustness and reliability.**

#### How it works ?

We're using the logs in event store to store the entire history of the system but also to orchestrate next steps. Whenever something happens that we need to react to, we write an event to the event store and have a worker who can pick it up and react to it. Each worker consumes events, performs its work, and emits new events.

So the payment worker sees "OrderPlaced" and calls our payment service. When the payment service calls back later with the status, the Payment Worker emits "PaymentCharged" or "PaymentFailed". The inventory worker sees "PaymentCharged" and emits "InventoryReserved" or "InventoryFailed". And so on.

Our API service is now just a thin initiating wrapper around the event store. When the order request comes in, we emit an "OrderPlaced" event and the system springs to life to carry the event through the system. Rather than services exposing APIs, they are now just workers who consume events.

This gives you:

- Fault tolerance: If a worker crashes, another picks up the event
- Scalability: Add more workers to handle higher load
- Observability: Complete audit trail of all events
- Flexibility: Possible to add new steps or modify workflows

Good stuff! But you're building significant infrastructure to make it work like event stores, message queues, and worker orchestration. For complex business processes, this becomes its own distributed systems engineering project.

### Workflows

What we really want to do is to describe a workflow, a reliable, long-running processes that can survive failures and continue where they left off. Our ideal system needs to be robust to server crashes or restarts instead of losing all progress and it shouldn't require us to hand-roll the infrastructure to make it work.

Enter workflow systems and durable execution engines. These solutions provide the benefits of event sourcing and state management without requiring you to build the infrastructure yourself. Just like systems like Flink provide a way for you to describe streaming event processing at a higher-level, workflow systems and durable execution engines give tools for handling these common multi-step processes. Both provide a language for you to describe the high-level workflow of your system and they handle the orchestration of it, but they differ in how those workflows are described and managed.

Some popular workflow systems include:

- Temporal: A popular open-source workflow engine that provides durable execution and state management. You write workflows in code (Go, Java, Python) and Temporal handles the rest.
- Apache Airflow: A platform to programmatically author, schedule, and monitor workflows. It uses directed acyclic graphs (DAGs) to manage workflow orchestration.
- AWS Step Functions: A serverless orchestration service that lets you combine AWS Lambda functions and other AWS services to build business-critical applications. You define workflows using JSON-based Amazon States Language.
- Cadence: An open-source, distributed, scalable, durable, and highly available orchestration engine developed by Uber. It allows you to write long-running workflows in code.
- Netflix Conductor: A microservices orchestration engine that runs in the cloud. It provides a way to define workflows using JSON and supports long-running processes.

These systems provide built-in support for retries, timeouts, and compensation actions. They also handle state persistence and recovery, so if a server crashes, the workflow can continue where it left off. This allows you to focus on the business logic of your workflows rather than the underlying infrastructure.

### When to use in interviews ?

Workflows often show up when there is a state machine or a stateful process in the design. If you find a sequence of steps that require a flow chart, there's a good chance you should be using a workflow system to design the system around it.

A couple examples:

- Payment Systems - In Payment Systems or systems that engage with them (like e-commerce systems), there's frequently a lot of state and a strong need to be able to handle failures gracefully. You don't want a user to end up with a charge for a product they didn't receive!
  
- Human-in-the-Loop Workflows - In products like Uber, there are a bunch of places where the user is waiting on a human to complete a task. When a user requests a driver, for instance, the driver has to accept the ride. These make for great workflow candidates.

In your interview, listen for phrases like "if step X fails, we need to undo step Y" or "we need to ensure all steps complete or none do." That's a clear signal for workflows.

In interviews, demonstrate maturity by starting simple. Only introduce workflows when you identify specific problems they solve: partial failure handling, long-running processes, complex orchestration, or audit requirements. Show you understand the tradeoffs.

---