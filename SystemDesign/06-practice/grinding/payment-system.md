# Payment system

## Problem

We want to design a global payment processing system similar to Stripe. This system allows merchants to accept payments from customers across various methods (Credit Cards, Digital Wallets, etc.) and ensures that funds are eventually settled into the merchant's bank account.

## Answer

We would first list down the requirements for the payment system

### Functional Requirements

- Merchants (or consumers) of our system should be able to register with the system to pass the callback they intend to get invoked.
- Merchants should be able to initiate payment by passing details. For the scope of this system lets assume our system just support payment via Credit/Debit card
- Merchants should be able to track progress of the payment they initiated.
- The system must support idempotent API calls using a unique key from the client to prevent duplicate transactions during network retries.
- Every movement of money must be recorded in an immutable, double-entry ledger.

### Non Functional Requirements

- System should be highly consistent, we cannot afford to charge a customer twice due to failures in the system
- System should be highly secure
- System should be able to process the payment with a latency of < 500 ms.
- Scale: 1 billion transactions per day, which makes it approximately 11,574 transactions per second (TPS) on average. However, we should also consider peak loads, which could be significantly higher than the average. For instance, during holiday seasons or major sales events, the TPS could spike to 100,000 or more.
- Availability: System should be highly available, with an uptime of 99.99% or higher.
- Durability: Once a transaction is processed, it should be stored durably and should not be lost even in the case of system failures.

These are some of the requirements I have come up with. In a real interview, we can always discuss with the interviewer and refine these if needed.

### Data model

After we noted down the requirements, we will next discuss on the data models for the system.

### Merchant

- id
- name
- callback_url
- created_at

### Transaction

- id
- merchant_id
- amount
- currency
- status (pending, completed, failed)
- created_at
- idempotency_key

### LedgerEntry

- id
- transaction_id
- amount
- currency
- account_id (could be customer account or merchant account)
- created_at

We can also have other data models like Customer, Card, etc. but for the scope of this system, we will keep it simple and focus on these three. In an actual interview, we can always discuss with the interviewer and refine these data models if needed.

### API Design

#### Register Merchant

- Endpoint: POST /merchants
- Request Body:
```json
{
  "name": "Merchant Name",
  "callback_url": "https://merchant.com/callback"
}
```
- Response
Status: 201 Created
Body:
```json
{
  "id": "merchant_id",
  "name": "Merchant Name",
  "callback_url": "https://merchant.com/callback",
  "created_at": "2024-06-01T12:00:00Z"
}
```

#### Initiate Payment

- Endpoint: POST /paymentintent
- Request Header:
```json
{
    "Authorization": <JWT>, (The merchant id would be extracted in the backend from the JWT)
    "idempotency_key": <key>
}
```
- Request Body:
```json
{
  "amount": 1000,
  "currency": "USD",
  "card": "token_visa_1234" (In a real system, we would not pass card details directly to our backend. Instead, we would use a tokenization service to generate a token for the card details and pass that token to our backend. This is done for security reasons.)
}
```
- Response
Status: 202 Accepted (This API would be an async one as payment will take some time to be completed)
Body:
```json
{
  "transaction_id": "transaction_id",
  "status": "pending"
}
```

#### Get Payment Status

