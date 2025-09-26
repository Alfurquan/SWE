# Online learning plaform

Design storage for an online learning platform like Coursera:

- Store video lectures, course materials, assignments
- Track student progress and completion status
- Need to support various content types (videos, PDFs, quizzes)
- 2M+ students, 100K+ courses
- Students frequently pause/resume videos

## Questions

- Which database type(s) would you choose for different data types?
- How would you handle video metadata vs actual video files?
- What would be your approach for tracking progress?

---

## Solution

### Requirements analysis

- Data volume: 2M+ students, 100K+ courses
- Read vs write: Read heavy system as courses are updated less frequently as compared to students watching them. (We can quantify it as well depending on no of student concurrently accessing the courses. If x students concurrently access a course Y, then read frequency for a course is x students/sec)
- Latency needs: System should support low latency about < 1ms to support good concurrent viewing of courses.
- Primary use case: Storing video courses, video course watching by students
- Secondary use case: Tracking student progress, updating course, student details etc.

### Database selection

So here as per the requirements of the system, we can consider these databases for storing course materials, student data, assignment etc.

- Relational database like SQL, Postgres

Pros

- Strong consistency guarantees, ACID property
- Data can be stored in structured manner in table in rows and columns, so it provides a structured way to store data

Cons

- Less flexible to schema changes
- Need to join different tables to get some data, joins can slow down the query leading to increase in latency

- Non relation database like Document DB

Pros

- Flexible, no structure, data can be stored in schema less manner
- More scalable than relational database

Cons

- No structure to data
- Deeply nested structure data can be difficult to query and manage in a document database.

1. We will choose Document database here because it is flexible to schema changes and is highly scalable.

2. We will store actual video files in blob storage like Azure blob or S3 and store the URL of the file in the document for the course data. Reason: Blob supports storing large data files like video files, pdfs. etc. If we directly store these in a non relational db, the size of the db will increase a lot and it will lead to increase in latency to query the database.

### Implementation details

#### Schema design

1.Student
- id (PK)
- name
- email
- courses_taken: List[course_id] (FK) (index on this)
- Assignments: List[assignment_id] (FK)

2.Course
- id (PK)
- name
- description
- video_files: List[url]

3.Assignment
- id (PK)
- course_id (FK) (index on this)
- completion_status
- student_id (FK) (index on this)

#### Scale

For scale we can partition the database tables based on student id, course id and assignment id fields. We can use consistent hashing as the partitioning scheme here.

We will also use redis as a cache to store hot courses, courses recently viewed and followed by a student to reduce load on our actual database

We can also use replication and replicate the data for courses, students on multiple database nodes to make system highly available in case of failures.

#### Video metadata and actual file

 We will store actual video files in blob storage like Azure blob or S3 and store the URL of the file in the document for the course data. Reason: Blob supports storing large data files like video files, pdfs. etc. If we directly store these in a non relational db, the size of the db will increase a lot and it will lead to increase in latency to query the database.

 #### Tracking progress

For tracking progress, we can have another document for it like Student_Course_Progress

Student_Course_Progress
- student_id (FK)
- course_id (FK)
- progress

As the student navigates through the course, we will update this. For updating this we can use asynchronous processing like message queues, and will send requests to update this table in batches. In this way, the actual app will be running fine and these updates can be done in the background.


# Enhanced solution

# Online Learning Platform - Enhanced Solution

Design storage for an online learning platform like Coursera:

- Store video lectures, course materials, assignments
- Track student progress and completion status  
- Need to support various content types (videos, PDFs, quizzes)
- 2M+ students, 100K+ courses
- Students frequently pause/resume videos

## Questions

- Which database type(s) would you choose for different data types?
- How would you handle video metadata vs actual video files?
- What would be your approach for tracking progress?

---

## Enhanced Solution

### Requirements Analysis

**Data Volume:**
- 2M+ students, 100K+ courses
- Estimated 200M+ video views per month
- ~10TB of video content, ~100GB of metadata

