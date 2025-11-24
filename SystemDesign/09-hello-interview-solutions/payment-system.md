# Payment System

## 📸 What is Stripe?
Payment processing systems like Stripe allow business (referred to throughout this breakdown as merchants) to accept payment from customers, without having to build their own payment processing infrastructure. Customer input their payment details on the merchant's website, and the merchant sends the payment details to Stripe. Stripe then processes the payment and returns the result to the merchant.

## Functional Requirements

Core requirements

- Merchants should be able to initiate payment requests (Charge a customer for a specific amount)
- Users should be able to pay for products with credit/debit cards
- Merchants should be able to view status updates for payments (e.g., pending, success, failed).

Below the line (out of scope):

- Customers should be able to save payment methods for future use.
- Merchants should be able to issue full or partial refunds.
- Merchants should be able to view transaction history and reports.
- Support for alternative payment methods (e.g., bank transfers, digital wallets).
- Handling recurring payments (subscriptions).
- Payouts to merchants.

## Non Functional Requirements

Core requirements

- The system should be highly secure
- The system should guarantee durability and auditability with no transaction data ever being lost, even in case of failures.
- The system should guarantee transaction safety and financial integrity despite the inherently asynchronous nature of external payment networks
- The system should be scalable to handle high transaction volume (10,000+ TPS) and potentially bursty traffic patterns (e.g., holiday sales).

Below the line (out of scope):
The system should adhere to various financial regulations globally (depending on supported regions).
The system should be extensible to easily add new payment methods or features later.

## Core Entities

- Merchant: This entity will store information about the businesses using our payment platform, including their identity details, bank account information, and API keys.

- PaymentIntent: This represents the merchant's intention to collect a specific amount from a customer and tracks the overall payment lifecycle from creation to completion. It owns the state machine from created → authorized → captured / canceled / refunded, and enforces idempotency for retries.

- Transaction: This represents a polymorphic money-movement record linked back to one PaymentIntent. Types include Charge (funds in), Refund (funds out), Dispute (potential reversal), and Payout (merchant withdrawal). Each row carries amount, currency, status, timestamps, and references to both the intent and the merchant. For simplicity, we'll only be focused on Charges as everything else is out of scope.

It's important to clarify the distinction between PaymentIntent and Transaction at this point as this can easily cause confusion. The relationship between them is one-to-many: a single PaymentIntent can have multiple Transactions associated with it. For example:

- If a payment attempt fails due to insufficient funds, the merchant might retry with the same PaymentIntent ID but a different Transaction will be created.
- For partial payments, multiple Transactions might be linked to the same PaymentIntent.
- For refunds, a new Transaction with a negative amount would be created and linked to the original PaymentIntent.

## API or System Interface

The API is the main way merchants will interact with our payment system. Defining it early helps us structure the rest of our design. We'll start simple and, as always, we can add more detail as we go. I'll just create one endpoint for each of our core requirements.

First, merchants need to initiate PaymentIntent requests. This will happen when a customer reaches the checkout page of a merchant's website. We'll use a POST request to create the PaymentIntent.

```json
POST /payment-intents -> paymentIntentId
{
  "amountInCents": 2499,
  "currency": "usd",
  "description": "Order#1234",
}
```

Next, the system needs to securely accept and process payments. Since we're focusing on credit/debit cards initially, we'll need an endpoint for that:

```json
POST /payment-intents/{paymentIntentId}/transactions
{
  "type": "charge",
  "card": {
    "number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }
}
```

**In a real implementation, we'd never pass raw card details directly to our backend like this. We'd use a secure tokenization process to protect sensitive data. We'll get into the details of how we handle this securely when we get further into our design. In your interview, I would just callout that you understand this data will need to be encrypted.**

Finally, merchants need to check the status of payments. This can be done with a simple GET request like so:

```json
GET /payment-intents/{paymentIntentId} -> PaymentIntent
```

For a more real-time approach (and one that actually mirrors the industry standard), we could also provide webhooks that notify merchants when payment statuses change. In this way, the merchant would provide us with a callback URL that we would POST to when the payment status changes, allowing them to get real-time updates on the status of their payments.

