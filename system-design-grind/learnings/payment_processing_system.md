# Payment Processing System — Complete End-to-End Breakdown

## Part 1: The Players

```
┌──────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────┐
│ Customer │    │   Merchant   │    │ Payment Gateway  │    │   Bank   │
│ (buyer)  │    │  (seller)    │    │  (Stripe/You)    │    │ (issuer/ │
│          │    │              │    │                  │    │ acquirer)│
└──────────┘    └──────────────┘    └─────────────────┘    └──────────┘
```

- **Customer**: person buying something, has a credit/debit card
- **Merchant**: business selling something, has an account with you
- **Payment Gateway (you/Stripe)**: sits between merchant and banks, orchestrates money movement
- **Issuing Bank**: customer's bank (issued the credit card)
- **Acquiring Bank**: merchant's bank (receives the money)
- **Card Network**: Visa/Mastercard — routes communication between issuing and acquiring banks

---

## Part 2: The Full Payment Flow

### Phase 1: Checkout & Tokenization

```
Customer enters card details on merchant's website
         │
         ▼
┌─────────────────────────────────┐
│ Merchant's Frontend (browser)   │
│ Card: 4242-4242-4242-4242       │
│ Expiry: 12/27, CVV: 123        │
└────────────┬────────────────────┘
             │
             │ HTTPS (direct to payment gateway, NOT to merchant server)
             ▼
┌─────────────────────────────────┐
│ Payment Gateway (Stripe)        │
│ Tokenize: card → tok_abc123    │
│ Return token to frontend        │
└─────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Merchant's Frontend             │
│ Sends token (tok_abc123) to     │
│ merchant's backend server       │
└─────────────────────────────────┘
```

**Why tokenization?**
The merchant's server never sees raw card numbers. This is a PCI-DSS compliance requirement. The raw card data goes directly from the browser to the payment gateway (Stripe). The merchant only handles a token — a reference that means nothing if stolen.

### Phase 2: Create Payment Intent

```
Merchant Backend → Payment Gateway API:

POST /v1/payment_intents
Headers:
  Authorization: Bearer sk_live_merchant_key
  Idempotency-Key: order_12345_attempt_1
Body:
  {
    "amount": 5000,           // $50.00 in cents
    "currency": "usd",
    "payment_method": "tok_abc123",
    "customer": "cus_xyz",
    "capture_method": "automatic",  // or "manual" for auth-then-capture
    "metadata": {
      "order_id": "order_12345"
    }
  }

Response:
  {
    "id": "pi_abc123",
    "status": "requires_confirmation",
    "amount": 5000,
    "currency": "usd"
  }
```

At this point, no money has moved. The payment intent is created and stored in the gateway's database.

### Phase 3: Confirm & Authorize

```
Merchant Backend → Payment Gateway:

POST /v1/payment_intents/pi_abc123/confirm
```

```
Payment Gateway                    Card Network              Issuing Bank
      │                               │                          │
      ├── Authorization Request ──────►│                          │
      │   "Can customer X pay $50?"   ├── Forward ──────────────►│
      │                               │                          │
      │                               │                          ├─ Check:
      │                               │                          │  - Card valid?
      │                               │                          │  - Sufficient funds?
      │                               │                          │  - Fraud check?
      │                               │                          │  - 3DS required?
      │                               │                          │
      │                               │◄── Auth Response ────────┤
      │◄── Auth Response ─────────────┤   "Approved, auth_code=AUTH123"
      │                               │   (funds are HELD, not yet moved)
      │
      ├── Update DB: payment status = "authorized"
      ├── Hold $50 on customer's card (reserved, not charged)
```

**Authorization hold**: the $50 is reserved on the customer's card. They can't spend it elsewhere. But the money hasn't actually moved yet. This is why you see "pending" charges on your credit card statement.

### Phase 4: Capture (Money Actually Moves)

```
If capture_method = "automatic":
  → Capture happens immediately after authorization

If capture_method = "manual":
  → Merchant explicitly calls capture later
  → Common for: hotels (charge at checkout), e-commerce (charge at shipment)

POST /v1/payment_intents/pi_abc123/capture
Body: { "amount": 5000 }  // can capture less than authorized (partial capture)
```

