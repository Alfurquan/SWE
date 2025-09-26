# Event driven architecture

Event-Driven Architecture (EDA) is a design paradigm in which a system is built around the production, detection, and consumption of events. An event is any significant change in state within a system, such as a user clicking a button, a sensor detecting a change in temperature, or an order being placed in an e-commerce application.

In EDA, components react to events asynchronously. Instead of constantly polling or waiting for data, components simply “listen” for events and act when they occur. This approach leads to systems that are more modular, scalable, and responsive.

## Key Components of EDA

```shell
                   +-----------------------+
                   |    Event Producers    |
                   | (e.g., Web App, IoT)  |
                   +-----------+-----------+
                               │
                               ▼
                    +---------------------+
                    |   Event Broker/     |
                    |   Message Queue     |
                    |  (e.g., Kafka)      |
                    +-----------+---------+
                               │
          ┌────────────────────┴────────────────────┐
          │                                         │
          ▼                                         ▼
   +--------------+                          +---------------+
   | Event        |                          | Event         |
   | Consumer A   |                          | Consumer B    |
   | (Analytics)  |                          | (Notification)|
   +--------------+                          +---------------+
```

### Event Producers

Event Producers generate events. They are the sources of information about changes in the system.

Examples:

- A web application that produces an "Order Placed" event when a customer completes a purchase.
- An IoT sensor that emits a "Temperature Changed" event.

### Event consumers

Event Consumers are the components that listen for and process events.

Examples:

- A notification service that sends confirmation emails when an order is placed.
- A thermostat system that adjusts heating when it receives a "Temperature Changed" event.

### Event Channels/Brokers

Event Channels or Brokers act as intermediaries that receive, store, and forward events from producers to consumers. They help decouple producers and consumers, allowing them to scale independently.

Examples:

- Message brokers like Apache Kafka, RabbitMQ, or AWS Kinesis.
- Event buses that route events to the appropriate consumers.

## Benefits of EDA

- Scalability
- Responsiveness
- Resilience and Flexibility
- Improved Resource Utilization
