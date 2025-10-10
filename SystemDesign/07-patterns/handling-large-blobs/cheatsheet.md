# Handling Large Blobs - L5 Interview Cheatsheet

## Core Problem

**Never proxy large files through your application servers**

- Files >100MB kill server performance and eat bandwidth
- Servers become dumb pipes adding latency and cost
- Blob storage + CDN already have global infrastructure

## The Pattern: Direct Upload/Download

1. **Server role**: Generate temporary credentials, validate access
2. **Client role**: Upload/download directly to/from blob storage
3. **Storage role**: Handle the actual bytes and notify completion

## Quick Decision Framework

### When to Use

- Files >100MB (immediate red flag in interviews)
- Video platforms, file sharing, photo storage
- Any user-generated content that's binary

### When NOT to Use

- Small files <10MB (unnecessary complexity)
- Need real-time validation during upload
- Compliance requires data inspection
- Immediate feedback needed based on file contents

## Core Components

### 1. Presigned URLs

```text
What: Temporary URLs with embedded permissions
How: Server signs URL with cloud credentials
Duration: 15min - 1 hour typically
Restrictions: File size, content type, upload location
```

### 2. Chunked Uploads (>100MB)

```text
AWS S3: Multipart uploads (5MB+ parts)
Google Cloud: Resumable uploads (any chunk size)  
Azure: Block blobs (4MB+ blocks)
Benefit: Resume from failed chunks, not start over
```

### 3. State Synchronization

```text
Problem: Database vs blob storage consistency
Solution: Storage events + reconciliation jobs
Pattern: Create DB record → Upload → Event updates status
```

## Interview Deep Dives

### "What if upload fails at 99%?"

**Answer**: Chunked uploads with resumable capability

- Client queries which parts already uploaded
- Resume from failed chunk, not from beginning
- Store session ID for cross-session resume
- Lifecycle policies clean incomplete uploads

### "How prevent abuse?"

**Answer**: Quarantine → Validate → Promote pipeline

- Upload to quarantine bucket first
- Run virus scans, content validation
- Move to public bucket only after approval
- Size limits in presigned URL conditions

### "How handle metadata?"

**Answer**: Database for metadata, storage for bytes

- Create DB record with 'pending' status immediately
- Use consistent storage key pattern
- Storage events update DB when upload completes
- Never embed rich metadata in object tags

### "How ensure fast downloads?"

**Answer**: CDN + Range requests

- CloudFront/CDN for geographic distribution
- Range requests for resumable downloads
- Cache headers for frequently accessed files
- Signed CDN URLs for access control

## L5 Scaling Patterns

### Geographic Distribution

```text
Upload: Presigned URLs to regional buckets
Download: Multi-region CDN with signed URLs
Mobile: Upload to nearest region, replicate async
```

### Concurrent Processing

```text
Events trigger multiple workflows:
- Virus scanning
- Thumbnail generation  
- Metadata extraction
- Search indexing
```

### Cost Optimization

```text
Storage classes: Hot → Warm → Cold → Archive
Lifecycle policies: Auto-tier based on access
Cleanup: Delete incomplete multipart uploads
```

## Common Architecture

```text
Client Request → API Server (validate, generate presigned URL)
                ↓
Client → Blob Storage (direct upload)
                ↓
Storage Event → Message Queue → Processing Workers
                ↓
Database Update (status: completed)
```

## Red Flags to Avoid

- ❌ Proxying large files through API servers
- ❌ Storing files in database as BLOBs
- ❌ No resumable upload for large files
- ❌ Trusting client without server validation
- ❌ No cleanup of incomplete uploads
- ❌ Serving large files without CDN

## L5 Talking Points

- "For files over 100MB, I'd use presigned URLs to bypass our servers"
- "We need chunked uploads with resumable capability for large files"
- "Storage events will update our database when uploads complete"
- "CDN with signed URLs for fast, secure downloads"
- "Quarantine bucket for security validation before promoting to public"