```
Payment Gateway                    Card Network              Issuing Bank
      │                               │                          │
      ├── Capture Request ────────────►│                          │
      │   "Capture $50, auth=AUTH123" ├── Forward ──────────────►│
      │                               │                          │
      │                               │                          ├─ Move $50 from
      │                               │                          │  customer's account
      │                               │                          │  to settlement queue
      │                               │◄── Capture Confirmed ───┤
      │◄── Capture Confirmed ─────────┤
      │
      ├── Update DB: payment status = "captured"
      ├── Update ledger: debit customer $50, credit merchant $50
```

### Phase 5: Settlement (Money Reaches Merchant)

Settlement doesn't happen in real-time. It's a batch process:

```
End of day (or next business day):

Payment Gateway aggregates all captured payments for each merchant:
  Merchant ABC:
    - Payment 1: $50.00
    - Payment 2: $30.00
    - Payment 3: $120.00
    - Subtotal: $200.00
    - Platform fee (2.9% + $0.30 per tx): $6.70
    - Net payout: $193.30

Payment Gateway → Acquiring Bank:
  "Transfer $193.30 to Merchant ABC's bank account"

Acquiring Bank → Merchant's Bank Account:
  ACH/wire transfer: $193.30
  (takes 1-2 business days)
```

```
Timeline:
  T+0 seconds:    Customer pays $50 (authorized + captured)
  T+0 to T+24h:   Payment sits in settlement queue
  T+1 day:         Batch settlement runs, initiates transfer
  T+2-3 days:      Money arrives in merchant's bank account
```

---

## Part 3: The Payment State Machine

```
                    ┌──────────────┐
                    │   CREATED    │  Payment intent created
                    └──────┬───────┘
                           │ confirm
                           ▼
                    ┌──────────────┐
              ┌─────│ REQUIRES_    │  3DS/SCA needed?
              │     │ ACTION       │──────────────┐
              │     └──────────────┘              │
              │ no                          yes   │ customer completes 3DS
              ▼                                   ▼
       ┌──────────────┐                   ┌──────────────┐
       │ AUTHORIZED   │◄──────────────────│ 3DS_COMPLETE │
       └──────┬───────┘                   └──────────────┘
              │
       ┌──────┴──────────┐
       │                 │
  auto-capture      manual capture
       │                 │
       ▼                 ▼ (merchant calls capture later)
┌──────────────┐  ┌──────────────┐
│  CAPTURED    │  │  AUTHORIZED  │──── expires after 7 days
└──────┬───────┘  │  (waiting)   │     (auth void, funds released)
       │          └──────────────┘
       ▼
┌──────────────┐
│   SETTLED    │  Money transferred to merchant
└──────┬───────┘
       │
       ▼ (optional)
┌──────────────┐
│  REFUNDED    │  Full or partial refund
└──────────────┘

At any point:
┌──────────────┐
│   FAILED     │  Bank declined, fraud detected, insufficient funds
└──────────────┘
┌──────────────┐
│  CANCELLED   │  Merchant cancelled before capture
└──────────────┘
```

---

## Part 4: Idempotency — The Complete Mechanism

### Why It's Critical

```
Customer clicks "Pay $50"
  → Request sent to gateway
  → Network timeout (no response)
  → Customer clicks "Pay $50" again
  → Without idempotency: customer charged $100
```

### The Full Flow

```
Request 1: POST /payments  Idempotency-Key: "order_123_v1"

┌─────────────────────────────────────────────────┐
│ Payment Gateway receives request                 │
│                                                  │
│ 1. Check idempotency store:                     │
│    SELECT * FROM idempotency_keys               │
│    WHERE key = 'order_123_v1'                   │
│    → Not found                                   │
│                                                  │
│ 2. Insert idempotency record atomically:        │
│    INSERT INTO idempotency_keys                 │
│    (key, status, created_at)                    │
│    VALUES ('order_123_v1', 'processing', now()) │
│    → Success (unique constraint holds)           │
│                                                  │
│ 3. Process payment (authorize, capture)          │
│    → Success: payment_id = pi_abc123             │
│                                                  │
│ 4. Update idempotency record:                   │
│    UPDATE idempotency_keys                      │
│    SET status = 'completed',                    │
│        response = '{"id":"pi_abc123",...}'       │
│    WHERE key = 'order_123_v1'                   │
│                                                  │
│ 5. Return response to client                    │
└─────────────────────────────────────────────────┘
```

