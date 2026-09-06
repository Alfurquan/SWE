# Video Platform (YouTube/Netflix) — Complete Deep Dive

## Overview

A video platform has two fundamentally different workloads:
- **Upload pipeline**: heavy compute (transcoding), large file handling, async processing
- **Streaming delivery**: extreme read throughput, latency-sensitive, geographically distributed

These require completely different architectures, which is why this is a popular interview question — it tests whether you can design for both.

## Functional Requirements

```
upload_video(creator_id, video_file, metadata) → video_id
stream_video(video_id, quality, byte_range) → video_chunk
search_videos(query) → List[VideoMetadata]
get_feed(user_id) → List[VideoMetadata]
record_watch_event(user_id, video_id, timestamp, watch_duration)
get_video_metadata(video_id) → VideoMetadata
```

## Non-Functional Requirements

- Videos available for streaming within 30 minutes of upload
- Stream start latency < 2 seconds
- Seamless quality adaptation based on network conditions
- 99.99% availability for streaming (viewers)
- 99.9% availability for upload (creators)
- Support 1M concurrent streams at peak

## Scale

```
500M daily active viewers
10K video uploads/day
1M concurrent video streams at peak
500PB total video storage
Average video: 1GB across all quality levels
Average watch session: 30 minutes
```

---

## Core Entities

```
Video
  - id
  - creator_id
  - title, description, tags
  - status: UPLOADING → UPLOADED → TRANSCODING → READY → PUBLISHED
  - upload_url (pre-signed)
  - created_at

VideoVariant (one per quality level per video)
  - video_id
  - quality: 360p / 480p / 720p / 1080p / 4K
  - storage_url (S3 path to manifest + segments)
  - bitrate
  - status: PENDING → TRANSCODING → READY

WatchEvent
  - user_id
  - video_id
  - timestamp
  - watch_duration
  - quality_played
  - device_type
```

---

## Storage Choices

| Data | Storage | Why |
|------|---------|-----|
| Video metadata | PostgreSQL | Structured, relational (creator → videos), transactional, moderate write volume (10K/day) |
| Video files (raw + transcoded) | S3 / Azure Blob | Designed for large objects, 11 nines durability, cheap at petabyte scale |
| Search index | Elasticsearch | Inverted index for full-text search, relevance ranking, faceted filtering |
| Watch events | Cassandra | Write-heavy (millions/sec), append-only event data, LSM-based, partition by video_id |
| User feed (recommendations) | Redis + Cassandra | Redis for hot/current feed (fast reads), Cassandra for feed history |
| Playback position (resume) | Redis | Small key-value: (user_id, video_id) → position. Fast reads, tolerates loss |
| View counts | Redis | Pre-computed counter, same pattern as YouTube view counts exercise |
| Event buffer | Kafka | Decouple ingestion from processing, absorb spikes, at-least-once delivery |

---

## Part 1: Upload Pipeline

### Step 1 — Upload Initiation

```
Creator → POST /videos (title, description, tags)
Server:
  1. Authenticate creator (JWT)
  2. Create video record in Postgres (status: UPLOADING)
  3. Generate pre-signed S3 URL (valid for 1 hour)
  4. Return { video_id, upload_url } to creator

Why pre-signed URL:
  - Video bytes go directly from client to S3
  - Server never handles large file data
  - Reduces server bandwidth and memory pressure
```

### Step 2 — Chunked Upload

```
Creator client:
  1. Split video into 8MB chunks
  2. Upload chunks in parallel (5-10 concurrent streams) to S3
  3. Each chunk carries a checksum for integrity verification
  4. S3 verifies checksum on receipt

If upload fails at chunk 47 of 100:
  - Client tracks uploaded chunks locally
  - On retry, resumes from chunk 48
  - No re-upload of chunks 1-47

This is S3 Multipart Upload — a built-in feature.
```

### Step 3 — Upload Complete

