# Concurrency vs Parallelism

Concurrency and parallelism are two of the most misunderstood concepts in system design.

## What is concurrency ?

Concurrency means an application is making progress on more than one task at the same time. While a single CPU can work on only one task at a time, it achieves concurrency by rapidly switching between tasks.
For example, consider playing music while writing code. The CPU alternates between these tasks so quickly that, to the user, it feels like both are happening at the same time.

Concurrency is primarily achieved using threads, which are the smallest units of execution within a process. The CPU switches between threads to handle multiple tasks concurrently, ensuring the system remains responsive.

### How does concurrency work ?

Concurrency in a CPU is achieved through context switching.

- Context Saving: When the CPU switches from one task to another, it saves the current task's state (e.g., program counter, registers) in memory.

- Context Loading: The CPU then loads the context of the next task and continues executing it.

- Rapid Switching: The CPU repeats this process, switching between tasks so quickly that it seems like they are running simultaneously.

## What is parallelism ?

Parallelism means multiple tasks are executed simultaneously. To achieve parallelism, an application divides its tasks into smaller, independent subtasks. These subtasks are distributed across multiple CPUs, CPU cores, GPU cores, or similar processing units, allowing them to be processed in parallel.

### How does Parallelism Works?

Modern CPUs consist of multiple cores. Each core can independently execute a task. Parallelism divides a problem into smaller parts and assigns each part to a separate core for simultaneous processing.