```json
POST {merchant_webhook_url}
{
  "type": "payment.succeeded",
  "data": {
    "paymentId": "pay_123",
    "amountInCents": 2499,
    "currency": "usd",
    "status": "succeeded"
  }
}
```

Designing a webhook callback system is often a standalone question in system design interviews. Designing a payment system, complete with webhooks, would be a lot to complete in the time allotted. Have a discussing with your interviewer early on so you're on the same page about what you're building.

## High Level Design

For our high-level design, we're simply going to work one-by-one through our functional requirements.

### Merchants should be able to initiate payment requests

When a merchant wants to charge a customer, they need to initiate a payment request. In our system, this is accomplished through the creation of a PaymentIntent. As we stated in our Core Entities, a PaymentIntent represents the merchant's intention to collect a specific amount from a customer and tracks the lifecycle of the payment from initiation to completion.

Let's start by laying out the core components needed for this functionality:

- API Gateway: This serves as the entry point for all merchant requests. It handles authentication, rate limiting, and routes requests to the appropriate microservices.

- Payment Service: This microservice is responsible for creating and managing PaymentIntents. It interfaces with our database to store payment information.

- Database: A central database that stores all system data including PaymentIntents records (with their current status, amount, currency, and associated metadata) and merchant information (API keys, business details, and configuration preferences).

Here's the flow when a merchant initiates a payment:

- The merchant makes an API call to our system by sending a POST request to /payment-intents with details like amount, currency, and description.
- Once authenticated, the request is routed to the PaymentIntent Service (more on this later).
- The PaymentIntent Service creates a new PaymentIntent record with an initial status of "created" and stores it in the Database.
- The system generates a unique identifier for this PaymentIntent and returns it to the merchant in the API response.

This PaymentIntent ID is crucial as it will be used in subsequent steps of the payment flow. The merchant will typically embed this ID in their checkout page or pass it to their client-side code where it will be used when collecting the customer's payment details.

At this stage, no actual charging has occurred. We've simply recorded the merchant's intention to collect a payment and created a reference that will be used to track this payment throughout its lifecycle. The PaymentIntent exists in a "created" state, awaiting the next step where payment details will be provided and processing will begin.

### Users should be able to pay for products with credit/debit cards.

Now that we have a PaymentIntent created, the next step is to securely collect payment details from the customer and process the payment. It's important to understand that payment processing is inherently asynchronous - the initial authorization response from the payment network is just the first step in a longer process that can take minutes or even days to fully complete. This is because payment networks need time to handle things like fraud checks, chargeback requests, etc.

Our system needs to handle this asynchronous nature by maintaining the state of each payment and transaction, and keeping merchants informed of status changes throughout the entire lifecycle.
Let's expand our architecture to handle this critical part of the payment flow:

- Transaction Service: A dedicated microservice responsible for receiving card details from the merchant server, managing transaction records throughout the payment lifecycle, and interfacing directly with external payment networks like Visa, Mastercard, and banking systems.

- External Payment Network: This is external to our actual system, though a crucial part of the payment flow. These are the payment networks (Visa, Mastercard, etc.) and banking systems that actually authorize and process the financial transactions.

Here's how the flow works when a customer enters their payment details:

- The customer enters their credit card information into a payment form on the merchant's website.
- The merchant collects this data and sends it to our Transaction Service along with the original PaymentIntent ID.
- The Transaction Service creates a transaction record with status "pending" in our system.
- The Transaction Service directly handles the payment network interaction: a. Connects to the appropriate payment network and sends the authorization request b. Receives the initial response (approval/decline) c. Updates the transaction record with the initial status d. Continues to listen for callbacks from the payment network over the secure private connection e. When additional status changes occur (settlement, chargeback, etc.), receives callbacks and updates records accordingly
- The Transaction Service updates the PaymentIntent status as the transaction progresses through its lifecycle.

