# Saga Pattern

The SAGA Pattern is an architectural approach to managing long-lived, distributed transactions in microservices. Instead of using a traditional, centralized transaction to ensure atomicity across services, a saga breaks the process into a series of local transactions. Each local transaction updates the database and publishes an event or invokes a service that triggers the next transaction in the saga.

## How the SAGA Pattern Works ?

Local Transactions and Compensating Actions

In a saga, the overall process is divided into a series of local transactions, each executed within a single microservice. Once a local transaction is successfully completed, it triggers the next transaction in the chain. However, if one transaction fails, the saga invokes compensating actions to undo the previous transactions, ensuring that the system reverts to a consistent state

Example Scenario: Consider an e-commerce order processing system with three services:

- Order Service: Creates an order.
- Payment Service: Processes the payment.
- Inventory Service: Updates inventory levels.

Normal Flow:

- Step 1: Order Service creates an order.
- Step 2: Payment Service processes the payment.
- Step 3: Inventory Service updates the stock.

If the Payment Service fails after the order is created, a compensating transaction is triggered:

Compensating Action: The Order Service cancels the order to undo the initial transaction.

## Real world use cases

- E-Commerce: Managing order processing where multiple services (order creation, payment processing, inventory management) work together, and a failure in one step triggers compensating actions.

- Financial Transactions: Handling multi-step financial processes where each step needs to be rolled back in case of failure.

- Travel Booking Systems: Coordinating reservations across flights, hotels, and car rentals where a failure in one service should cancel the entire booking process.