**Traffic Patterns:**
- Read-heavy: 90% reads, 10% writes
- Peak: 50K concurrent video streams
- Course updates: ~1K per day
- Progress updates: ~500K per day

**Latency Requirements:**
- Course loading: <200ms (realistic for metadata)
- Video streaming: <300ms initial load + CDN delivery
- Progress updates: <500ms (non-critical path)
- Search/browse: <300ms

**Primary Use Case:** Video streaming with progress tracking
**Secondary Use Cases:** Course management, student analytics, assignments

### Database Selection & Justification

#### Option Comparison Matrix

| Database Type | Course Metadata | Video Files | Progress Tracking | Analytics |
|---------------|-----------------|-------------|------------------|-----------|
| **Relational** | ✅ Structure | ❌ Size limits | ✅ ACID | ✅ Complex queries |
| **Document** | ✅ Flexibility | ❌ Size limits | ✅ Schema-less | ❌ Aggregations |
| **Blob Store** | ❌ No queries | ✅ Large files | ❌ No structure | ❌ No queries |
| **Time-series** | ❌ Not time-based | ❌ Wrong use case | ✅ Progress over time | ✅ Analytics |

#### Final Architecture Decision

**Hybrid Multi-Database Approach:**

1. **Document Database (MongoDB)**: Course metadata, student profiles, quiz data
2. **Blob Storage + CDN**: Video files, PDFs, course materials  
3. **Time-Series Database**: Progress tracking, analytics, viewing patterns
4. **In-Memory Cache (Redis)**: Session data, frequently accessed courses

**Justification:**
- Document DB handles varying course structures (different quiz types, assignments)
- Blob storage optimized for large file delivery
- Time-series perfect for progress tracking over time
- Cache reduces database load for hot content

### Implementation Details

#### Schema Design

**MongoDB Collections:**

```javascript
// Students Collection
Student: {
  _id: ObjectId,
  name: String,
  email: String (indexed),
  enrolled_courses: [course_id],  // Denormalized for quick access
  subscription_type: String,
  created_at: Date
}

// Courses Collection  
Course: {
  _id: ObjectId,
  title: String (indexed),
  description: String,
  instructor_id: ObjectId,
  category: String (indexed),
  difficulty_level: String,
  content: {
    videos: [{
      video_id: String,
      title: String,
      duration_seconds: Number,
      blob_url: String,
      quality_variants: {
        "360p": String,
        "720p": String, 
        "1080p": String
      }
    }],
    pdfs: [{
      title: String,
      blob_url: String,
      size_mb: Number
    }],
    quizzes: [{
      quiz_id: String,
      questions: [...],
      passing_score: Number
    }]
  },
  total_duration: Number,
  created_at: Date
}

// Assignment Collection
Assignment: {
  _id: ObjectId,
  course_id: ObjectId (indexed),
  title: String,
  instructions: String,
  due_date: Date,
  max_score: Number,
  submission_format: String
}
```

**Time-Series Database (InfluxDB) for Progress:**

```javascript
// Student Progress Measurements
student_progress: {
  time: timestamp,
  student_id: String (tag),
  course_id: String (tag), 
  video_id: String (tag),
  progress_seconds: Number (field),
  completion_percentage: Number (field),
  session_id: String (tag)
}

// Video Analytics
video_analytics: {
  time: timestamp,
  video_id: String (tag),
  student_id: String (tag),
  event_type: String (tag), // play, pause, seek, complete
  timestamp_seconds: Number (field),
  quality: String (tag)
}
```

#### Content Type Handling Strategy

**Videos:**
- Store in blob storage with multiple quality variants
- Use CDN for global delivery (CloudFront/Azure CDN)
- Implement adaptive bitrate streaming
- Generate thumbnails and preview clips

**PDFs:**
- Store in blob storage with direct download links
- Implement PDF viewer integration
- Track reading progress via scroll position

**Quizzes:**
- Store as structured documents in MongoDB
- Support multiple question types (MCQ, fill-in-blank, code)
- Real-time validation and scoring

