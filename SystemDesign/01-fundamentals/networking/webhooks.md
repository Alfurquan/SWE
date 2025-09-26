# Webhooks

Imagine you're building an e-commerce platform and using an external payment processor like Stripe to collect payments from users.

Once a user completes a payment, your system needs to:

- Mark the order as paid
- Send an invoice
- Notify the warehouse to start packing

But here's the challenge:Stripe operates on its own infrastructure. Your system doesn’t control it. So how do you know instantly when a payment goes through?

A naive solution would be to keep asking Stripe every few seconds
This is known as polling.

Now imagine doing this for every order on a site like Amazon.
It just doesn’t scale and wastes server resources.
Instead of your app repeatedly asking, what if Stripe could just tell you when the payment succeeds?
That’s what webhooks do.

## What is a webhook ?

A webhook is a simple way for one system (provider) to notify another system (receiver) in real time when an event happens using an HTTP request.

### Real-World Analogy

Let’s say you go to a busy restaurant.
The host says: “There’s a 30-minute wait. Please leave your number, and we’ll text you when your table is ready.”
You don’t need to stand at the counter asking every 2 minutes: “Is my table ready yet?”
Instead, you walk away, and when your turn comes, they notify you automatically.
That’s the idea behind webhooks.

## How do webhooks work ?

At a high level, webhooks work through registration, triggering, and delivery.

