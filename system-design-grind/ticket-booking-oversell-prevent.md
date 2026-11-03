# Senior SWE System Design Notes: Preventing Double Booking

## 1. Problem statement

One seat remains available, and potentially one million users try to book it concurrently. How do we prevent overselling?

### Requirements

**Functional**

- Users can book a seat.
- A successful booking is confirmed to the user.
- Unavailable seats are rejected.
- If payment is involved, successful payment and booking outcomes must be handled consistently.

**Non-functional**

- No two users can own the same seat.
- Handle concurrent requests, retries, and service failures.
- Support high traffic without overwhelming the database.
- Provide reliable outcomes even when responses time out.

### Core invariant

**For a given seat, at most one active booking can own it.**

Start by stating this invariant. Every design decision should preserve it.

---

## 2. Step 1 — Identify the race condition

Suppose the service does the following:

1. Read the seat status.
2. Check whether it is available.
3. Update it to booked.

Two requests can interleave:

- Request A reads `AVAILABLE`.
- Request B reads `AVAILABLE`.
- Request A books the seat.
- Request B also attempts to book it.

This is a classic check-then-act race condition.

A normal application-level check followed by a write is not sufficient. We need to make the availability check and state transition atomic.

---

## 3. Step 2 — Start with an atomic conditional update

My default solution is to make the database enforce the transition from available to booked.

```sql
UPDATE seats
SET status = 'BOOKED',
    booking_id = :booking_id
WHERE seat_id = :seat_id
  AND status = 'AVAILABLE';
```

Check the number of affected rows:

- `1` row: this request successfully claimed the seat.
- `0` rows: the seat is no longer available.

### Why does this work?

The database coordinates conflicting writes to the same row. In PostgreSQL at `READ COMMITTED`, a competing update waits for the earlier conflicting update to resolve and re-evaluates its `WHERE` condition against the updated row.

Therefore, if the first request commits `BOOKED`, the second request's condition `status = 'AVAILABLE'` no longer matches.

We don't need an application-level mutex or a Redis lock just to protect this single-row transition.

**Interview phrasing:**

"I would use an atomic conditional update at the database, which is the source of truth. The database serializes conflicting writes to the same seat, and the affected-row count tells us whether the claim succeeded. This avoids the race condition inherent in checking availability separately from updating it."

---

## 4. Step 3 — Make the booking and reservation record atomic

A realistic booking may require:

1. Claim the seat.
2. Insert a reservation.
3. Store the idempotency result.

These operations should execute in a single database transaction when they belong to the same database.

```text
BEGIN TRANSACTION

1. Conditionally claim the seat.
2. If zero rows updated, abort.
3. Insert the reservation record.
4. Persist the idempotency record.

COMMIT
```

If any required database operation fails, roll back the transaction. The seat claim must not survive without its corresponding reservation.

Use appropriate unique constraints as an additional integrity safeguard. For example, the data model can enforce that a seat has at most one active reservation.

**Important distinction:**

- Conditional update prevents competing requests from claiming the same seat.
- Transaction ensures related database writes commit or roll back together.
- Unique constraints provide an additional layer of data integrity.

---

## 5. Step 4 — Handle one million concurrent users

The database-level conditional update protects correctness, but it does not make one million requests cheap.

All requests targeting the same seat contend on the same database row. This is a hot-row bottleneck.

I would separate the design into two concerns.

### Correctness layer

The authoritative database decides who owns the seat. No request may confirm ownership without successfully claiming it.

### Traffic-management layer

Reduce unnecessary work reaching the database:

- Apply rate limiting and admission control.
- Place excess requests in a durable queue if the product supports waiting.
- Use bounded worker concurrency.
- Reject requests quickly when the seat is already unavailable.
- Apply backoff and jitter to appropriate retries.
- Return a clear unavailable or sold-out response once the outcome is known.

A queue can smooth traffic spikes, but it does not itself prevent double booking. Multiple workers can still race unless the database enforces the invariant.

If the product requires first-come-first-served semantics, explicitly define how arrival order is determined. A generic message queue does not automatically guarantee globally fair ordering.

### Architecture

```text
Users
  |
  v
API Gateway / Rate Limiter
  |
  v
Booking Service
  |
  v
Authoritative Database
  |
  +-- Conditional seat claim
  +-- Reservation record
  +-- Idempotency record
```

For a single remaining seat, it is reasonable to let the database serialize the competing claims. Optimize throughput around that invariant rather than weakening it.

---

## 6. Step 5 — Handle client retries with idempotency

Consider this failure:

1. The database commits the booking.
2. The service response gets lost.
3. The client times out and retries.
4. The seat is already booked, so the conditional update affects zero rows.

Without idempotency, the service might incorrectly report that the original booking failed.

### Solution

The client supplies an idempotency key for the logical booking request.

Persist the key with the booking result and enforce uniqueness. Where possible, store it in the same database transaction as the booking.

On retry:

- If the same key already completed, return the original result.
- If the same key is still processing, return a suitable pending response or wait.
- If the key is new, process the request normally.
- If a key is reused with a different request payload, reject it.

Do not rely solely on a Redis cache for booking correctness. The durable database record and business constraints should protect against duplicate bookings even if a cache entry expires or disappears.

---

## 7. Step 6 — Introduce reservation holds when payment is involved

