# Problems on Handling large blobs

## Scenario 1: Video Streaming Platform (Easy)

You're designing YouTube. Users upload videos ranging from 50MB to 5GB. The current architecture routes uploads through API servers, causing:

- Server crashes during large uploads
- 7-minute upload times for 1GB videos
- Failed uploads force users to restart from scratch
Question: How would you redesign the upload system to handle these issues?

### Solution

We will be using blob or object storage approach here with clients uploading videos directly to object storage instead of API servers

Here's how we will re-architect it out.

- Client sends a request to upload a video
- API server receives it, generates a pre signed url using storage credentials. It also makes an entry in the database for the storage url with a status of pending. The database will be storing the metadata for the videos.
- The API server returns the pre-signed url back to the client.
- The client uses the pre-signed url to upload the video directly to the object store. The upload happens in small chunks, so that if at any point if upload fails, client can retry from the point the failure happened instead of starting from scratch.
- Progress tracking comes naturally with chunked uploads. As each part completes, you know the percentage done. Simple client-side math gives you a nice progress bar to show users.
- Once all the chunks, are uploaded, client sends another complete upload request to object store, the object store combines the chunks and stores them as a single file.
- Once upload is completed, the object store sends a notification to the API server via message queue, the API server then uses the storage url in the notification to update the status to completed in metadata database.
- The API server then sends a response back to the client that upload is completed.
- For downloads, we'd serve videos through CloudFront CDN with signed URLs. This gives global distribution and prevents unauthorized access while keeping our servers out of the video delivery path

---

## Scenario 2: Mobile Photo Backup (Medium)

You're building a mobile photo backup service like Google Photos. Users upload thousands of photos/videos from their phones, including:

- 4K videos up to 500MB each
- RAW photos up to 50MB each
- Batch uploads of 100+ files
- Unreliable mobile connections that drop frequently
Question: Design an upload system that works reliably on mobile networks and provides good user experience.

Think about: Resumable uploads, batch processing, mobile-specific challenges

### Solution

We will be using blob or object storage approach here with clients uploading photos and videos directly to object storage instead of API servers

Here's how we will re-architect it out.

- Client sends a request to upload a video or photo
- API server receives it, generates a pre signed url using storage credentials. It also makes an entry in the database for the storage url with a status of pending. The database will be storing the metadata for the videos and photos
- The API server returns the pre-signed url back to the client.
- The client uses the pre-signed url to upload the video or photo directly to the object store. The upload happens in small chunks, so that if at any point if upload fails, client can retry from the point the failure happened instead of starting from scratch. This is useful for unreliable mobile networks.
- Progress tracking comes naturally with chunked uploads. As each part completes, you know the percentage done. Simple client-side math gives you a nice progress bar to show users.
- Once all the chunks, are uploaded, client sends another complete upload request to object store, the object store combines the chunks and stores them as a single file.
- Once upload is completed, the object store sends a notification to the API server via message queue, the API server then uses the storage url in the notification to update the status to completed in metadata database.
- The API server then sends a response back to the client that upload is completed.
- For a single file, the above approach is good, but if we have many files say 100+, we can perform batch upload of the files, the process of upload remains same, the only difference being that instead of single upload we do upload in batches like 10 files at a time etc.
- We also track progress of the batches, and in case any batch fails, it can be retried.
- For background upload, we can use a background queue that persists jobs locally in SQLite. It monitors network/battery conditions and automatically retries for failed uploads using exponential backoff. It supports wifi only mode.
- For batching, we can be smart and request multiple presigned URLs at once, upload photos in parallel, prioritize recent photos over old ones and skip duplicated using local hash comparison.

---

## Scenario 3: Enterprise Document Storage (Medium)

You're building Dropbox for enterprises. Requirements:

- Files up to 2GB (presentations, videos, datasets)
- Must scan all uploads for viruses and sensitive data
- Compliance requires audit trail of who accessed what when
- Global teams need fast access from different regions
Question: Design a system that meets these security and compliance requirements while maintaining performance.

## Solution

We will be using blob or object storage approach here with clients uploading content directly to object storage instead of API servers

Here's how we will re-architect it out.

