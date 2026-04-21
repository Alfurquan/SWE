# Job Scheduler

## Problem Statement: Distributed Job Scheduler

Scenario: You are tasked with building a centralized Distributed Job Scheduler for your company's microservices ecosystem. Many services need to "defer" work to a specific time in the future but don't want to manage their own timers or persistent queues.

## Functional requirements

- Clients should be able to submit jobs to the system to run on a schedule (Like every day, every monday of a week etc.) For now we will suport one off scheduled tasks and park the recurring jobs.
- Clients should be able to cancel a job.
- Clients should be able to get status of the jobs submitted by them
- Clients should be able to run a job immediately
- System supports running webhooks (Calling URL with payload) and pub/sub system as part of the job.
- System prevents duplicate jobs from getting scheduled using an idempotency key.

These are some of the functional requirements which our system would support. The last one we can discuss with the interviewer to bring in scope or out of scope.

## Non Functional requirements

- Scale: Supprt 10 million scheduled jobs per day, with a peak of 5K jobs executing per second
- Precision: Jobs to be executed as close to the target execute_at time as possible (within +/- 2seconds)
- Durability: Once a job is accepted with a `202` response, the system should never lose it
- Retention: The system should handle jobs scheduled from 1 minute to 6 months in the future.
- Reliability: The system should ensure the job scheduled to run is executed atleast once, even in the face of server failures. This ensure atleast once guarantees for job execution.
- Throtting: The system should ensure the jobs of one client should not affect the performance of other clients. This is to ensure fair usage of the system.

## Data model

Next up we will be defining the data models for the system. We will be listing down the tables and their attributes that we will be storing.

### Job

- id (Primary key)
- name
- description
- status: SCHEDULED, CLAIMED, ENQUEUED, EXECUTING, SUCCEEDED, FAILED
- execute_at
- retries
- callback_type: WEBHOOK, PUBSUB
- callback_url
- callback_payload
- idempotency_key
- run_immediately (boolean)
- client_id (Foreign key to Client table)

### Client

- id (Primary key)
- name
- email

These are the basic data models that we will be using for our system. We can always add more attributes as we go along.

## Choice of database

As we mentioned in the non functional requirements, that we need to support 10 million scheduled jobs per day, with a peak of 5K jobs executing per second. This means that we need a database that can handle high write and read throughput.

We need a database that can support 5000 reads/writes per second. We can use a Relational database like PostgreSQL for this purpose. The relational databases use B+ tree indexes which are good for efficiently querying the jobs based on the `execute_at` and `status` attributes.

To further optimize the reads, we can index the `execute_at` and `status` columns. This will allow us to quickly query the jobs that are scheduled to run at a specific time and are in a specific status.

### Hot spot problem

If 10,000 tasks are all scheduled for exactly 12:00:00, and you have 10 scheduler nodes polling the DB, then to ensure that they don't all pick up the same job, we can use a technique called "claiming". When a scheduler node picks up a job, it will update the status of the job to "CLAIMED". So we will be having a status column in our Job table which will have the following values: SCHEDULED, CLAIMED, ENQUEUED, EXECUTING, SUCCEEDED, FAILED. This way, when a scheduler node picks up a job, it will update the status to "CLAIMED" and other scheduler nodes will not pick up the same job.

We will implement this by using a SQL query that updates the status of the job to "CLAIMED" and returns the job details in a single transaction. This will ensure that only one scheduler node can claim a job at a time.

```SQL
UPDATE jobs
SET status = 'CLAIMED'
WHERE id = (
    SELECT id FROM jobs
    WHERE status = 'SCHEDULED' AND execute_at <= NOW()
    ORDER BY execute_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
```

### Sharding 

To further scale our database, we can use sharding. We can shard our database based on the `client_id` attribute. This way, the jobs of one client will be stored in a different shard than the jobs of another client. This will ensure that the jobs of one client do not affect the performance of other clients. The trade off here is that if one client has a lot of jobs, then it can lead to a hot spot in that shard

