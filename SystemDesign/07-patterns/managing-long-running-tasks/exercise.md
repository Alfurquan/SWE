# Problems on Managing long running tasks

## Scenario 1: Email Marketing Platform (Easy)

You're building Mailchimp. Users create email campaigns and send them to subscriber lists ranging from 1,000 to 1 million recipients. Currently, when a user clicks "Send Campaign," the system tries to send all emails synchronously, causing:

Request timeouts for large lists (>10,000 recipients)
Users can't tell if their campaign is actually sending
Server crashes when multiple users send large campaigns simultaneously
Question: How would you redesign the email sending system to handle large campaigns reliably?

### Solution

For this problem, we will be using async processing as sending emails to 1000 to 1 Million subscribers will take seconds or even minutes. By using async processing, whenever a user clicks "Send Campaign", they do not have to wait for minutes, instead we respond immediately and then perform the email sending in background. Here's how the flow will be

- User clicks on "Send Campaign", the client sends a POST request to our API server with the campaign details like name, details etc.
- The API server accepts the POST request, creates a new campaign record for the campaign in the database with the status as pending and returns the campaign id back to the client.
- The API server after making entry in the database, places the campaign id of the record in a message queue, like kafka. We choose kafka here because it offers great durability and low latency. It also gives ability to replay events so none of the events are lost.
- From the queue, a set of workers consume the event, retrieve the campaign id placed, fetches campaign details from the details, it also fetches the list of subscribers for the sender and then sends email to the recipients.
- Once all the emails have been sent, the workers update the status of the campaign as completed.
- The client, can use the campaign id returned, to poll for the progress and we show a good user experience to the user by showing a progress bar etc.
- In order to optimize the email sending process, we can send emails in parallel to the recipients. We can even process these events in batches from the queue to optimize the email sending process.
- This async background process decouples the API server from the email sending process and each of them can be scaled independently. In case of high load, we can autoscale the background workers to handle more load.

Failure handling

- In case any worker crashes in the middle of sending emails, the event can be handled by another worker.
- We can retry failed emails or temporary failures, and if retries exceed a certain limit, we move those events to dead letter queues for manual inspection and resolution
- Email providers have rate limit, our workers respect this and retry failed emails with exponential backoff.
- In case of peak load, when the queue grows a lot, we can apply backpressure where we apply some depth limit to the queue, where if the depth of the queue exceeds the limit, we ignore new events till the consumer catches up. We can autoscale and more consumers i.e. workers to help resolve this issue

---

## Scenario 2: Social Media Analytics (Medium)

You're building a Twitter analytics dashboard. Users can request reports showing:

- Tweet engagement over the last year (requires processing millions of records)
- Follower growth analysis (complex calculations across time periods)
- Competitor comparison reports (aggregating data from multiple accounts)

These reports take 2-5 minutes to generate. Users currently wait on a loading screen, often refreshing and creating duplicate requests.

Question: Design a system that provides a better user experience while handling the computational load efficiently.

### Solution

For this problem, we will be using asynchronous processing when user request creating reports. By using async processing, whenever a user clicks "Generate report", they do not have to wait for minutes, instead we respond immediately and then perform the report generation in background. Here's how the flow will be

We will be using message queues like Kafka for storing user requests here while the requests will be picked up by background workers. We choose Kafka here as it provides great durability guarantees, low latency and it gives ability to replay events so no events would get lost in case of crashes or failures.

For this problem, wince different reports will take different times to complete processing, we do not want a long running process block short ones, so we will have different message queues for different types of reports, long running and short ones

