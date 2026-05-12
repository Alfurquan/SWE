# Problem

Given stream of logs with jobid, timestamps, event type as start and end, detect the first timeout that has occurred if the start and end of a job goes beyond a given threshold.

## Approach

So here would be my approach along with the data structure choice.

Once you as interviewer give a go ahead, I will code it out.

So we would be having stream of logs coming in. Each log would have a job_id, timestamp, event_type (This can be start or end). We need to find the job which will timeout first, by timeout we mean the job whose execution time has passed a certain threshold.

I would be using sorted sets to store the in progress jobs who are sorted in ascending order by the time they would timeout. So if lets say a job A's start log comes at T=2, and threshold = 10, it would timeout after 2+10 = 12, If another job B's start log comes at T=5, it would timeout after 5+10 = 15, so the set would be [(12, A), (15, B)].

I have not chosen heap to store it. I would discuss it once I explain my approach.

This is how the logic goes

- We maintain an in memory sorted set of inprogress jobs sorted in ascending order by the time they would timeout.
- We also maintain an in memory watermark time which tracks the latest timestamp the system has seen.
- Once a log message comes, we do the following
	- We update the watermark time to the timestamp of the log message
	- If sorted set is not empty, we take out the list of inprogress job from the set whose timeout time <= watermark.
	- Since the set is sorted by timeout times, we take the first job and return its id.
	- Now if the log message is of start event_type, we put the job_id from the log message and its timeout time in the sorted set.
	- If the log message is of end event_type, if the job_id is not in the sorted set -> It means it either timed out or it's start event_type log never came. We simply ignore this message. If the job_id is present in sorted set, we remove it as the job is completed without being timed out. In order to find the job_id in the sorted set, we can maintain a hash map of job_id to its timeout time, so that we can find the timeout time of the job_id in O(1) time and then remove it from the sorted set in O(logN) time.

Now we have not chosen min heap here because removing an element from min_heap would have taken O(N) time, whereas removing an element from sorted sets takes O(logN) time.