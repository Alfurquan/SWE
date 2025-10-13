# Managing Long-Running Tasks - L5 Interview Cheatsheet

## Core Problem

**Never block users waiting for slow operations**

- Operations >3-5 seconds kill user experience
- Synchronous processing causes timeouts and poor UX
- Different operations need different hardware resources

## The Pattern: Accept → Queue → Process Async

1. **Web server**: Validate request, create job, return job ID immediately
2. **Queue**: Store jobs durably, enable worker coordination
3. **Workers**: Pull jobs, process asynchronously, update status

## Quick Decision Framework

### When to Use (Interview Triggers)

- Video transcoding, image processing, PDF generation
- Operations taking >5 seconds
- Bulk operations (email campaigns, data exports)
- When math doesn't work (need 100+ servers for processing)
- Different hardware needs (GPU vs CPU workloads)

### When NOT to Use

- Fast operations <1 second
- Simple CRUD that's already optimized
- Real-time requirements where delay isn't acceptable

## Core Components

### 1. Message Queue

```text
Redis + Bull/BullMQ: Great for startups, simple setup
AWS SQS: Managed, no ops overhead, pay-per-message
RabbitMQ: Enterprise features, requires self-hosting
Kafka: Event streaming, replay capability, high throughput
```

### 2. Worker Pool

```text
Regular Servers: Full control, long-running jobs OK
Serverless (Lambda): Auto-scaling, 15min limit
Containers (K8s/ECS): Middle ground, better resource usage
```

### 3. Job Status Tracking

```text
Database stores: job_id, status, progress, result_url
States: pending → processing → completed/failed
Client polls or gets notified when complete
```

## Interview Deep Dives

### "What if worker crashes mid-job?"

**Answer**: Heartbeat mechanism + job retry

- Workers send periodic heartbeats to queue
- Queue retries jobs when heartbeat stops
- Configure retry limits (3-5 attempts typical)

### "What about repeated failures?"

**Answer**: Dead Letter Queue (DLQ)

- Move jobs to DLQ after max retries
- Isolates poison messages from healthy work
- Human investigation required for DLQ items

### "How prevent duplicate work?"

**Answer**: Idempotency keys

- Unique key per operation (user_id + action + timestamp)
- Check existing jobs before creating new ones
- Make work itself idempotent (safe to retry)

### "Queue gets backed up during peak?"

**Answer**: Backpressure + autoscaling

- Set queue depth limits, reject when overwhelmed
- Autoscale workers based on queue depth
- Separate queues for fast vs slow jobs

### "Jobs depend on other jobs?"

**Answer**: Simple chains vs orchestration

- Simple: Each worker queues next step
- Complex: Use Step Functions/Temporal/Airflow
- Include full context for independent retries

## L5 Scaling Patterns

### Queue Management

```text
Separate queues by job type (fast/slow)
Priority queues for urgent work
Batch processing for efficiency
Geographic distribution for global users
```

### Worker Scaling

```text
Auto-scaling based on queue depth
Different instance types per job type
Spot instances for cost optimization
Circuit breakers for downstream failures
```

### Monitoring

```text
Queue depth and processing latency
Worker health and job failure rates
Dead letter queue growth
End-to-end job completion times
```

## Common Architecture

```text
Client → API Server (validate, create job, return job_id)
                ↓
        Message Queue (Redis/SQS/Kafka)
                ↓
Worker Pool → Process Job → Update Status
                ↓
        Database (job status/results)
                ↓
Client polls or gets notified
```

## Red Flags to Avoid

- ❌ Synchronous processing for >5 second operations
- ❌ No retry mechanism for failed jobs
- ❌ Infinite retries without dead letter queue
- ❌ No idempotency protection
- ❌ Single queue for all job types
- ❌ No monitoring of queue depth/worker health

## L5 Talking Points

- "This operation takes 45 seconds, so I'll return a job ID immediately"
- "I'll use separate worker pools for CPU vs GPU workloads"
- "Queue depth monitoring will trigger auto-scaling"
- "Dead letter queue isolates poison messages"
- "Idempotency keys prevent duplicate work from impatient users"

## Interview Examples

- **YouTube**: Video upload → transcoding workers
- **Instagram**: Photo upload → thumbnail generation workers  
- **Uber**: Ride request → matching algorithm workers
- **Stripe**: Payment → fraud detection workers
- **Dropbox**: File upload → virus scanning workers

---