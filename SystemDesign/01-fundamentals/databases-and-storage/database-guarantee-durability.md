# How Databases Guarantee Durability (Even After Crashes) ?

One of the things that make databases truly powerful is their ability to protect your data even in the face of unexpected failures.
This promise is known as Durability — one of the four essential ACID properties of databases.

## Key techniques to ensure durability

### Write ahead logging (WAL)

One of the most fundamental techniques databases use to guarantee durability is called Write-Ahead Logging (WAL).

The idea is simple

```text
Always write changes to a log file first, before updating the main data files.
```

This simple-looking step is powerful

It gives the database a persistent, chronological record of every change, which can later be replayed to recover the exact state after a crash.

#### How WAL ensures durability ?

- Log the change
Whenever the database needs to perform a change, such as an INSERT, UPDATE, or DELETE, it first creates a detailed record in a sequential append-only log file called the WAL (or sometimes a commit/redo log).

This write is typically done in memory first, making it fast and efficient.

Example WAL record

```shell
LSN: 0/01000050
Record Type: INSERT
Table: public.users
Page: 2003
Tuple ID: (0, 5)
Inserted Values:
    id = 101
    name = 'Alice'
    email = 'alice@example.com'
Transaction ID: 5001
```

LSN (Log Sequence Number) uniquely identifies the position of the record in the WAL.
Record Type describes the operation (in this case, an INSERT).
Other details specify exactly what changed, where it changed, and under which transaction.

- Flush the log to the disk

After creating the WAL record in memory, the database flushes it to durable disk storage. Only after the WAL record is safely written to disk does the database consider the change durable. Even if the database server crashes immediately after this step, the change is preserved on disk and can be used for recovery.

- Acknowledge the commit

Once the WAL record is durably stored on disk, the database sends a "Success" response back to the client.

At this point:

The transaction is officially considered committed and durable.
The client can safely move on, confident that the change will not be lost.
The main data files (such as tables or indexes) may not have been updated yet, but that is acceptable because the WAL contains everything needed to recover the change.

- Update in-memory Data Pages

After acknowledging the commit, the database may also update in-memory versions of the affected data pages.

- Apply Changes to Data Files (Later)

Writing the actual updated pages to the database’s main data files happens later, typically through background processes like:

Checkpointing
Lazy background flushes

- Crash Recovery via WAL

If the database crashes at any point, here's what happens during restart:

1. The database reads the WAL starting from the last known checkpoint.
2. It replays any committed transactions that were recorded in the WAL but not yet fully applied to the data files.
3. It restores the database to a consistent, committed state it was in just before the crash.

### Checkpointing

While WAL protects committed data against crashes, relying on WAL alone is not practical in the long run.

Imagine a database that runs for months without any cleanup, constantly appending to the WAL.If the system crashes, it would need to replay millions or even billions of operations from the beginning just to recover.

That recovery could take hours or even days, making the system unusable for a long time.

This is where Checkpointing comes in.

#### What is a Checkpoint ?

A checkpoint is a point-in-time snapshot where the database ensures that all changes up to that moment are fully written to the main data files.

At a checkpoint, the database synchronizes its data files with its log files up to a specific position called the Log Sequence Number (LSN).

This creates a save point in the system, so that if a crash happens, the database can start recovery from the latest checkpoint instead of from the very beginning.

Checkpointing solves two major problems:

- It reduces crash recovery time by limiting the amount of WAL that needs to be replayed after a failure.
- It keeps WAL file size manageable by allowing the system to delete or archive old, unnecessary logs.

### Replication

For truly resilient systems especially in distributed databases and high-availability architectures, we need Replication.

Replication simply means:

Keeping extra copies of your data on separate machines or separate storage so that even if one copy is lost, another remains available.