Another way to shard the database is by using a hash of the job id. This way, the jobs will be distributed across the shards in a more even manner. The trade off here is that we will not be able to query the jobs of a specific client easily.

Even another way to shard the database is by using a range of the `execute_at` attribute. This way, the jobs that are scheduled to run at a specific time will be stored in the same shard. The trade off here is that if there are a lot of jobs scheduled to run at the same time, then it can lead to a hot spot in that shard.

A single postgres instance can handle 5K reads/writes per seconds, but if load increases, we can implement sharding by using the options we listed above.

## API

### Create Job

```
POST /v1/jobs
Content-Type: application/json

{
    "name": "Job 1",
    "description": "This is job 1",
    "execute_at": "2024-07-01T10:00:00Z",
    "callback_type": "WEBHOOK",
    "callback_url": "https://example.com/webhook",
    "callback_payload": {
        "key": "value"
    },
    "client_id": 1,
    "idempotency_key": "unique_key_123",
    "run_immediately": false
    "retries": 3
}
``` 

### Cancel Job

```
POST /v1/jobs/{job_id}/cancel
```

### Get Job 

```
GET /v1/jobs/{job_id}
Content-Type: application/json
{
    "id": 1,
    "name": "Job 1",
    "description": "This is job 1",
    "status": "SCHEDULED",
    "execute_at": "2024-07-01T10:00:00Z",
    "callback_type": "WEBHOOK",
    "callback_url": "https://example.com/webhook",
    "callback_payload": {
        "key": "value"
    },
    "client_id": 1,
    "retries": 3
    "run_immediately": false
}
```

## High level design

We will design the system by discussing the end to end flow for all the functional requirements of the system. In this problem, we are designing a system that just schedules jobs of different clients to run at the specified time. The system does not care how the job is executed, it simply calls the callback and updates the status accordingly.

Lets next discuss the end to end flow for the functional requirements of the system.

### Submit Job

- Client sends a POST call to `/v1/jobs` with the job metadata payload and a unique idempotency key
- The request is recieved by the API gateway which checks for Auth, rate limiting etc and forwards the request to job service
- The job service stores the job metadata and the idempotency key in the jobs table in the database.
- The job is initially stored with a job status as `SCHEDULED`
- This idempotency key is crucial to prevent duplicate jobs getting stored and scheduled in case of network faults and clients retrying the POST call to submit the job.

### Schedule Job

- The job details are stored in the jobs table in the database.
- Multiple job scheduler (nodes) poll the table at some frequency, lets say every hour to claim the jobs due for next hour. Once the job scheduler pulls the jobs due to run in the next hour, it changes the jobs status to `CLAIMED`
- If 10,000 jobs are all scheduled for exactly 12:00:00, and we have 10 scheduler nodes polling the DB, then to ensure that they don't all pick up the same job, we can use a technique called "claiming". When a scheduler node picks up a job, it will update the status of the job to "CLAIMED". This way, when a scheduler node picks up a job, it will update the status to "CLAIMED" and other scheduler nodes will not pick up the same job.
We will implement this by using a SQL query that updates the status of the job to "CLAIMED" and returns the job details in a single transaction. This will ensure that only one scheduler node can claim a job at a time.
- The scheduler store the jobs in their memory and start a timer process to put the job in a message queue at the time the job is scheduled to run. It changes the status of the job to `ENQUEUED`. In order to make sure the placing of the job on the message queue and update of job status is atomic, we use a technique here called `Outbox pattern` This is how it works

    - In a single transaction, the scheduler node updates the job status to `ENQUEUED` and inserts the job record in an `outbox table`. So if any one of them fails, the other is rolled back and we prevent the system from being in an inconsistent state.
    - A separate worked process gets notified via Change data capture(CDC) when the outbox table is updated and the worker process places the job data on the message queue.