This simplified architecture keeps the Transaction Service as the single point of responsibility for both managing our internal transaction records and interfacing with external payment networks. While this combines multiple concerns in one service, it reduces complexity and eliminates unnecessary network hops while still maintaining security through proper PCI compliance within the service.

### The system should provide status updates for payments

After a payment is initiated and processed, merchants need a reliable way to determine its current status. This information is very important for business operations! Merchants need to know when a payment succeeds to trigger fulfillment actions like shipping physical products, granting access to digital content, or confirming reservations. Likewise, they need to know when payments fail so they can notify customers or attempt alternative payment methods.

Let's see how our existing architecture supports this functionality:

Since we already have a PaymentIntent Service that manages PaymentIntents, we can leverage this same service to provide status updates to merchants. There's no need to create a separate service just for checking statuses.

Here's how the flow works when a merchant checks a payment's status:

- The merchant makes a GET request to /payment-intents/{paymentIntentId} to retrieve the current status of a specific PaymentIntent.
- The API Gateway validates the merchant's authenticity and routes the request to the PaymentIntent Service.
- The PaymentIntent Service queries the database for the current state of the PaymentIntent, including its status, any error messages (if failed), and related transaction details.
- The service returns this information to the merchant in a structured response format.

This simple polling mechanism allows merchants to programmatically check payment statuses and integrate the results into their business workflows.
The PaymentIntent can have various statuses throughout its lifecycle, such as:

- created: Initial state after the merchant creates the PaymentIntent
- processing: PaymentIntent details received and being processed
- succeeded: PaymentIntent successfully processed
- failed: Payment processing failed (with reason)

While this polling approach works well for many use cases, it's not ideal for real-time updates or high-frequency status checks. In a deep dive later, we'll explore how webhooks can be implemented to provide push-based notifications that eliminate the need for polling and reduce latency between payment completion and fulfillment actions.

## Deep Dives

At this point, we have a basic system that satisfies the core functional requirements of our payment processing system. Merchants can initiate payments by creating a PaymentIntent, customers can pay with credit/debit cards, and merchants can view payment status updates. However, our current design has significant limitations, particularly around transaction safety, durability, and scaling to handle high volumes. Let's look back at our non-functional requirements and explore how we can improve our system to handle 10,000+ TPS with strong consistency and guaranteed durability.

### The system should be highly secure

Let's start with security. For a payment processing system, there are two main things we care about when it comes to guaranteeing the security of the system.

- Is the person/merchant making the payment request who they say they are?
- Are we protecting customer personal information so that it can't be stolen or compromised?

Starting with #1, we need to validate that merchants connecting to our system are who they claim to be. After all, we're giving them the ability to charge people money, we better make sure they're legit! Most payment systems solve this with API keys, but there are different approaches with varying levels of security. Here are some options.

#### Basic API key authentication

We can use standard, static API keys as the primary authentication mechanism for merchants. When a merchant onboards to our payment platform, we generate a unique API key (typically a random string like pk_live_51NzQRtGswQnXYZ8o) and store it in our database associated with the merchant's account. For each API request, merchants include this key in the request headers, typically as Authorization: Bearer {api_key} or a custom header like X-API-Key: {api_key}. When our API Gateway receives a request, it extracts the API key, looks it up in the database, and identifies the corresponding merchant. If the key is valid, the request is authenticated and processed.

#### Enhanced API key management with request signing

To improve on the good solution, we can implement request signing which ensures that API requests are authentic, unmodified, and cannot be replayed by attackers. We can accomplish this with a combination of public API keys like before (to identify the merchant) and private secret keys (used to generate time bound signatures).

During merchant onboarding, we provide two keys: a public API key for identification and a private secret key stored securely on the merchant's server (never in client-side code). These keys are used for authenticating the merchant's server with our payment system, which is separate from how we handle customer card data (covered in the next section).

For each API request, the merchant's server generates a digital signature by hashing the request details (method, endpoint, parameters, body) along with a timestamp and a unique nonce using their secret key. This signature proves the request's authenticity and prevents tampering. This way, even if replayed, we'd know that the timestamp was outside our acceptable window or that the nonce was already used, allowing us to reject the request.