You usually should not hold a database transaction open while calling an external payment provider.

Instead, use a booking lifecycle:

`AVAILABLE → PAYMENT_PENDING → CONFIRMED`

Possible alternative outcomes include `EXPIRED`, `PAYMENT_FAILED`, and `REFUND_PENDING`.

### Suggested flow

1. Atomically claim the seat for a booking with a hold expiry.
2. Insert the reservation and idempotency records.
3. Commit the database transaction.
4. Record a payment intent in a transactional outbox if asynchronous payment processing is needed.
5. A worker processes the payment request using a stable payment idempotency key.
6. Confirm the reservation after payment succeeds and the booking remains eligible for confirmation.

The transactional outbox prevents the database commit and event publication from becoming an unsafe dual write. A durable queue and retries help deliver the payment work, generally with at-least-once processing.

### Handle payment timeouts

A timeout does not prove payment failed.

- Confirmed payment success: attempt to confirm the eligible reservation.
- Definitive payment failure: mark the booking failed and release the seat safely.
- Unknown payment outcome: reconcile with the provider.
- Payment succeeded after the reservation expired and the seat was reassigned: refund or otherwise compensate the customer.

Use idempotency for both payment attempts and refunds.

---

## 8. Step 7 — Make expiry and confirmation race-safe

Suppose the expiry worker and payment worker both read `PAYMENT_PENDING`.

Payment worker:

```sql
UPDATE reservations
SET status = 'CONFIRMED'
WHERE booking_id = :booking_id
  AND status = 'PAYMENT_PENDING';
```

Expiry worker:

```sql
UPDATE reservations
SET status = 'EXPIRED'
WHERE booking_id = :booking_id
  AND status = 'PAYMENT_PENDING';
```

Both compete for the same reservation row. Only one transition can win under the stated database behavior.

But the seat operation must also be coordinated:

- If expiry wins, release the seat in the same transaction, guarded by the reservation or booking ID that currently owns it.
- If confirmation wins, expiry must not release the seat.
- If expiry wins but payment actually succeeded externally, reconciliation must trigger compensation.

The reservation transition and seat release must be atomic together. Otherwise, a delayed expiry worker could release a seat already allocated to another customer.

**Remember:** database transactions protect internal state; they cannot undo external payment operations.

---

## 9. Why not use a mutex or Redis distributed lock?

### In-process mutex

It coordinates threads sharing the same lock within one process. It does not coordinate independent service instances.

### Redis distributed lock

It can coordinate processes across machines, but introduces lease expiry, ownership, stale lock holder, and failure-handling concerns.

For the basic seat-booking problem, neither is necessary for correctness if the database conditional update already enforces the invariant.

Consider distributed locks only when there is a concrete coordination requirement that database transactions do not adequately address. Even then, retain authoritative database constraints.

---

## 10. Follow-ups to prepare

### Correctness and database behavior

1. Why does the conditional update prevent double booking?
2. What happens when two updates run concurrently under PostgreSQL `READ COMMITTED`?
3. Why is a transaction needed when inserting a reservation record?
4. When would you use `SELECT ... FOR UPDATE`?
5. What if a booking spans multiple seats?

### Retries and failures

6. What if the booking commits but the response times out?
7. How do you implement idempotency?
8. What if the payment succeeds but the worker crashes?
9. What if payment outcome is unknown?
10. How do you release an expired reservation safely?

### Scale and distributed systems

11. What changes when one million users compete for one seat?
12. Would you use a queue, Redis, or both?
13. What happens if the database becomes the hot-row bottleneck?
14. How do you prevent stale workers from releasing another customer's seat?
15. How do you guarantee that an outbox event is not lost?

### Data integrity

16. Why add unique constraints if the conditional update already exists?
17. What if the same user submits two different idempotency keys?
18. How would you design the system for multiple seats and partial availability?

---

## 11. A concise interview answer to memorize

"I'd start by defining the invariant: at most one active booking can own a seat.

I'd enforce it at the authoritative database using an atomic conditional update that claims the seat only if it is still available. The affected-row count determines whether the claim succeeded. If booking requires multiple database writes, I'd wrap the seat claim, reservation insertion, and idempotency record in one transaction.

For retries, I'd use a durable idempotency key so a repeated request returns the original outcome rather than creating another booking.

For one million competing users, the conditional update still protects correctness, but the seat row becomes a hot spot. I'd manage load with admission control, rate limiting, and potentially a durable queue, without relying on the queue or Redis lock for correctness.

If payment is involved, I'd use an explicit reservation lifecycle, a transactional outbox for reliable payment work, provider-side idempotency, and reconciliation for unknown outcomes. Reservation expiry and confirmation must be coordinated atomically, and a late successful payment must be compensated if the seat has already been reassigned."

## Final mental model

- **Conditional update:** Who wins the seat?
- **Transaction:** Do related database changes succeed together?
- **Unique constraint:** What additional invalid states can the database forbid?
- **Idempotency:** What happens when the same request is retried?
- **Outbox and queue:** How do we reliably deliver asynchronous work?
- **Reconciliation and compensation:** What happens when an external operation has an uncertain or irreversible outcome?
- **Rate limiting and admission control:** How do we handle a massive burst without overwhelming the system?

Get these distinctions right, and you can reason through most of the important follow-ups without memorizing a separate solution for each one.