```
Client → POST /videos/{id}/complete
Server:
  1. Verify all chunks received (S3 CompleteMultipartUpload)
  2. Update video status: UPLOADING → UPLOADED
  3. Publish event to Kafka topic: "video-uploaded"
     { video_id, s3_path, duration, resolution }
```

### Step 4 — Transcoding Pipeline

```
                    ┌──────────────┐
 Kafka: video-      │  Transcoding │    S3: transcoded
 uploaded topic ───►│  Workers     │───► segments per
                    │  (scalable)  │    quality level
                    └──────────────┘
                          │
                          ▼
                    Update Postgres:
                    video status → READY
```

**How transcoding works:**

```
Input: raw 4K video (50GB)

Step 1: Split into 5-second segments
  Segment 1: 0:00 - 0:05
  Segment 2: 0:05 - 0:10
  ...

Step 2: Transcode each segment at each quality level (PARALLEL)
  Segment 1 → [4K, 1080p, 720p, 480p, 360p]  (Worker A)
  Segment 2 → [4K, 1080p, 720p, 480p, 360p]  (Worker B)
  Segment 3 → [4K, 1080p, 720p, 480p, 360p]  (Worker C)
  ...

Step 3: Generate manifest file (HLS .m3u8 or DASH .mpd)
  Lists all quality levels and their segment URLs

Step 4: Upload transcoded segments + manifest to S3
```

**Pipeline parallelism — why it's fast:**

```
Without pipelining:
  Upload 50GB (20 min) → transcode all (4 hrs) = 4+ hrs

With chunk-level pipelining:
  Chunk 1 uploaded → immediately transcode at all qualities
  Chunk 2 uploaded → immediately transcode
  (upload and transcoding happen simultaneously)
  
  Total ≈ upload time + last chunk's transcode time ≈ 25-30 min
```

**Worker scaling:**
- Each transcoding worker processes one segment at one quality
- A 3-hour video = 2160 segments × 5 qualities = 10,800 tasks
- Distribute across 100 workers → done in minutes
- Use a task queue (SQS/Kafka) for job distribution
- Idempotent: if worker crashes, another retries the same segment

### Step 5 — Post-Processing

After transcoding completes:

```
1. Update Postgres: video status → READY
2. Sync metadata to Elasticsearch via CDC
   (title, description, tags → searchable)
3. Generate thumbnail (extract frame at multiple timestamps)
4. Run content moderation (separate ML pipeline)
   - If flagged → status: UNDER_REVIEW (not published)
   - If clean → status: PUBLISHED
5. Invalidate/warm CDN cache for the video manifest
```

---

## Part 2: Video Streaming (Read Path)

### How Adaptive Bitrate Streaming Works

```
Client requests video:
  1. GET manifest file (video_123.m3u8)
     Manifest lists:
       - 360p segments: /segments/360p/seg_001.ts, seg_002.ts, ...
       - 720p segments: /segments/720p/seg_001.ts, seg_002.ts, ...
       - 1080p segments: /segments/1080p/seg_001.ts, seg_002.ts, ...

  2. Client measures bandwidth
     - Good bandwidth → request 1080p segments
     - Bandwidth drops → switch to 720p or 480p mid-stream
     - Bandwidth recovers → switch back up

  3. Client fetches segments sequentially
     seg_001 (1080p) → seg_002 (1080p) → seg_003 (720p) → seg_004 (720p) → ...
                                          ↑ bandwidth dropped

  4. Client buffers 10-30 seconds ahead
     - Brief network drops (< buffer duration) → no visible interruption
```

### CDN Architecture

```
                          ┌─────────┐
                          │  Origin │
                          │  (S3)   │
                          └────┬────┘
                               │ cache miss (rare)
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              ┌──────────┐┌──────────┐┌──────────┐
              │CDN Edge  ││CDN Edge  ││CDN Edge  │
              │US-West   ││EU-West   ││Asia-East │
              └────┬─────┘└────┬─────┘└────┬─────┘
                   │           │           │
              Viewers      Viewers      Viewers
              in US        in EU        in Asia
```

