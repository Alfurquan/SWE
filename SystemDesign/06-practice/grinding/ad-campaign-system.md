 # The Scenario

Imagine we are building the backend for "AdVantage," a new real-time advertising platform. Advertisers use our dashboard to monitor their active campaigns. They need to see how their ads are performing right now to make split-second decisions on bidding and budget.

# Answer

## Functional requirements

- When a user sees an ad, the system must record the event
- When a user clicks on an ad, the system must record the event
- The advertisers should be able to view CTR (click through rate) for their campaigns (We can keep this simple and just focus on last 5 minutes and last hour)
- The advertisers should be able to view the total spends for each campaign (We can keep this simple and just focus on last 5 minutes and last hour)

## Non functional requirements

- Scale: 10 billion events per day (roughly 120,000 events per second on average, peaking at 300,000+).
- Consistency: While "approximate" counts might be okay for some analytics, the Spend metrics must be highly accurate for billing purposes.
- Availability: The ingestion must be highly available; we cannot afford to "lose" click events as they represent revenue.
- Latency: Metrics for ad clicks should be near real-time with latency of 1-10 seconds.
- Read/Write Ratio: ~1:10 — the system should be optimized for writes
- Billing Accuracy: No over-billing or under-billing should happen for advertisers

We can always bring in more requiements into scope after discussing with the interviewer.

## Data model

Next up we will list down the data models for our system and their attributes. Note that here for the `seen` and `click` event we are tracking the user id as well, which means the user must be authenticated to view and click an ad. If user id is not needed then we can remove this constraint after discussing with the interviewer.

### Campaign

- id (PK)
- name
- description
- budget
- publisher_name

### Ad

- id (PK)
- campaign_id
- name
- media_urls
- cost_per_click

### Seen

- id (PK)
- ad_id
- campaign_id
- timestamp
- user_id

### Click

- id (PK)
- ad_id
- campaign_id
- timestamp
- user_id

### Spend

- campaign_id
- amount
- time_duration (This will be last 10 minutes and last hour for now)

### CTR

- campaign_id
- value
- time_duration (This will be last 10 minutes and last hour for now)

Please note that I have mentioned `Spend` and `CTR` in the data models here to just state what the schema for these will look like. These will be aggregated by processing layer and then stored. These arent just tables in a relational database.

## API

After defining the data models, lets define some API endpoints. We can always come back and refine the API and data models as we iterate on our design and interviewer feedback

### Record Seen

```
POST /seen

{
    "ad_id": <>,
    "campaign_id": <>,
    "event_id": <>,
    "client_timestamp": <>
}

Response - 201 Created
```

We will not pass the user id in the payload, it will be enriched by the gateway after extracting the user from the JWT token

### Record click

```
POST /click

{
    "ad_id": <>,
    "campaign_id": <>,
    "event_id": <>,
    "client_timestamp": <>
}

Response - 201 Created
```

We will not pass the user id or cost per click in the payload, it will be enriched by the server after extracting the user from the JWT token and fetching cost per click from the db. How this will actually happen will be discussed when I get to the high level design of the system. Also I have passed campaign_id in the payload here to prevent looking up db for this info on huge vilume of write events which will be sent.
The cient timestamp is just for debugging and we would not be relying on it for processing the events. The event id is passed to prevent duplicate clicks in case of retries.

### Get metrics

```
GET /metrics?campaign_id={123}&type={SPEND|CTR}

Response - 200 OK

{
    "type": "SPEND|CTR",
    "value": <>
    "campaign_id": <>,
    "time_duration": <last 10 minutes|last 1 hour>
}
```

## Choice of tools

We will be designing this system by thinking in terms of layers. Below will be the layers that will be present in the system

- Client layer: Recording `seen` and `click` events and sending it to the server
- Ingestion layer: Ingesting the events to the system. The ingestion should be fast due to large volume of writes/sec.
- Processing layer: Processing the ingested events and aggregating and computing `CTR` and `spend` metrics
- Storage layer: Storing the aggregated metrics for querying later.

So we have defined the layers, now we will go ahead and discuss the choice of database and tools needed at different layers of the system.


### Ingestion layer

For ingesting the data, we can use `Kafka`. For our large volume of writes, we need an ingestion layer which is fast and `Kafka` supports faster writes due to its append only commit log architecture. Also Kafka ensures at least once guarantees due to its architecture which has replication built in. This ensures none of the `seen` and `click` events are lost.

We will have two topics in Kafka, one for `seen` events and another for `click` events. The producers will be the API servers which will be receiving the events from the clients and then pushing it to the respective topics in Kafka.

To scale and parallelize the huge volume of writes, we can partition the topics based on `campaign_id` or `ad_id`. This way we can have multiple consumers consuming from different partitions in parallel and processing the events. 

To ensure ordering of events for a particular campaign or ad, we can use the same partitioning key for both `seen` and `click` events. This way all events for a particular campaign or ad will go to the same partition and will be processed in order. For example, if we partition based on `campaign_id`, then all events for a particular campaign will go to the same partition and will be processed in order. However this can lead to hot partitions if some campaigns are more popular than others. To resolve this we can add `salting` to the partitioning key. For example we can add a random number to the `campaign_id` to create a new partitioning key like `campaign_id + random_number`. This way we can distribute the events for a particular campaign across multiple partitions and avoid hot partitions. The trade off here is that we loose strict per campaign ordering but the processing layer (Spark/Flink) would handle this.