- User click on generate button
- The UI sends a POST /reports with parameters for generating report including the type of report they want, like tweet engagement, follower growth analysis etc.
- The post request comes to our API server which generates a unique idempotency key for the request like userId + action + timestamp (rounded to the time we want to prevent duplicates). This unique key serves as the jobId for the request. The server first checks if the job with the id exists, if it does, it returns immediately with the jobId, else it creates an entry in the job table in the database with the id and status as pending and places the request in the right queue depending on action type. It returns back with the newly created job id. This idempotency key helps prevent duplicate requests if user clicks on refresh or the generate button.
- The client can use the jobId to poll for the status of the background job.
- The background workers listening for events on the message queue, pick up the request from the queue, lookup the job details from the database and perform the job in the background.
- Once the worker finishes execution, they update the job status to completed in the database.
- When the job is completed, the client polling from the status of the job, fetches the data from the API server and shows the result to the user.
- Before returning results back to the user, the API server also caches the result in an in memory cache like redis. This helps reducing the work and the reports can now be served from the cache directly. This is helpful for reusable reports and ones which are requested often. 
- We can also set TTL to the cache data so that after a certain time, (lets say 1 day), here time depends on whether reports are generated from real time data or historical data. For historical data, TTL can be large like 1 day, for real time data, TTL can be small like 30 seconds to 5-10 mins. TTL helps expire the cache entries. A background cron job thread can clean up stale cache entries and this helps to keep cache memory in check.

Failure handling

- In case any worker crashes in the middle of processing, the event can be handled by another worker.
- We can retry failed reports or temporary failures, and if retries exceed a certain limit, we move those events to dead letter queues for manual inspection and resolution
- In case of peak load, when the queue grows a lot, we can apply backpressure where we apply some depth limit to the queue, where if the depth of the queue exceeds the limit, we ignore new events till the consumer catches up. We can autoscale and more consumers i.e. workers to help resolve this issue.

---

## Scenario 3: Video Conference Recording (Medium)

You're building Zoom's recording feature. When meetings end:

- Raw video files are 5-50GB depending on duration and participants
- Need to process audio/video separately, generate transcripts
- Create multiple formats (MP4, audio-only, mobile-optimized)
- Extract highlights and generate summary clips

Processing takes 20-60 minutes per recording. Users expect to access recordings "soon" after meetings end.

Question: Design a system that processes recordings efficiently while providing good user experience and handling failures gracefully.

### Solution

For this problem, we will be using asynchronous processing when meetings end. By using async processing, whenever a meeting ends, we will place jobs to prepare the recordings and immediately return back to the user.

Now for this use case, for every meeting which is recorded, we need to process audio and video separately, create different formats and extract highlights and generate summary clips. Now some of these steps can run in parallel like audio extraction, video transcoding, transcript generation. So we can use multiple message queues for them. These tasks can then be picked up by multiple workers and done in parallel.

We will be using message queues like Kafka for storing requests here while the requests will be picked up by background workers. We choose Kafka here as it provides great durability guarantees, low latency and it gives ability to replay events so no events would get lost in case of crashes or failures.

Here is how the flow would be

- When a meeting end, the client makes a POST call to our API server with the meeting id
- The API server accepts the request, and creates a new job in the database with the meeting details and status as pending. The server places the job id in separate message queues to be picked up by workers.
- The workers pick up the event from the message queue, fetch job and meeting details from job id in the message queue. The workers then fetch the video files which will be stored in object storage like S3 or azure blob and perform the processing.
- Once the worker finish processing, the update the status in the job table accordingly. Different workers will be performing jobs in parallel so they update status like lets say the worker finishes audio extraction, it can update status as audio extraction completed and so on.
- This status can be used on the client side to show the user where we are in the processing pipeline.
- This is helpful in cases where users might want audio while video is still processing. So if audio extraction is completed as fetched from status in job table, the client can serve audio to the users while video is still processing.
- Now there are some steps which depends on other steps, like extracting highlights and summary clips. They depend when audio extraction, video transcoding and transcript generation. So when lets say audio extraction is completed, the workers doing it can places another event on the message queue for extracting highlights. Some other worker will then pick it up and perform the processing.
- Once all the processing is completed, the job status will be updated to completed, and the client can then display whatever the user is interested in.
- Large files like one of 50GB will be processed in chunks.

Failure handling