**CDN behavior:**
- Popular videos: cached at edge → served in <50ms
- Unpopular videos: cache miss → fetch from origin → cache at edge → serve
- Request coalescing: if cache expires and 100K viewers request simultaneously, ONE request goes to origin, all others wait for cache repopulation
- This is why CDN is critical: 1M concurrent streams hitting S3 directly would be catastrophic. CDN reduces origin requests to <0.1%

### Stream Start Flow

```
Client opens video:
  1. GET /videos/{id}/metadata → Postgres (or Redis cache)
     Returns: { title, manifest_url, thumbnail, duration }
  
  2. GET manifest_url → CDN (or origin on miss)
     Returns: list of quality levels + segment URLs
  
  3. Client measures bandwidth, picks initial quality
  
  4. GET first segment → CDN
     Client starts playback after first segment loads
     
  Target: < 2 seconds from click to first frame
```

### Playback Resume (Cross-Device)

```
During playback:
  Client periodically reports position (every 10-30 seconds):
  POST /videos/{id}/progress { user_id, position: 2703 }
  Server: SET progress:{user_id}:{video_id} 2703 in Redis

On different device:
  Client opens same video
  GET /videos/{id}/progress → Redis: position 2703
  Client: "Resume from 45:03?" → seek to segment containing 45:03
  
For transient disconnects (30-second drop):
  - Entirely client-side
  - Client buffer covers the gap
  - On reconnect, client knows which segment it needs next
  - No server involvement
```

---

## Part 3: Search

### Elasticsearch Index

```
Index: videos
Document:
{
  "video_id": "abc123",
  "title": "How to build a distributed system",
  "description": "In this video we cover...",
  "tags": ["system-design", "distributed", "engineering"],
  "creator_name": "TechChannel",
  "created_at": "2024-01-15",
  "view_count": 1500000,
  "duration": 1823
}
```

**How search works:**
```
Query: "distributed system design"

Elasticsearch:
  1. Tokenize query → ["distributed", "system", "design"]
  2. Look up inverted index:
     "distributed" → [video_abc, video_def, video_xyz]
     "system"      → [video_abc, video_ghi, video_xyz]
     "design"      → [video_abc, video_xyz, video_jkl]
  3. Score by relevance (TF-IDF / BM25) + popularity (view_count)
  4. Return ranked results
```

### Sync: Postgres → Elasticsearch

```
Option 1: CDC (Change Data Capture) — preferred
  Postgres WAL → Debezium → Kafka → Elasticsearch consumer
  - Async, decoupled
  - Seconds of lag (acceptable)
  - No dual-write inconsistency

Option 2: Application-level dual write
  - Write to Postgres AND Elasticsearch in application code
  - Risk: one succeeds, other fails → inconsistency
  - Not recommended
```

**Search lag (5-second CDC delay):**
- Not a real problem — no one searches for a video uploaded 3 seconds ago
- Creator sees their own video immediately on their dashboard (served from Postgres)
- Search visibility lagging by a few seconds has zero user impact

### Search Optimization

```
- Cache popular search results in Redis (TTL 5-10 minutes)
- Autocomplete / typeahead: separate prefix index in Elasticsearch
- Filters: by duration, upload date, quality, creator
- Personalization: boost results from creators the user follows
```

---

## Part 4: Watch Events & Analytics

### Event Pipeline

```
Viewer watches video
    │
    ▼
Client reports every 30 seconds:
  POST /events/watch { user_id, video_id, position, quality, device }
    │
    ▼
API Gateway → Kafka topic: "watch-events"
  Partitioned by video_id (co-locate events per video)
  For viral videos: add shard suffix (video_id + hash(user_id) % 10)
    │
    ├─────────────────────────────┐
    ▼                             ▼
Consumer Group 1:            Consumer Group 2:
Write to Cassandra           Stream processor (Flink)
(raw events, batch writes)   ├─ Update view count (Redis INCRBY, batched)
                             ├─ Feed recommendation updates
                             ├─ Anomaly detection (bot filtering)
                             └─ Real-time analytics dashboard
```