- Client sends a request to upload a content
- API server receives it, generates a pre signed url using storage credentials. It also makes an entry in the database for the storage url with a status of pending. The database will be storing the metadata for the content.
- The API server returns the pre-signed url back to the client.
- The client uses the pre-signed url to upload the content directly to the object store. The upload happens in small chunks, so that if at any point if upload fails, client can retry from the point the failure happened instead of starting from scratch.
- Progress tracking comes naturally with chunked uploads. As each part completes, you know the percentage done. Simple client-side math gives you a nice progress bar to show users.
- Once all the chunks, are uploaded, client sends another complete upload request to object store, the object store combines the chunks and stores them as a single file.
- Once upload is completed, the file is sent to the quarantine store, where it is scanned for viruses and sensitive data. During this time, the status of the file will be pending in metadata database, so if anyone tries to access this file, they will be denied.
- Once scanning is done, the object store sends a notification to the API server via message queue, the API server then uses the storage url in the notification to update the status to completed in metadata database.
- The API server then sends a response back to the client that upload is completed.
- For downloads, we can use CDN cloudfront to serve contents to users from geographically closer edge servers. So the users can access the file faster.
- To maintain audit trail, we can have another table like audit in the database with columns lets say fileId, emailId, timestamp. When someone requests access to the file, the request goes to the API server, the API server generates a pre signed url and routes the request to the CDN from where the user ca download and view the file. During this time, the API server records the identity of the person and timestamp in audit table.
- Presigned URL restrictions: File size and content-type limits baked into the signature
- Post-upload validation: File type verification in the quarantine phase
- User permissions: Check upload quotas and folder permissions before generating presigned URL

---

## Scenario 4: Social Media with Anti-Abuse (Hard)

You're designing Instagram's photo/video upload system. Challenges:

- Users try to upload inappropriate content
- Some users attempt to upload malware disguised as images
- Need immediate thumbnail generation for feed display
- Must prevent hotlinking and unauthorized sharing
- 100M+ uploads per day
Question: Design an upload system that prevents abuse while maintaining fast user experience.

### Solution

We will be using blob or object storage approach here with clients uploading photos and videos directly to object storage instead of API servers

Here's how we will re-architect it out.

- Client sends a request to upload a video or photo

- API server receives it, generates a pre signed url using storage credentials. It also makes an entry in the database for the storage url with a status of pending. The database will be storing the metadata for the videos and photos. We can bake in file size and content type in the presigned url. This is to ensure the user does not upload files greater than imposed file size. This also prevents users from uploading videos or executable if content type is an image.

- The API server returns the pre-signed url back to the client.

- The client uses the pre-signed url to upload the video or photo directly to the object store. The upload happens in small chunks, so that if at any point if upload fails, client can retry from the point the failure happened instead of starting from scratch. This is useful for unreliable mobile networks.

- Progress tracking comes naturally with chunked uploads. As each part completes, you know the percentage done. Simple client-side math gives you a nice progress bar to show users.

- As the chunks get uploaded, events get written to a message queue, A transcoding service picks the event, generates the thumbnail and stores it in blob.

- Once all the chunks, are uploaded, client sends another complete upload request to object store, the object store combines the chunks and stores them as a single file.

- Once file is uploaded, an event is written to the message queue. A quarantine service picks the event, and performs security checks and virus scanning in background.

- Once upload and thumbnail is completed, the object store sends a notification to the API server via message queue, the API server then uses the storage url in the notification to update the status to completed in metadata database along with the thumbnail url.

- The API server then sends a response back to the client that upload is completed and the thumbnail is immediately shown to the user with virus scanning being done in the background.

- Once the background virus scanning completes, the quarantine service can update a boolean field in the metadata database like `secured`. If any security check fails, the service goes ahead and deletes the file from the blob storage and the corresponding entry from the metadata table. Now here is one tradeoff in user experience, In case of failure scenario for security checks, the user will immediately see the thumbnail, but after a few seconds, they may not see the image they uploaded. This is fine because security comes first here.

- For downloads, we'd serve videos and photos through CloudFront CDN with signed URLs. This gives global distribution and prevents unauthorized access while keeping our servers out of the video delivery path. We will bake in access control in the presigned URLs, so as to restrict access to unauthorized users.

---