When our API Gateway receives a request, it:

- Retrieves the merchant's secret key based on the provided API key
- Recreates the HMAC signature using the same algorithm (SHA-256), secret key, and request data
- Compares the calculated signature with the one provided in the request headers
- Validates that the timestamp is within an acceptable time window (typically 5-15 minutes)
- Ensures the nonce hasn't been used before within the valid time window by checking the cache/DB

Now let's look at #2 - protecting sensitive customer data throughout the payment process. Allowing a bad actor to get a hold of someone else's credit card information can lead to fraud, identity theft, and a total loss of customer trust. Plus, there are strict regulations like PCI DSS that mandate how payment data must be handled.

### The system should guarantee durability and auditability with no transaction data ever being lost, even in case of failures.

For a payment system, the worst thing you can do is lose transaction data. It would be both a financial and legal disaster. Every transaction represents real money moving between accounts, and regulations like PCI-DSS, SOX compliance, and financial auditing standards require us to maintain complete, immutable records of every payment attempt, success, and failure.
We need to track not just what the current state is, but the entire sequence of events that led to that state. When a customer disputes a charge six months later, we must be able to prove exactly what happened: when the payment was initiated, what amount was authorized, when it was captured, and whether any refunds were processed. A single missing record could mean inability to defend against chargebacks, failed compliance audits, or worse—being unable to determine the true state of customer accounts.

#### Database + Change data capture + Event Streams

A more robust approach, used by payment processors like Stripe, separates operational and audit concerns while guaranteeing consistency between them. We still use a traditional database for merchant-facing operations, but audit durability comes from an immutable event stream populated via Change Data Capture (CDC).

Here's how it works:

- Operational Database: Handles merchant API requests with optimized tables for current state queries. No audit tables needed—just pure operational data models.
- Change Data Capture: Monitors the database's write-ahead log (WAL) or oplog, capturing every committed change as an event. This happens at the database level, not application level, guaranteeing we never miss changes.
- Immutable Event Stream: CDC publishes all changes to Kafka, creating an append-only log of every state transition. Events are keyed by payment_intent_id and include the full before/after state.
- Specialized Consumers: Different services consume the event stream for their specific needs without impacting the operational database.

The nice part about this architecture is that different consumers can materialize different views:

- Audit Service: Maintains a complete, immutable history optimized for compliance queries
- Analytics: Builds denormalized views for business intelligence
- Reconciliation: Correlates our events with external payment network events
- Webhook Delivery: Tracks which state changes need merchant notification

For durability, Kafka provides configurable replication (typically 3x) across multiple brokers and availability zones. Events are retained for a configurable period (often 7-30 days) on disk, with older events archived to object storage for permanent retention. All events are automatically flushed to S3 for long-term auditability, ensuring we can reconstruct any payment's complete history even years later for compliance audits or dispute resolution. This gives us both hot data for operational use and cold storage for compliance.

This architecture provides the best of both worlds: merchants get sub-10ms API responses from an optimized operational database, while every change is automatically captured in an immutable event stream without impacting API latency. Since CDC operates at the database level, there's no reliance on application code remembering to write audit records—if a change commits to the database, it will appear in the event stream.

**A savvy interviewer might ask: "Isn't CDC a single point of failure? What happens if your CDC system fails and you miss critical payment events?"
This is a great question! CDC is technically a single point of failure - if it stops working, events stop flowing to Kafka even though database writes continue. Companies like Stripe handle this by running multiple independent CDC instances reading from the same database, each writing to different Kafka clusters. They also implement monitoring that alerts within seconds if CDC lag increases, and maintain recovery procedures to replay missed events from database logs if needed. For critical payment events, they might also implement application-level fallbacks that write directly to Kafka if CDC hasn't confirmed the event within a certain timeframe.**

### The system should guarantee transaction safety and financial integrity despite the inherently asynchronous nature of external payment networks