```
Request 2 (retry): POST /payments  Idempotency-Key: "order_123_v1"

┌─────────────────────────────────────────────────┐
│ Payment Gateway receives request                 │
│                                                  │
│ 1. Check idempotency store:                     │
│    SELECT * FROM idempotency_keys               │
│    WHERE key = 'order_123_v1'                   │
│    → Found! status = 'completed'                │
│                                                  │
│ 2. Return stored response immediately           │
│    → {"id":"pi_abc123",...}                      │
│    → No second charge. Customer safe.            │
└─────────────────────────────────────────────────┘
```

```
Request 2 (retry while Request 1 still processing):

┌─────────────────────────────────────────────────┐
│ Payment Gateway receives request                 │
│                                                  │
│ 1. Check idempotency store:                     │
│    → Found! status = 'processing'               │
│                                                  │
│ 2. Return 409 Conflict                          │
│    "Payment is being processed, retry later"     │
└─────────────────────────────────────────────────┘
```

### Idempotency Key Lifecycle

```
Key created:     on first request
Key TTL:         24-72 hours (after which client must use a new key)
Key storage:     same DB as payments (or Redis for speed + DB for durability)
Key generation:  client-side (deterministic from order context is best)
                 e.g., hash(merchant_id + order_id + amount)
```

---

## Part 5: Webhooks — Asynchronous Notifications

### Why Webhooks?

Payment processing involves asynchronous steps (bank authorization takes time, 3DS requires customer action, settlement happens hours later). The merchant needs to know when things happen without polling.

### The Flow

```
Merchant registers webhook URL:
  https://merchant.com/stripe-webhooks

Payment Gateway sends POST requests to this URL when events happen:
```

```
Event: payment_intent.authorized
  POST https://merchant.com/stripe-webhooks
  Headers:
    Stripe-Signature: t=1234,v1=sha256_signature
  Body:
    {
      "id": "evt_001",
      "type": "payment_intent.authorized",
      "data": {
        "object": {
          "id": "pi_abc123",
          "status": "authorized",
          "amount": 5000
        }
      }
    }

Event: payment_intent.captured
  POST https://merchant.com/stripe-webhooks
  Body:
    {
      "type": "payment_intent.captured",
      "data": { ... }
    }

Event: payment_intent.payment_failed
  POST https://merchant.com/stripe-webhooks
  Body:
    {
      "type": "payment_intent.payment_failed",
      "data": {
        "object": {
          "id": "pi_abc123",
          "last_payment_error": {
            "code": "card_declined",
            "message": "Insufficient funds"
          }
        }
      }
    }
```

### Webhook Reliability

Webhooks are HTTP calls — they can fail. The payment gateway must handle this:

```
Delivery attempt 1: POST to merchant → timeout
Delivery attempt 2: retry after 1 minute → 500 error
Delivery attempt 3: retry after 5 minutes → 500 error
Delivery attempt 4: retry after 30 minutes → 200 OK ✓

Retry schedule (exponential backoff):
  1min, 5min, 30min, 2hr, 12hr, 24hr, 48hr
  After all retries exhausted: mark as failed, alert merchant
```

### Webhook Security

The merchant must verify that the webhook actually came from the payment gateway (not an attacker):

```
Payment Gateway:
  1. Compute signature: HMAC-SHA256(webhook_secret, timestamp + "." + body)
  2. Send in header: Stripe-Signature: t=timestamp,v1=signature

Merchant's webhook handler:
  1. Extract timestamp and signature from header
  2. Recompute: HMAC-SHA256(my_webhook_secret, timestamp + "." + raw_body)
  3. Compare signatures → match? Authentic. Mismatch? Reject.
  4. Check timestamp → within 5 minutes? Accept. Old? Reject (replay attack).
```