To prevent a bot from spamming `seen` and `click` events we will use redis. Redis is single threaded and can be used to prevent abuse. For example we can try to acquire a lock for lets say 60 seconds for a particular user and ad combination when we receive a `seen` or `click` event. If the lock is acquired successfully, then we can allow the event to be processed and if the lock is not acquired, then we can reject the event as it means that the user has already seen or clicked the ad in the last 60 seconds.

### Processing layer

For processing the events, we can use `Apache Flink` or `Apache Spark Streaming`. Both of these are stream processing frameworks which can process the events in real time and can handle large volume of data. They also have built in support for windowing and aggregation which will be useful for computing the `CTR` and `spend` metrics for the last 10 minutes and last hour.

### Storage layer

For storing the ad and campaign information, we can use a relational database like `PostgreSQL`. This will allow us to have strong schema guarantees and also support complex queries if needed.

For storing the aggregated metrics, as mentioned earlier we can use `Cassandra` for storing CTR and `PostgreSQL` for storing spends. We can also use a blob storage like `Amazon S3` for storing the raw seen and click events for historical analysis.

## High level design

Before going into the high level design, I would like to clarify one point

Since CTR is an aggregate metric (clicks/impressions), we don’t need to match individual events. We can independently count clicks and impressions per campaign in a time window and compute CTR.

Here is how we will be designing this system in layers

### Event layer

This is the layer where the event gets generated, that is on the client side when the user sees or clicks on an ad.

This is how the flow works here

- User sees or clicks on an ad.
- Client sends a post call to /seen and /clicks endpoint with the payload and unique event id which is generated on the client side. This event id would be used as an idempotency key later.
- Sample payload 
```
{
    "ad_id": <>,
    "campaign_id": <>,
    "event_id": <>,
    "client_timestamp": <>
}
```

### Ingestion layer

This is the layer where the event generated in the event layer is ingested into the system

This is how the flow works here

- The request is received by the API gateway which extracts user ID from the jwt token and places it in the payload. The gateway also injects an event time which is calculated based on client timestamp and server timestamp. If the client timestamp is within a reasonable threshold (say 5 minutes) of the server timestamp, then we can use the client timestamp as the event time, else we can use the server timestamp as the event time. This is done to prevent skewed results due to clients clock being skewed.
- The gateway puts the event in the corresponding `kafka` topic partitioned by campaign id. To prevent hot partitions, the gateway adds a random salt to the campaign id before putting it to the kafka topic. For example, if the campaign id is 123, then the partitioning key can be `123 + random_number`. This way we can distribute the events for a particular campaign across multiple partitions and avoid hot partitions. The trade off here is that we loose strict per campaign ordering but the processing layer (Spark/Flink) would handle this.

### Processing layer

This is the layer where the ingested events are processed and the metrics are computed.

- Spark streaming job consumes from kafka partitions.
- There are two workflows for the streaming job - computing ctr and computing spend.
- The worker for computing spend enriches the click event with cpc, counts the total spend for a time window by summing up the cpcs and then groups them by campaign id to compute the aggregated results. The worker writes the result to the database. To prevent overbilling, the worker uses the event id as the idempotency key. This idempotency key can be stored in a database or checkpointed in the streaming job to ensure that if the same click event is processed again due to retries, it does not lead to overbilling.
- The CPC is versioned by time and the worker can fetch the cpc for a click event based on the event time of the click. This way if there are any changes in the cpc for a campaign, it would be reflected in the spend computation correctly.
- The worker for computing ctr, sums up the total impressions and total clicks for a time window and then groups them by campaign id to the the ctr. The worker writes this computed ctr value to the database.
- Both the workers use watermark to ensure late arriving events are computed in the right window. For example, if we are computing the metrics for the last 10 minutes, then we can set a watermark of 15 minutes to allow for late arriving events to be included in the computation.
- A separate worker process also consumes events from the kafka topic partitions, enriches the click events with cpc and writes them to an object storage for historical analysis. This way we can have a record of all the click events along with their cpc for any future analysis or reprocessing if needed.

### Batch processing layer

Since we want spends to be accurate, so there can be some clicks which come even after the watermark ends. These clicks would be stored in the object storage. 

- A separate batch process does the reprocessing and computes the spend by consuming click events from object storage and writing the results to a different table. 
- The query layer decides which table to fetch results from - whether real time spend is intended or final value. We will discuss how the query layer does this in the next section.
- This way we can have both real time spend computation through streaming as well as correct spend computation using a batch process.

### Query processing layer

This is the layer where the advertisers can query the metrics for their campaigns.

- Advertisers call the /metrics end point to fetch the ctr and spend values for last 10 minutes or last hour.
- For CTR, the query layer can directly fetch the computed CTR value from the database as it is an aggregate metric and slight inaccuracy is acceptable for CTR.
- For Spend, the query layer uses a watermark like boundary called `finalized timestamp` produced by batch pipeline. For time ranges before this, it queries the batch (accurate) data, and for recent time ranges it queries the streaming (real-time) data. If a request spans both, it merges results from both sources.
