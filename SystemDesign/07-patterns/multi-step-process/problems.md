# Problems

## Exercise: The "All-or-Nothing" Travel Booking

Scenario: You are designing the backend for a travel portal (like Expedia). A user wants to book a "Weekend Gateway" package which consists of a Flight and a Hotel.

The Workflow:

Payment: Charge the user's card for the total amount ($500).

Book Flight: Call the Airline API to reserve a seat.

Book Hotel: Call the Hotel API to reserve a room.

Confirm: Send a confirmation email to the user.

The Constraints (The "L5" Complexity):

Distributed Ownership: The Airline API and Hotel API are 3rd-party services. You do not own their databases.

Latency: The Airline API is legacy and can take up to 45 seconds to return a confirmation.

Failure Mode: The Hotel API is fast, but availability is volatile. It is very common for the Flight to be booked successfully, but the Hotel step to fail because the room was snatched up by someone else.

Business Rule: This is an "All-or-Nothing" transaction. We cannot leave the user with a flight but no hotel (or vice versa).

---

### Your Task
Please outline your solution focusing on these three points:

Orchestration Strategy: Would you use a single synchronous request, a message queue chain (Choreography), or a Workflow Engine? Why is your choice specifically better for the 45-second latency constraint?

The "Partial Failure" Scenario: Walk me through exactly what happens if Step 2 (Flight) succeeds, but Step 3 (Hotel) fails (returns "Sold Out").

What happens to the Flight?

What happens to the Payment?

Idempotency: If your server crashes right after charging the payment but before booking the flight, and the user (or the client app) retries the request, how do you ensure you don't charge them $1,000?

---

## Solution

### Orchestration Strategy

For this all-or-nothing travel booking we will be using a workflow engine as it will allow for the 45 second latency contraint. Workflows can also utilize signals to wait for external events. Most durable execution engines provide a way to wait for signals that is more efficient and lower-latency than polling. So we can send a signal for the 45 second and wait for it.

### Partial failure scenarion

We will cancel the flight booking, and refund the payment back. This means we will have to redo the flight booking and payment steps if the hotel booking fails. We can do this by having compensating actions for each step in the workflow. So if the hotel booking fails, we can trigger the compensating action for the flight booking (cancel flight) and payment (refund payment). This will nclude API calls to the airline and payment gateway to cancel the flight and refund the payment.

### Idempotency

To ensure idempotency in payments we can use an idempotency key like a transaction id. When the user retries the transaction, we will see if the transaction id exists in the database. If it does we will not charge the user, else we will go ahead and charge the user and store the transaction id in the database to ensure idempotency in retries. These transaction ids can get cleaned by a cron job which will ensure we do not leave behind stale transaction ids in the database.

---