### View Count

```
Same pattern as view counter exercise:
- Batch increments in app server memory (5 seconds)
- Flush to Redis: INCRBY view_count:{video_id} <batch_count>
- Periodically flush Redis to Postgres (durable archive)
- View count may be seconds stale — acceptable ("4.2M views")
```

### Bot Detection

```
API Gateway layer:
  - Rate limiting per IP, per user (first line of defense)
  - Catches crude bots

Stream processor layer:
  - Analyze watch patterns in time window
  - Flags:
    - 90% of views with watch_duration < 5 seconds
    - Burst from data center IPs (not residential)
    - Same user watching same video 100 times
    - Views from new accounts with no other activity
  - Action: freeze view count, flag for manual review
```

---

## Part 5: Feed / Recommendations

### Feed Generation

```
NOT computed per request (too expensive at 500M users).
Pre-computed and stored:

Watch event → Kafka → Recommendation Engine
  │
  ├─ Builds user profile (watch history, preferences, dwell time)
  ├─ Collaborative filtering ("users like you watched X")
  ├─ Content-based filtering ("similar to videos you liked")
  │
  ▼
Write pre-computed feed to:
  - Redis: current feed (fast reads, latest recommendations)
  - Cassandra: feed history (if user scrolls deep)

GET /feed:
  Server reads from Redis → returns pre-computed list
  Sub-millisecond response, no computation at query time
```

### Feed Refresh

```
- Recommendation engine runs continuously (stream processing)
- Feed updated every few minutes per user
- New video from a subscribed creator → inject into feed immediately
  (separate fast path, not through the ML pipeline)
```

---

## Part 6: Failure Handling

### Upload Failures

| Failure | Impact | Recovery |
|---------|--------|----------|
| Client crashes mid-upload | Partial chunks in S3 | Client resumes from last chunk. S3 multipart has 7-day expiry for incomplete uploads |
| S3 unavailable | Upload fails | Client retries with exponential backoff. Pre-signed URL still valid for 1 hour |
| Transcoding worker crashes mid-segment | One segment not transcoded | Task queue redelivers the segment to another worker. Idempotent — re-transcoding same segment is safe |
| Transcoding produces corrupt output | Bad quality video | Verify segment integrity (checksum) after transcode. If corrupt, retry. Don't mark video as READY until all segments verified |

### Streaming Failures

| Failure | Impact | Recovery |
|---------|--------|----------|
| CDN edge node down | Viewers in that region lose cache | CDN automatically routes to next nearest edge. Origin serves on cache miss |
| S3 origin down | New cache misses can't be fulfilled | S3 has 99.999999999% durability. Cross-region replication for extreme cases. CDN cache continues serving already-cached content |
| Client network drops for 30s | Playback pauses | Client buffer covers brief drops. On reconnect, resume from next needed segment |
| Client network drops for 5 min | Playback stops | Client reconnects, requests manifest again, seeks to last known position, resumes |

### Event Pipeline Failures

| Failure | Impact | Recovery |
|---------|--------|----------|
| Kafka broker down | Events can't be published | Kafka replication (RF=3). Producer retries to another broker. If all brokers down, client buffers events locally |
| Cassandra node down | Some writes fail | Cassandra replication (RF=3). Writes go to replica. Hinted handoff replays when node recovers |
| Stream processor crashes | Aggregation pauses | Flink restarts from last checkpoint (Kafka offset + RocksDB state). At-least-once processing with idempotent writes |
| Redis (view counts) crashes | Counts stale | Redis with AOF + replication. On recovery, replay AOF. Small window of count loss acceptable |

### Data Consistency Failures

| Failure | Impact | Recovery |
|---------|--------|----------|
| Postgres write succeeds, CDC to Elasticsearch fails | Video not searchable | CDC retries from Kafka offset. Eventually consistent — resolves in seconds |
| Redis view count drifts from Cassandra | Displayed count slightly wrong | Periodic reconciliation job. Acceptable for view counts |
| Feed Redis cache evicted | User gets empty feed | Fall back to Cassandra feed history. Rebuild cache on next recommendation cycle |