### Webhook Idempotency (Merchant Side)

The merchant may receive the same webhook twice (retry after network issue). The merchant must handle this:

```
Merchant webhook handler:
  1. Parse event_id from body ("evt_001")
  2. Check: "Have I processed evt_001 before?"
     → Yes: return 200 immediately (don't process again)
     → No: process event, store evt_001, return 200
```

---

## Part 6: The Ledger — Append-Only Financial Record

### Double-Entry Bookkeeping

Every money movement creates two entries that sum to zero:

```
Payment of $50 from Customer to Merchant:

┌─────────────────────────────────────────────────────┐
│ Ledger Entry 1:                                      │
│   account: customer_cus_xyz                         │
│   type: DEBIT                                        │
│   amount: -5000  ($50.00)                           │
│   payment_id: pi_abc123                             │
│   bank_txn_id: txn_bank_456                         │
│   created_at: 2024-01-15 10:30:00                   │
├─────────────────────────────────────────────────────┤
│ Ledger Entry 2:                                      │
│   account: merchant_acct_abc                        │
│   type: CREDIT                                       │
│   amount: +5000  ($50.00)                           │
│   payment_id: pi_abc123                             │
│   bank_txn_id: txn_bank_456                         │
│   created_at: 2024-01-15 10:30:00                   │
└─────────────────────────────────────────────────────┘

Sum of all entries for this payment: -5000 + 5000 = 0 ✓
Sum of ALL entries in the entire ledger must always = 0
```

**With platform fees:**

```
Customer pays $50 for a product:

Entry 1: Customer account       DEBIT   -$50.00
Entry 2: Merchant account       CREDIT  +$48.25
Entry 3: Platform fee account   CREDIT  +$1.75  (2.9% + $0.30)

Sum: -50.00 + 48.25 + 1.75 = 0 ✓
```

### Why Append-Only?

- **Auditability**: every transaction ever recorded is preserved. Regulators can audit.
- **No silent changes**: you never UPDATE or DELETE a ledger entry. To reverse a charge, you ADD a new reversal entry.
- **Reconciliation**: you can replay the entire ledger and verify balances at any point in time.

```
Refund of $50:

Entry 4: Customer account       CREDIT  +$50.00  (money back)
Entry 5: Merchant account       DEBIT   -$48.25  (amount returned)
Entry 6: Platform fee account   DEBIT   -$1.75   (fee returned)

Sum of entries 4-6: +50.00 - 48.25 - 1.75 = 0 ✓
Total sum of all 6 entries: 0 ✓

Customer net: -50 + 50 = $0 (fully refunded)
Merchant net: +48.25 - 48.25 = $0
Platform net: +1.75 - 1.75 = $0
```

---

## Part 7: The Complete Architecture