**Assignments:**
- File submissions stored in blob storage
- Metadata and grading in document database
- Support version control for resubmissions

#### Tracking Progress - Detailed Implementation

**Multi-Level Progress Tracking:**

```javascript
// Real-time progress updates via WebSocket
student_session: {
  student_id: String,
  course_id: String,
  current_video_id: String,
  current_position: Number, // seconds
  last_heartbeat: timestamp,
  device_type: String
}

// Persistent progress in time-series DB
progress_checkpoint: {
  time: timestamp,
  student_id: String,
  course_id: String, 
  video_id: String,
  checkpoint_seconds: Number,
  completed: Boolean,
  watch_time_seconds: Number, // actual watch time vs video duration
  engagement_score: Number // calculated metric
}
```

**Progress Update Strategy:**
1. **Real-time**: WebSocket updates every 10 seconds during video playback
2. **Checkpoints**: Persistent saves every 30 seconds to time-series DB
3. **Offline Support**: Browser localStorage with sync when back online
4. **Conflict Resolution**: Last-write-wins with timestamp comparison

#### Scalability & Performance

**Partitioning Strategy:**
```
MongoDB Sharding:
- Courses: Shard by category (balanced distribution)
- Students: Shard by student_id hash (consistent hashing)
- Progress: Shard by student_id + course_id composite key

Time-Series Partitioning:
- Partition by time (monthly) + student_id
- Retention policy: Raw data 90 days, aggregated data 2 years
```

**Caching Strategy:**
```javascript
Redis Cache:
- Popular courses: TTL 1 hour
- Student progress: TTL 30 minutes  
- Search results: TTL 15 minutes
- Session data: TTL 24 hours

Cache Keys:
- course:{course_id}
- student_progress:{student_id}:{course_id}
- search:{query_hash}
```

**Performance Optimizations:**
- Read replicas for MongoDB (3 replicas)
- CDN caching for static content (24h TTL)
- Connection pooling for database connections
- Async processing for non-critical updates

#### Advanced Features

**Video Streaming Optimization:**
- **Adaptive Streaming**: Multiple quality variants based on bandwidth
- **Resume Capability**: Exact timestamp restoration across devices
- **Prefetching**: Download next video segment while watching current
- **Offline Support**: Download videos for offline viewing

**Progress Analytics:**
```sql
-- Time-series queries for insights
SELECT mean(completion_percentage) 
FROM student_progress 
WHERE course_id = '123' 
GROUP BY time(1d)

-- Engagement patterns
SELECT student_id, 
       SUM(watch_time_seconds) as total_watch_time,
       COUNT(DISTINCT video_id) as videos_watched
FROM video_analytics 
WHERE time > now() - 30d
GROUP BY student_id
```

**Real-time Features:**
- **Live Progress Sync**: Multiple device synchronization
- **Collaborative Features**: Study groups, discussion threads
- **Real-time Notifications**: Assignment due dates, course updates

### Trade-offs & Limitations

**Optimizing For:**
- ✅ Read performance (course browsing, video streaming)
- ✅ Flexible schema (different course types)
- ✅ Scalability (millions of students)
- ✅ Progress tracking accuracy

**Sacrificing:**
- ❌ Complex cross-collection joins (denormalized data instead)
- ❌ Strong consistency for progress (eventual consistency acceptable)
- ❌ Single database simplicity (operational complexity with multiple DBs)

**Potential Bottlenecks:**
- Video streaming bandwidth costs
- Time-series database growth (need archival strategy)
- Real-time progress updates at scale
- Cross-database consistency challenges

### Monitoring & Operations

**Key Metrics:**
- Video buffering rates and quality downgrades
- Progress update latency and success rates
- Database query performance and connection pooling
- Cache hit rates and CDN performance

**Alerting:**
- Progress sync failures (>5% failure rate)
- Video streaming errors (>1% error rate)  
- Database connection pool exhaustion
- Unusual traffic spikes or bot detection

This enhanced solution addresses the realistic latency requirements, provides comprehensive progress tracking, handles all content types effectively, and includes operational considerations for a production system.