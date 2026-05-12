# The Problem: "The Distributed Task Scheduler"

Imagine you are building a system like Airflow or a Distributed Cron. You have thousands of tasks that need to be executed at specific times in the future.

The Task:
Implement a class TaskScheduler that allows users to schedule a function to run at a specific delay (in milliseconds) from the current time.

The API:

1. schedule(task_id: str, delay_ms: int):

- Schedules a task to be "ready" at current_time + delay_ms.

2. get_next_task() -> str:

- Returns the task_id of the task that is ready to run (i.e., its scheduled time has passed).

- If no task is ready, it should return None or wait (we can clarify this).

3. cancel_task(task_id: str):

- Removes a task from the schedule before it runs.

## Phase 1: Coding for single machine

### Approach:

#### Data structures used

- Sorted set: 
  - To keep track of tasks in order of their scheduled execution time.
  - This allows for efficient retrieval of the next task to run.

- Dictionary/HashMap:
  - To map task_id to its scheduled time for quick access and cancellation.

We have chosen sorted sets over heaps because sorted sets allow for efficient insertion, deletion, and retrieval of the next task in O(log n) time complexity. Heaps are also efficient but may require additional handling for task cancellation. Whereas with dictionary we can get the scheduled time of a task in O(1) time, and then compute the tuple (scheduled_time, task_id) to remove it from the sorted set in O(log n) time.

#### Logic:

- The `schedule` method will add the task to both the sorted set and the dictionary with its scheduled time. The scheduled time would be calculated as the current time plus the delay in milliseconds.
- The `get_next_task` method will check the sorted set for the task with the earliest scheduled time. If the current time is greater than or equal to that scheduled time, it will return the task_id and remove it from both the sorted set and the dictionary. If no tasks are ready, it will return None.
- The `cancel_task` would first check if task exists by checking it in the dictionary. If it exists, it will retrieve the scheduled time from the dictionary, create a tuple (scheduled_time, task_id), and remove it from the sorted set and the dictionary. It will also remove it from the dictionary to ensure it is no longer tracked.

## Phase 2: System Design (The "Distributed Scheduler")

Now, let's take this to the L5 Senior level. Imagine this is no longer a class in a single Python script. It is now a service used by 1,000 different microservices to schedule millions of tasks.

1. The "Missed Execution" Problem (Fault Tolerance)
Currently, your tasks live in the Python process memory.

Question: If the server crashes and restarts, all scheduled tasks are gone. How would you modify this to ensure persistence? Where would you store the SortedSet and the Dict so they survive a reboot?

2. The "Double Execution" Problem (Distributed Workers)We now have 10 servers running get_next_task().Scenario: A task is ready at $T=100$. Both Server A and Server B call get_next_task() at the exact same millisecond.Question: How do you ensure that exactly one server executes the task? (Think about the "Distributed Lock" or "Atomic Transaction" patterns we've discussed).

3. The "Waiting" Problem (Efficiency)
In your code, if no task is ready, get_next_task returns None. This means the caller has to "poll" (call the function over and over), which wastes CPU.

Question: If you were using a message broker or a specialized database (like Redis or a SQL DB), how could you make the worker sleep until the exact moment the next task is ready, rather than constantly checking?

## Answers

### 1. The "Missed Execution" Problem (Fault Tolerance)

We would keep our servers stateless so that we can scale horizontally. We would store the SortedSet and the Dict in a persistent storage system like a database (SQL or NoSQL) or a distributed cache like Redis. This way, if a server crashes, it can recover the scheduled tasks from the persistent storage upon restart.

We can choose redis for its sorted set data structure, which allows us to store tasks with their scheduled execution time as the score. This will allow us to efficiently retrieve the next task to run and also handle task cancellations.

### 2. The "Double Execution" Problem (Distributed Workers)

We can use a distributed lock mechanism to ensure that only one server can execute a task at a time. When a server retrieves the next task, it would attempt to acquire a lock on that task. If it successfully acquires the lock, it can proceed to execute the task. If another server tries to acquire the lock for the same task, it will fail and will not execute the task.

This can be implemented using Redis' SETNX command. This ensures that even if multiple servers call get_next_task() at the same time, only one will be able to execute the task. We can also set a TTL (time-to-live) on the lock to prevent deadlocks in case a server crashes while holding the lock.

### 3. The "Waiting" Problem (Efficiency)

To solve the waiting problem, we can move away from polling to a push based mechanism. When a worker tries fetching the next task, if no task is ready, it can sleep until the next task schedule time. It also subscribes to redis pub/sub system to get notified if a new task is scheduled before the next task's scheduled time. This way, the worker can wake up and check for tasks only when necessary, reducing CPU usage and improving efficiency. When a new task is scheduled, and if the scheduled time is earlier than the next task's scheduled time, the producer can publish a message to redis pub/sub channel to notify the workers to wake up and check for tasks. This way, we can ensure that workers are only active when there are tasks to execute, leading to better resource utilization.