Payment networks operate in a fundamentally different way than our internal systems. When we send a charge request to Visa, Mastercard, or a bank, we're crossing into systems we don't control. These networks process millions of transactions across global infrastructure, with their own retry mechanisms, queue delays, and batch processing windows. A payment we consider "timed out" might still be winding its way through authorization systems, while another might have succeeded instantly but lost its response packet on the way back to us.

This asynchronous reality creates serious risks. The most dangerous is double-charging. A customer clicks "pay" for their $50 purchase, we timeout waiting for the bank's response, the merchant retries, and suddenly the customer sees two $50 charges on their statement. Even if we eventually refund one, we've damaged trust and created support headaches. The opposite risk is equally damaging: a payment succeeds at the bank but we never know it, so we tell the merchant the payment failed. The merchant never ships the product, the customer's card gets charged anyway, and now we have an angry customer who paid for goods they'll never receive.

#### Event driven safety with reconciliation

The most robust approach leverages the CDC and event stream infrastructure we established for durability, treating asynchronous payment networks as first-class citizens in our architecture.

he key insight is to track our intentions before acting on them. Here's how the complete flow works:

- Record the attempt: Before calling any payment network, we write an attempt record to our database with the network name, reference ID, and what we're trying to accomplish. This triggers a CDC event capturing our intention.
- Call the payment network: We send the actual charge request with our configured timeout.
- Handle the response (branching based on outcome):
    - Success: Update the attempt status to "succeeded" in the database, which triggers another CDC event with the successful outcome
    - Timeout: Update the attempt status to "timeout" in the database, triggering a CDC event that the reconciliation service will process
    - Explicit failure: Update the attempt status to "failed" with the failure reason
- Automated reconciliation: A dedicated reconciliation service consumes timeout events and proactively queries the payment network using our recorded reference ID to determine what actually happened.

### How can we expand the design to support Webhooks?

While our polling-based status endpoint works well for basic scenarios, merchants often need real-time updates about payment status changes to trigger business processes like order fulfillment or access provisioning. Webhooks solve this by allowing our system to proactively notify merchants about events as they occur.

Merchants provide us with two additional bits of information:

- Callback Url: This is the URL that we will POST updates to when we have them.
- Subscribed Events: This is a list of events that they want to subscribe to. We will notify them, at the callback url, when any of these events occur.

**You hear real-time updates and you may think websockets or SSE! But no, these are often conflated concepts, but it's important to understand that webhooks represent server-to-server communication, not server-to-client (like websockets or SSE). The payment system's server sends notifications directly to the merchant's server via HTTP requests to a predefined endpoint. This is fundamentally different from client-facing real-time updates (like WebSockets or Server-Sent Events), which would deliver updates from a server to a browser or mobile app. Webhooks are designed for system-to-system communication and typically require the merchant to operate a publicly accessible endpoint to receive these notifications.**

Here's how webhooks would work at a high level in our payment processing system:

- Database Changes: Our Transaction and PaymentIntent services update the operational database as payments progress through their lifecycle (created → authorized → captured, etc.).

- CDC Events: Change Data Capture automatically captures these database changes and publishes them to our Kafka event stream. These CDC events include payment status changes, transaction completions, and other state transitions.

- Webhook Service: We introduce a new Webhook Service that consumes from the same Kafka event stream as our other specialized consumers ie, Reconciliation. When the service receives a CDC event, it checks if the associated merchant has configured a webhook endpoint for that event type. If configured, it prepares the webhook payload with relevant event details, signs the payload with a shared secret to enable verification, and attempts delivery to the merchant's endpoint.

- Delivery Management: For each webhook, the delivery attempt is recorded with its status. If delivery fails, the Webhook Service implements a retry strategy with exponential backoff (e.g., retry after 5s, 25s, 125s, etc., up to a reasonable maximum interval like 1 hour).

- Merchant Implementation: On the merchant side, they would need to configure a publicly accessible HTTPS endpoint to receive webhooks. They must verify the signature of incoming webhooks using the shared secret to ensure authenticity. After verification, they would process the webhook payload and update their systems accordingly with the new information. Finally, they should return a 2xx HTTP status code to acknowledge receipt of the webhook, preventing unnecessary retries.