```
                          ┌─────────────────────┐
                          │   Merchant's App     │
                          │   (e-commerce site)  │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              Tokenize card    API calls         Webhooks
              (browser→GW)    (server→GW)      (GW→server)
                    │                │                │
                    ▼                ▼                │
              ┌──────────────────────────────────┐   │
              │        API Gateway / LB          │   │
              │   (rate limiting, auth, routing)  │   │
              └──────────────┬───────────────────┘   │
                             │                        │
                    ┌────────┴────────┐               │
                    ▼                 ▼               │
            ┌──────────────┐  ┌──────────────┐       │
            │Payment Service│  │Payment Service│       │
            │  (instance 1) │  │  (instance 2) │       │
            └──────┬───────┘  └──────┬───────┘       │
                   │                  │               │
         ┌─────────┴──────────────────┘               │
         │                                            │
         ▼                                            │
┌─────────────────┐                                   │
│   PostgreSQL    │  ← Payments DB                    │
│   (primary)     │    - payments table               │
│                 │    - idempotency_keys table        │
│                 │    - ledger_entries table           │
├─────────────────┤                                   │
│   PostgreSQL    │  ← Read replica                   │
│   (replica)     │    (for list_payments queries)     │
└─────────────────┘                                   │
         │                                            │
         ▼                                            │
┌─────────────────┐                                   │
│  Saga           │  ← Payment Orchestrator            │
│  Orchestrator   │    Manages: auth → capture →       │
│                 │    settle → notify                  │
└────────┬────────┘                                   │
         │                                            │
         ▼                                            │
┌─────────────────┐    ┌─────────────────┐            │
│  Card Network   │    │  Webhook Service │────────────┘
│  Gateway        │    │  (sends events   │
│  (Visa/MC API)  │    │   to merchants)  │
└─────────────────┘    └────────┬────────┘
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
                ┌──────────┐     ┌──────────┐
                │  Kafka   │     │  Redis   │
                │ (events) │     │ (retry   │
                │          │     │  queue)  │
                └──────────┘     └──────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| API Gateway | Auth, rate limiting, routing |
| Payment Service | Stateless API handlers, idempotency check |
| PostgreSQL | Payments, ledger, idempotency keys |
| Saga Orchestrator | Multi-step payment flow, compensation |
| Card Network GW | Talk to Visa/MC for auth/capture |
| Webhook Service | Deliver events to merchants, retry |
| Kafka | Event bus (payment.created, captured...) |
| Redis | Rate limiting, caching, webhook retries |
| Reconciliation Job | Daily batch: compare ledger vs bank |

---

## Part 8: Reconciliation — End of Day

```
Daily reconciliation job (runs at 2 AM):

┌────────────────────────────────────────────────────────────┐
│ Input 1: Our ledger (all captured payments for the day)    │
│   pi_001: $50.00, bank_txn: txn_101                      │
│   pi_002: $30.00, bank_txn: txn_102                      │
│   pi_003: $75.00, bank_txn: txn_103                      │
│   Total: $155.00                                           │
├────────────────────────────────────────────────────────────┤
│ Input 2: Bank settlement report (CSV/API from bank)       │
│   txn_101: $50.00  ✓ match                                │
│   txn_102: $29.70  ✗ amount mismatch ($0.30 difference)   │
│   txn_104: $20.00  ✗ in bank but not in our ledger        │
│   (txn_103 missing from bank report)                       │
│   Total: $99.70                                            │
├────────────────────────────────────────────────────────────┤
│ Output: Reconciliation report                              │
│                                                            │
│ MATCHED:     1 transaction ($50.00)                        │
│ MISMATCHED:  1 transaction (txn_102: we say $30, bank $29.70)│
│ MISSING:     1 transaction (txn_103: in our ledger, not bank)│
│ UNEXPECTED:  1 transaction (txn_104: in bank, not our ledger)│
│ DISCREPANCY: $55.30                                        │
│                                                            │
│ Actions:                                                   │
│   txn_102: likely currency conversion → auto-resolve       │
│   txn_103: likely settles tomorrow → re-check next day     │
│   txn_104: ALERT → manual investigation                    │
└────────────────────────────────────────────────────────────┘
```

---

## Part 9: Key Interview Talking Points

When asked to design a payment system, hit these in order:

1. **TOKENIZATION**: Card data never touches merchant servers. Tokenized in the browser, PCI compliant.

2. **IDEMPOTENCY**: Every payment request carries an idempotency key. Atomic insert with unique constraint. Retries return stored result. In-flight duplicates get 409.

3. **STATE MACHINE**: Payment moves through CREATED → AUTHORIZED → CAPTURED → SETTLED. Each transition is atomic. Saga orchestrator handles multi-step flow with compensating actions on failure.

4. **CONSISTENCY**: CP over AP. During DB failover, reject payments rather than risk double-charges. Client retries safely with idempotency key.

5. **LEDGER**: Append-only, double-entry bookkeeping. Every transaction has debit + credit summing to zero. Never update or delete entries.

6. **WEBHOOKS**: Async notification to merchants. Signed with HMAC-SHA256. Exponential retry. Merchant must handle idempotently.

7. **RECONCILIATION**: Daily batch job matches our ledger against bank reports. Categorizes discrepancies. Most resolve automatically (timing). Exceptions alert humans.