- Endpoint: GET /paymentintent/{transaction_id}
- Request Header:
```json
{
    "Authorization": <JWT> (The merchant id would be extracted in the backend from the JWT)
}
- Response
Status: 200 OK
Body:
```json
{
  "transaction_id": "transaction_id",
  "status": "completed"
}
```

### Choice of database

For this system, we would need a database that can handle high write throughput and provide strong consistency guarantees. We can use a relational database like PostgreSQL or MySQL for storing the transaction and ledger data. These databases support ACID transactions, which will help us ensure that our financial data is consistent and reliable.

### High level design

Next we will discuss the high level design of the system. We will go flow by flow and first cover happy path and then we will discuss about failure scenarios and how we can handle them.

#### Merchant registration flow

- Client sends a POST request to /merchants endpoint with the merchant details.
- The request is received by the API Gateway, which forwards it to the Merchant Service.
- The Merchant Service validates the request and creates a new merchant record in the database.
- Once the merchant is created, the Merchant Service returns the merchant details in the response.

#### Payment initiation flow


The payment initiation flow is a combination of fast path and slow path.

##### The fast path

- Client sends a POST request to /paymentintent endpoint with the payment details and idempotency key.
- The request is received by the API gateway, which does authentication and authorization checks. It also checks for rate limiting. It extracts the merchant id from the JWT and checks if the merchant is valid.
- If the request is valid, the API gateway forwards the request to the Payment Service.
- If the request is not valid, the API gateway returns an appropriate error response (e.g., 401 Unauthorized)
- The API gateway embeds the merchant_id in the json body along with a request_id (This request_id is used for logging and tracing purposes) and forwards the request to the Payment Service.
- The Payment Service first checks if a transaction with the same idempotency key and request payload already exists in the database. If it does, it returns the existing transaction details in the response. This ensures that if the client retries the request due to a network failure, we do not create duplicate transactions.
- If there is no existing transaction with the same idempotency key, the payment service first validates the card token by calling an external card tokenization service. If the card token is not valid, the payment service returns an error response (e.g., 400 Bad Request).
- If the card token is valid, the system uses an outbox pattern here. The payment service in a single database transaction creates a new transaction record in the database with status "created" and stores the idempotency key and another record in the outbox table with the payment details. The outbox table is used to store messages that need to be processed asynchronously. This outbox pattern is used to ensure that both the transaction record and the message to process the payment are created atomically in the same database transaction. This helps us maintain consistency in our system.
- The payment service then returns the transaction details in the response with status "created" and a `202` Accepted HTTP status code, indicating that the payment is being processed asynchronously.

##### The slow path

- When the outbox table is populated with the payment details, a separate payment processor service gets notified via change data capture (CDC) mechanism.
- The payment processor service reads the payment details from the outbox table and puts the details in a message queue like `kafka` for asynchronous processing. We have chosen `kafka` here because its an append-only commit log which ensures fast writes, it also provides at least once delivery using its consumer offsets and acknowledgment mechanism. This at-least-once delivery is important for us to ensure that we do not miss processing any payment.
- Separate worker processes consume the payment details from the message queue. The workers first update transaction status to `inprogress` and then process the payment by calling the external payment procssors like `Chase`, or `Wells Fargo` etc. The workers pass the payment details and the idempotency key to the external payment processor to ensure that even if there are retries, the external payment processor does not process the same payment multiple times.
- Once the payment is processed, the worker updates the transaction status to `succeeded` or `failed` based on the response from the external payment processor. 
- It also creates a new ledger entry in the database to record the movement of money. The ledger entry is created in the same database transaction as the transaction status update to ensure consistency in our financial data. The ledger entry will have the transaction id, amount, currency and account id (which could be the customer account or the merchant account depending on the direction of money movement). There will be two ledger entries for each transaction, one for the debit from the customer's account and one for the credit to the merchant's account. This is the double-entry ledger system which helps us maintain an immutable record of all financial transactions in our system.
- Finally the worker calls the merchant's callback URL to notify them about the payment status.

#### Get payment status flow

- Client sends a GET request to /paymentintent/{transaction_id} endpoint with the transaction id.
- The request is received by the API gateway, which does authentication and authorization checks. It extracts the merchant id from the JWT and checks if the merchant is valid.
- If the request is valid, the API gateway forwards the request to the Payment Service.
- The Payment Service retrieves the transaction details from the database and returns them in the response.

### Failure scenarios and handling

#### Duplicate payment initiation requests

- If the client sends duplicate payment initiation requests with the same idempotency key, the payment service will check for existing transactions with the same idempotency key and return the existing transaction details in the response. 
- This ensures that we do not create duplicate transactions and charge the customer multiple times. 
- To do the check effectively we check the idempotency key along with the request payload to ensure the same request is being retried and not a different request with the same idempotency key.

#### Worker crashes

- Workers consuming from the message queue, commit the offsets back to the message queue. 
- So incase a worker crashes separate worker process would take over and start reading messages from the last committed offset from the message queue.
- Now in this case, there can be these situations
    - Worker crashes before doing anything for a transaction: In this case its a clean slate, and the new worker can continue as is
    - Worker crashes after updating the transaction status but before calling the external payment processor: In this case the worker calls the external payment processor, passing the payment details and idempotency key.
    - Worker crashes after updating the transaction status and after calling the external payment processor: In this case the new worker has no way of knowing whether the old one had called the external payment processor. So the new worker would call the external payment processor, passing the payment details and idempotency key. The external payment processor would check the idempotency key and if it has already processed the payment with the same idempotency key, it would return the same response as before. This way we can ensure that even in case of worker crashes, we do not end up processing the same payment multiple times.

#### Reconciliation

- We can have a separate reconciliation process that runs periodically (e.g., daily) to reconcile the transactions in our system with the records from the external payment processors.
- This reconciliation process can identify any discrepancies (e.g., transactions that were marked as succeeded in our system but were not successful in the external payment processor) and take appropriate actions (e.g., mark the transaction as failed and notify the merchant).
- The process will take the transaction records from our database and call the external payment processor's API to get the status of those transactions. It will then compare the status in our system with the status from the external payment processor.
- If lets say we find a transaction that is marked as succeeded in our system but is marked as failed in the external payment processor, we can mark that transaction as failed in our system and create a new ledger entry to reverse the previous ledger entry that was created when we marked the transaction as succeeded. We can also notify the merchant about this discrepancy and the action taken.
- These can happen due to various reasons like network issues, bugs in our system, bugs in the external payment processor, etc. So having a reconciliation process helps us ensure the integrity of our financial data and take corrective actions when needed.

### Edge cases

- What if the external payment processor is down? In this case, we can implement a retry mechanism with exponential backoff in the worker process. If the payment processor is down, the worker can retry after some time. We can also have a maximum retry limit after which we mark the transaction as failed and notify the merchant.

- What if the merchant's callback URL is down? In this case, we can implement a retry mechanism in the worker process to retry calling the merchant's callback URL after some time. We can also have a maximum retry limit after which we stop retrying and log the failure for manual investigation.

- What if the external payment processor is slow to respond? In this case, we can set a timeout for the call to the external payment processor. If the processor does not respond within the timeout period, we can mark the transaction as failed and notify the merchant.

### Deep dives

Interviewer: "You mentioned using Kafka for the 'Slow Path' to ensure at-least-once delivery. However, at-least-once delivery means a worker might process the same successful payment twice (e.g., it processes the payment, but crashes before committing the Kafka offset). How exactly does your Ledger and Transaction table handle this 'replay' of a successful event to ensure we don't record the profit twice in our database?"

What is your strategy for making the Worker's database update idempotent?

The worker will be updating the `ledger` and `transaction` table in a single database transaction. It will update the transaction table by using the transaction id and the ledger table by using the transaction id as well. So if the worker processes the same successful payment twice, it will try to update the same transaction record and insert the same ledger entry. We can use unique constraints on the transaction id in the transaction table and ledger table to ensure that if there is an attempt to insert a duplicate record, it will fail with a unique constraint violation error. The worker can catch this error and ignore it, since it means that the payment has already been processed and recorded in the database. This way we can ensure that even if there is a replay of a successful event, we do not end up recording the profit twice in our database.

Another alternative way is to update the transaction status to `succeeded` only if the current status is `inprogress`. This way if there is a replay of a successful event, the worker will try to update the transaction status to `succeeded` but since the current status is already `succeeded`, the update will not happen and we can ensure that we do not end up recording the profit twice in our database. In case of the ledger entry we can have a unique constraint on the transaction id and account id to ensure that we do not insert duplicate ledger entries for the same transaction and account. The worker can catch the unique constraint violation error and ignore it, since it means that the ledger entry has already been created for that transaction and account.
