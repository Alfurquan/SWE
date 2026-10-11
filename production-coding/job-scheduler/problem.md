# Job Scheduler

Design and implement a Job Scheduler.

Core API:

- schedule(job, run_at) → schedule a job to run at a specific time (or after a delay)
- cancel(job_id) → cancel a scheduled job before it runs
- A background mechanism executes each job at (or shortly after) its scheduled time

## Requirements:

- Many jobs scheduled for different times; the scheduler runs each at the right time.
- Jobs execute via some worker mechanism (like pub/sub's handle, a job has a run() or is a callable).
- Minimal on purpose — part of the signal is what you clarify and what you volunteer.