- We will use a message queue like `Kafka` here as its append only commit log allows for faster writes. Also kafka offers at least once guarantees via its replication mechanism which will help in ensuring that the job would not be lost.
- We can also use acknowledgement feature and consumer offsets provided by kafka to make sure the jobs are executed even in case of workers crashing.
- To ensure scaling and parallelism we can partition the queue. We will discuss this in below section.

### Execute Job

- Once the job is placed on the message queue, separate worker process pull the job details from the queue. They update the job status to `EXECUTING` and call the callback to execute the job.
- After the job completes execution, the worker updates the job status to `SUCCEEDED` or `FAILED`.
- if the job fails, the worker retries the job based on the retries value in the job metadata.

## Failure Scnearios

### Prevent same job to be scheduled twice

- This is solved using idempotency key which is generated by the client and passed to the server when calling the POST call to submit the job.
- The idempotency key is stored in the database along with other job metadata.
- Incase of network failures, if the client retries to submit the job twice, the server looks up the idempotency key and prevents storing the duplicate job record.

### Prevent same job to be claimed by multiple scheduler nodes

- This is solved using separate job status for different stages in a job lifecycle. 
- If 10,000 jobs are all scheduled for exactly 12:00:00, and we have 10 scheduler nodes polling the DB, then to ensure that they don't all pick up the same job, we can use a technique called "claiming". When a scheduler node picks up a job, it will update the status of the job to "CLAIMED". This way, when a scheduler node picks up a job, it will update the status to "CLAIMED" and other scheduler nodes will not pick up the same job.
- We will implement this by using a SQL query that updates the status of the job to "CLAIMED" and returns the job details in a single transaction. This will ensure that only one scheduler node can claim a job at a time.

### Job stuck at Claimed state

- This happens in situation when a scheduler node claims a job and then crashes.
- To solve this we can use a separate background worker process which checks for job which are stuck in claim state for a long time (greater than a threshold) and moves them back to scheduled state so that they can be picked up by other scheduler nodes.

### Job stuck at Executing state

- This happens in situation when a worker node picks up a job for execution and then crashes.
- To solve this we can use a separate background worker process which checks for job which are stuck in executing state for a long time (greater than a threshold) and moves them back to enqueued state so that they can be picked up by other worker nodes for execution.

### Prevent multiple worker nodes executing the same job

- This can be handled using a state based approach. When a worker node picks up a job for execution, it updates the job status to `EXECUTING`. This way, if another worker node tries to pick up the same job, it will see that the job is in `EXECUTING` state and will not pick it up for execution.

### Scaling and partitioning

To ensure scaling and parallelism we can partition the message queue and use consumer groups of workers. Each partition can be consumed by only one consumer in a consumer group at a time. This way, we can ensure that the jobs are distributed across multiple worker nodes for execution and we can achieve parallelism in job execution.

Below are the different ways we can partition the message queue:

- We can partition the queue based on `client_id`. This way, the jobs of one client will be in a different partition than the jobs of another client. This will ensure that the jobs of one client do not affect the performance of other clients. The trade off here is that if one client has a lot of jobs, then it can lead to a hot spot in that partition.

- We can partition the queue based on a hash of the job id. This way, the jobs will be distributed across the partitions in a more even manner.

- We can partition the queue based on a range of the `execute_at` attribute. This way, the jobs that are scheduled to run at a specific time will be in the same partition. The trade off here is that if there are a lot of jobs scheduled to run at the same time, then it can lead to a hot spot in that partition.


## Deep dives

### Deep Dive 1: The Fresh Task Problem

"You said scheduler nodes poll for jobs due in the 'next hour' and keep them in memory. If I am a user and I schedule a task to run 2 minutes from now, and your scheduler node just completed its hourly poll 1 minute ago, how does my task get executed on time?"

### Answer

Option 1: Reduce polling frequency from one hour to every minute. This can help solve the above issue but can lead to DB getting overloaded with lots of requests from different scheduler nodes.

Option 2: Push based approach
In this approach whenever a new job is created in the DB, in the same transaction we write an event called job created in an outbox table. A separate worker process gets notified via CDC when a new job is created, the worker gets the last poll time of the schedulers and if the job is scheduled to run in the current poll window, it pushes the job to the time buffer.