- In case any worker crashes in the middle of processing, the event can be handled by another worker.
- We can retry failed reports or temporary failures, and if retries exceed a certain limit, we move those events to dead letter queues for manual inspection and resolution
- In case of peak load, when the queue grows a lot, we can apply backpressure where we apply some depth limit to the queue, where if the depth of the queue exceeds the limit, we ignore new events till the consumer catches up. We can autoscale and more consumers i.e. workers to help resolve this issue.
- To make sure the job status is consistent, we can use distributed transactions or 2 phase commit protocols when updating the job status in the database and placing events in the message queue. This ensures that either both operations succeed or both fail, preventing partial updates.

### Follow up questions

#### How do you ensure consistency in job status updates ?

When multiple workers update job status in parallel, you can get inconsistent states:

```text
Worker A: "audio_extraction: completed" 
Worker B: "video_transcoding: completed"
But what if Worker A's database update fails while Worker B's succeeds?
```

- Option 1: Database Transactions with Optimistic Locking

```sql
-- Each worker does this atomically
BEGIN TRANSACTION;
UPDATE jobs 
SET audio_status = 'completed', updated_at = NOW(), version = version + 1
WHERE job_id = 'abc123' AND version = 5;  -- Only update if version matches
COMMIT;
```

- Option 2: Event Sourcing Pattern

```text
Instead of updating status directly:
1. Worker publishes "AudioExtractionCompleted" event
2. Job orchestrator consumes all events
3. Orchestrator maintains the authoritative job state
4. Single source of truth, no race conditions
```

- Option 3: Saga Pattern

```text
Each status update is a mini-transaction:
1. Update database
2. If success, publish event to queue
3. If either fails, rollback both
4. Use 2PC coordinator to ensure atomicity
```

```text
I'd use optimistic locking for simplicity, but if we need stronger guarantees, 
I'd implement event sourcing where a single orchestrator maintains job state."
```

#### How Parallel Queues Work

```text
meeting_end_event → [Fan-out to multiple queues]
                  ↓
    ┌─────────────────┬─────────────────┬─────────────────┐
    │ audio_queue     │ video_queue     │ transcript_queue│
    └─────────────────┴─────────────────┴─────────────────┘
            ↓                  ↓                  ↓
    audio_workers     video_workers     transcript_workers
```

Coordination mechanism

```python
# When meeting ends, orchestrator does:
job_id = create_job(meeting_id, status="processing")

# Fan out to parallel queues
publish_to_queue("audio_queue", {"job_id": job_id, "task": "extract_audio"})
publish_to_queue("video_queue", {"job_id": job_id, "task": "transcode_video"})
publish_to_queue("transcript_queue", {"job_id": job_id, "task": "generate_transcript"})

# Each worker updates specific status fields
def audio_worker(message):
    process_audio(message.job_id)
    update_job_status(message.job_id, audio_status="completed")
    
    # Check if dependencies are ready for next stage
    if all_dependencies_ready(message.job_id):
        publish_to_queue("highlights_queue", {"job_id": message.job_id})
```

Dependency management

```python
def all_dependencies_ready(job_id):
    job = get_job(job_id)
    return (job.audio_status == "completed" and 
            job.video_status == "completed" and 
            job.transcript_status == "completed")
```

```text
Each queue handles one type of task. 
Workers check if their completion unlocks dependent tasks and 
trigger them by publishing to downstream queues.
```

#### Processing Large Files in Chunks

The Challenge

50GB file can't fit in memory
Single worker might take 60+ minutes
If worker crashes at 59 minutes, you lose all work

```text
I'd split large files into 500MB chunks, process each chunk independently, 
and merge results at the end. This enables resumability and progress tracking
```

### Quick confidence builders

#### For Consistency Questions

- Start simple: "Optimistic locking handles most race conditions"
- Show depth: "For stronger guarantees, I'd use event sourcing"
- Be practical: "The complexity depends on our consistency requirements"

#### For Parallel Processing Questions

- Explain fan-out: "One trigger event spawns multiple parallel tasks"
- Show coordination: "Workers check dependencies before triggering next stage"
- Mention monitoring: "Each queue can be monitored and scaled independently"

#### For Large File Questions

- Emphasize resumability: "Chunking means we never lose more than 500MB of work"
- Show progress tracking: "Users see incremental progress, not just 'processing...'"
- Mention resource efficiency: "Workers need only 500MB RAM, not 50GB"

---