---

## Part 7: Capacity Estimation

```
Storage:
  10K uploads/day × 1GB average = 10TB/day raw
  × 5 quality levels = 50TB/day transcoded
  × 365 days = ~18PB/year new storage
  Total after years: 500PB (given)

Streaming bandwidth:
  1M concurrent streams × 5 Mbps average bitrate = 5 Tbps
  CDN handles this — no single origin serves this load

Kafka:
  Watch events: 1M concurrent × 1 event/30sec = 33K events/sec
  + view events, search events, etc. ≈ 50-100K events/sec
  100K / 30K per partition ≈ 4 partitions minimum, provision 32 for growth

Cassandra (watch events):
  50K writes/sec (from Kafka consumers, batched)
  50K / 15K per node ≈ 4 nodes minimum, with RF=3 ≈ 12 nodes

Elasticsearch:
  10K new documents/day (low write volume)
  Search queries: ~50K/sec (high read volume)
  5-10 node cluster with replicas
```

---

## Part 8: The Complete Architecture Diagram

```
                        Creators                              Viewers
                           │                                     │
                    POST /upload                          GET /videos/{id}
                           │                                     │
                           ▼                                     ▼
                    ┌─────────────┐                      ┌──────────────┐
                    │  API Server │                      │  API Server  │
                    └──────┬──────┘                      └──────┬───────┘
                           │                                    │
              ┌────────────┼────────────┐                       │
              ▼            ▼            ▼                       ▼
        ┌──────────┐ ┌──────────┐ ┌─────────┐          ┌──────────────┐
        │ Postgres │ │  Kafka   │ │   S3    │          │     CDN      │
        │(metadata)│ │(events)  │ │(videos) │◄─────────│  (edge cache)│
        └──────────┘ └────┬─────┘ └────┬────┘          └──────────────┘
              │            │            │
              │     ┌──────┴──────┐     │
              │     ▼             ▼     │
         CDC  │ ┌────────┐  ┌────────┐  │
         │    │ │Transcode│  │  Flink │  │
         ▼    │ │Workers  │  │(stream)│  │
    ┌─────────┐│ └───┬────┘  └───┬────┘  │
    │Elastic  ││     │           │        │
    │Search   ││     ▼           ▼        │
    └─────────┘│  S3 (transcoded) ┌───────┴──┐
               │              │   │Cassandra │
               │              │   │(events)  │
               │              │   └──────────┘
               │              │
               │         ┌────┴────┐
               │         │  Redis  │
               │         │(counts, │
               │         │ feed,   │
               │         │ resume) │
               │         └─────────┘
               │
          ┌────┴─────┐
          │ Postgres  │
          │(metadata) │
          └───────────┘
```

---

## Part 9: Key Interview One-Liners

| Topic | One-liner |
|-------|-----------|
| Upload | "Pre-signed URL for direct S3 upload, chunked for resumability, async transcoding via task queue" |
| Transcoding | "Split into 5-second segments, transcode each at all quality levels in parallel across workers. Pipeline with upload for 30-min turnaround" |
| Streaming | "HLS/DASH adaptive bitrate — client fetches manifest then segments, switching quality based on bandwidth. CDN serves 99.9% of requests" |
| CDN stampede | "Request coalescing — one miss goes to origin, all others wait for cache repopulation" |
| Search | "Elasticsearch with CDC from Postgres. Seconds of lag is acceptable — no one searches for a 3-second-old video" |
| View counts | "Batched Redis INCRBY, periodic flush to Postgres. Seconds of staleness acceptable for display counts" |
| Feed | "Pre-computed by recommendation engine (collaborative + content filtering), stored in Redis. Zero computation at query time" |
| Bot detection | "Rate limiting at gateway + anomaly detection in stream processor (short watch durations, data center IPs, burst patterns)" |
| Resume | "Client-side for transient drops (buffer covers it). Server-side position tracking in Redis for cross-device resume" |