We will use redis as the time buffer here and utilize the sorted sets data structure of redis which would give us O(LogN + k) lookups and O(logN) inserts. Here the key would be job id and score would be next execution time. The scheduler will pull next due jobs from redis and remove the jobs from redis using a Lua script to ensure that the operation is atomic.

So for this situation we would be using a hybrid approach, new jobs whose next execution time is in the current poll window gets pushed to redis, the jobs which are long term (hours later) get executed via the pull approach.

A single redis instance would get overwhelmed with multiple schedulers pulling jobs from it, so we can use a redis cluster here.

---

### Deep Dive 2: The Hot Shard / Fairness Problem

"We have two clients: Client A (a massive marketing service) schedules 1 million 'Happy New Year' webhooks for exactly midnight. Client B (a critical security service) schedules 1 task for the same time. If we use a simple Kafka queue, Client B's critical task might get stuck behind 1 million marketing tasks. How can we ensure fairness or priority so one client doesn't starve the others?"

### Answer

Having separate queues per tenant is not a scalable approach because with a large number of tenants (e.g., thousands), most of which are low-volume, it would create unnecessary operational overhead and fragmented utilization.

Instead, we can handle fairness using a combination of upstream control and runtime scheduling policies:

1. Upstream fairness via quotas

We can enforce per-tenant quotas on the number of jobs they can submit per day/hour.
This protects the system from heavy-hitter tenants overwhelming shared resources and ensures baseline fairness at ingestion time.

2. Shared queue with fair scheduling at execution time

Instead of per-tenant queues, we use a shared queue and apply scheduling policies at the worker layer.

Workers can implement:

round-robin across tenants
weighted fair scheduling (based on tenant priority/SLA)

This ensures that no single tenant dominates execution capacity.

Priority should ideally be enforced at both layers, but for different goals:

1. Before queue (ingestion layer) — primary control
Enforce quotas and priority tagging
Prevent system overload
Protect SLAs at admission time

2. After queue (execution layer) — fine-grained fairness
Workers apply scheduling logic (round robin / weighted selection)
Handles dynamic runtime conditions like:
varying job durations
uneven load across tenants

---

### Deep Dive 3: The "At Least Once" Side Effect
Since we use Kafka and a Reaper process, we are guaranteeing At-Least-Once delivery. If our worker crashes exactly after calling a client's Webhook but before committing the Kafka offset, the next worker will pick up the task and call the Webhook again.

The Challenge:

- What contract must we establish with our clients (the users of the scheduler) so that their systems don't break when they receive the same task twice?
- What should the payload include to help them?

### Answer

To solve this idempotency issue, the system can include a unique key in the header while calling the client's webhook. This means the clients must handle this key in the header when they recieve a call to their webhook. The clients can use this key to see if they have already executed the callback (or webhook), if not executed, they can execute the webhook and store they idempotency key, if executed, they simply return the result of the last execution and do not execute the callback again.

Now to choose the idempotency key to be passed in the header of the clients webhook, we can use 

- A unique guid which the worker generates when calling the client's callback URL. The issue here is that a worker can call the client's callback url, pass the unique guid as the idempotency key and then crash. The second worker can pick the job, and generate a fresh new guid as the idempotency key and pass it to the clients callback and this would lead to duplicate processing.

- A better and more robust approach here would be to pass the message offset from kafka which would be unique even if the message (Job) is retried by a different worker. This way, even if the job is retried by a different worker, the same idempotency key (kafka offset) would be passed to the client's callback and the client can use this key to prevent duplicate processing of the same job.

- The best option here is to pass job_id itself as the idempotency key. Job_id is unique for a job and is the best bet for use here as passing message offset can be leaky and since message off set is tied to kafka, if we more away from kafka, we would need to modify this part as well.

So the contract we are establishing with our clients is that we will be passing a unique idempotency key in the header when calling their webhook and they should use this key to prevent duplicate processing of the same job.



