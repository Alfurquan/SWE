# Smart Telemetry Suppressor

We are building a client-side SDK for a cloud monitoring platform. Applications use this SDK to report errors identified by an error code.

To reduce network bandwidth and avoid sending repetitive telemetry, duplicate errors should be suppressed for a configurable time window. If an error has not been emitted before, or its previous emission was sufficiently long ago, the event should be allowed through and the suppression window for that error should be reset.

### Example

Suppose the suppression window is 10 seconds.

| Timestamp | Error Code | Should Emit |
| --------- | ---------- | ----------- |
| 1         | ERR_A      | True        |
| 5         | ERR_A      | False       |
| 11        | ERR_B      | True        |
| 12        | ERR_A      | True        |
| 15        | ERR_A      | False       |

### Task

Design and implement a data structure that supports this functionality.

Please discuss the API you would design.

---

## What you are evaluating in the first 2–3 minutes

You are NOT checking code yet. You are checking:

1. Do they define an API?

Expected

```python
class TelemetrySuppressor:
    def __init__(window_size)
    def should_emit(timestamp, error_code)
```

2. Do they ask clarifying questions?

Good signals:

- “Is timestamp monotonic?”
- “Is suppression per error code?”
- “What is window unit?”

Bad signal:

- Immediately starts coding without clarifying anything

### If they don’t propose a class

You should nudge like this (after ~2 minutes max):

“Suppose we design this as a class. What methods and state would it have?”

This is a very standard L62 nudge.

### If they immediately start with a function, let them.

Then nudge like this:

- "Where would the state live if I wanted multiple suppressors with different window sizes?"
- "How would you package this as part of an SDK? Would you introduce a class?"

### If they still struggle

Then you become more explicit:

“You can assume a class with an initialization method and a function that takes timestamp and error code and returns a boolean.”

Now you are testing implementation, not API design.

## What you should NOT do

- Don’t give class structure upfront
- Don’t suggest HashMap immediately
- Don’t over-explain the solution

Because then you lose signal on:

- API design
- abstraction thinking
- problem decomposition

## Simple interviewer script (you can reuse)

Here is a clean flow you can literally follow:

### Step 1 (open)

“Design and implement a telemetry suppressor.”

### Step 2 (wait 2–3 min)

If they don’t define structure:

“How would you model this as a class?”

### Step 3 (if needed)

“What state would you maintain and what methods would you expose?”

### Step 4 (only if stuck)

“You can assume a method should_emit(timestamp, error_code) that returns a boolean.”

---

## One-line interpretation

- Weak → “Needs solution guidance”
- Average (L62 pass zone) → “Can solve with some nudges”
- Strong (L62+) → “Drives design + anticipates extensions”

---

# Follow-up 1: Memory Growth

## Candidate Option 1: Do Nothing

### Cons

* Memory grows forever.
* Space = O(total unique errors ever seen).

### Nudge

> Suppose this process runs for months and sees millions of unique errors. Is unbounded growth acceptable?

---

## Candidate Option 2: Background Cleanup Thread + Full Map Scan

### Approach

```text
Map<error, last_timestamp>

Background thread periodically:
    scan entire map
    remove expired entries
```

### Pros

* Simple.
* `should_emit()` remains O(1).

### Cons

* Periodic O(N) scans.
* Expired entries may remain longer than necessary.
* Additional synchronization with request threads.
* Doesn't scale well for very large maps.

### Nudge

> Suppose there are 100 million entries. Would scanning the entire map every minute still be efficient?

> Can cleanup cost depend only on the number of expired entries instead of the total map size?

---

## Candidate Option 3: Min Heap + Map

### Approach

```text
Map<error, last_timestamp>
MinHeap<(timestamp, error)>
```

### Pros

* Can efficiently find oldest entry.

### Cons

* Insert = O(log N)
* Delete = O(log N)
* More complex than necessary.

### Nudge

> Since timestamps arrive in order, do we really need a heap?

> Can we exploit monotonic timestamps?

---

## Candidate Option 4: Queue + Map (Expected)

### Approach

```text
Map<error, latest_timestamp>
Queue<(timestamp, error)>
```

Cleanup:

while oldest entry expired:
pop queue

```
if popped_timestamp == last_seen[error]:
    remove from map
```

### Pros

* O(1) amortized time.
* Space proportional to active window.
* No background thread.
* Cleanup proportional to expired entries.
* Simple and scalable.

### Key Insight

Monotonic timestamps mean oldest entries expire first, so FIFO order is sufficient.

---

## Good Nudges

> Can we avoid scanning the entire map?

> Can cleanup be proportional to the number of expired entries?

> How can we quickly find the oldest entry?

> Since timestamps are increasing, do we need a sorted structure?

> Is there a simpler structure than a heap?

---

## Signal

Background thread + scan:
✓ Acceptable

Heap + Map:
✓ Strong

Queue + Map:
✓✓ Very Strong

---

# Follow-up 2: Multi-dimensional Suppression

Question:

Suppression should happen independently for each combination of:

(service, machine_id, error_code)

For example, the same error emitted by two different machines and services should be treated independently.

How would you modify your design?

---

## Candidate Option 1: Nested Maps

### Approach

```text
Map<service,
    Map<machine,
        Map<error, timestamp>>>
```

### Pros

* Works.
* Easy to understand.

### Cons

* Verbose.
* Harder to maintain.
* Doesn't generalize well if another dimension is added.

### Nudge

> Suppose tomorrow we add region. Would you keep nesting maps?

> Can we treat the combination itself as the key?

---

## Candidate Option 2: Concatenated String Key

### Approach

```text
service + ":" + machine + ":" + error
```

### Pros

* Simple.
* Minimal changes.

### Cons

* Delimiter collisions.
* Brittle.
* Poor type safety.

### Nudge

> What if a field itself contains ':'?

> Can we represent the combination more explicitly?

---

## Candidate Option 3: Tuple / Pair / Triple

### Approach

```text
(service, machine, error)
```

used as the key.

### Pros

* Simple.
* Algorithm unchanged.
* Easy to extend.

### Cons

* Slightly less expressive.

### Signal

✓ Strong

---

## Candidate Option 4: Custom Key Class / Record

### Approach

```java
record EventKey(
    String service,
    String machineId,
    String errorCode
)
```

or

```java
class EventKey {
    service
    machineId
    errorCode

    equals()
    hashCode()
}
```

### Pros

* Clean abstraction.
* Immutable.
* Extensible.
* Type-safe.

### Signal

✓✓ Very Strong

### Nudge

> Can we encapsulate these dimensions into one object?

---

## Common Probe

If they create a custom class:

Ask:

> Suppose I create two EventKey objects with identical fields. Will HashMap treat them as the same key?

Expected:

Need equals() and hashCode().

(Java record automatically provides them.)

---

## Strong Signal

Candidate says:

"The algorithm doesn't change. Only the key changes."

That demonstrates separation of concerns and extensibility.

## Biggest thing you're testing

You're not testing whether they know Java records or tuples.

You're testing whether they realize:

The suppression logic stays the same. Only the identity of an event changes.

---

# Follow-up 3: Thread Safety

Question:

This SDK may be invoked concurrently from multiple threads.

Are there any race conditions to be aware of? How would you make this thread-safe?

---

## Candidate Option 1: No Synchronization

### Problem

Two threads execute:

```text id="pb3yxy"
get
check
update
```

simultaneously.

Both may decide to emit.

### Race

```text id="aj0gmk"
Thread 1: read timestamp=1
Thread 2: read timestamp=1

Both:
12 - 1 >= window

Both emit
```

### Signal

✗ Concern

### Nudge

> Can two threads both emit the same error?

---

## Candidate Option 2: ConcurrentHashMap

### Approach

```java id="3y58cb"
ConcurrentHashMap<EventKey, Integer>
```

### Pros

* Thread-safe map operations.

### Problem

Algorithm is:

```text id="2dzpij"
get
check
put
```

which is not atomic.

Duplicate emission still possible.

### Signal

✓ Average

### Nudge

> Is ConcurrentHashMap alone sufficient?

> Are get() and put() together atomic?

---

## Candidate Option 3: Global Lock

### Approach

Protect entire method:

```text id="v8cp20"
cleanup
check
update map
update queue
```

with one mutex.

### Pros

* Simple.
* Correct.
* Keeps map and queue consistent.

### Cons

* Contention under high throughput.

### Signal

✓✓ Strong

### Expected L62 Answer

> Map and queue together form one logical state, so I'd protect the whole operation with a lock.

---

## Candidate Option 4: ConcurrentHashMap + compute()

### Approach

```java id="v2l76f"
map.compute(...)
```

performs atomic updates for a key.

### Pros

* Solves duplicate emission race for map.

### Problem

Queue is still shared.

Map and queue can become inconsistent.

### Signal

✓✓ Strong

### Nudge

> What about the queue?

> Does the queue also need synchronization?

---

## Candidate Option 5: Sharding

### Approach

Partition by:

```text id="0zmzll"
hash(key) % N
```

Each shard has:

```text id="7h2u54"
lock
map
queue
```

### Pros

* Parallelism.
* Reduced contention.

### Signal

✓✓✓ Exceptional

---

## Strong Probe

If candidate says ConcurrentHashMap:

Ask:

> Is that sufficient?

If candidate says yes:

Ask:

> Can two threads still both emit the same error?

If candidate says compute():

Ask:

> What about consistency between map and queue?

---

## Key Insight

Thread-safe containers ≠ thread-safe algorithm.

The whole transaction:

```text id="icg3ew"
cleanup
↓
check
↓
update map
↓
update queue
```

must be atomic.

---

## Signal Summary

| Answer                      | Signal      |
| --------------------------- | ----------- |
| No race conditions          | Concern     |
| ConcurrentHashMap only      | Average     |
| Global lock                 | Strong      |
| ConcurrentHashMap + compute | Strong      |

Biggest thing to remember as an interviewer

You are not looking for sharding or lock-free structures.

If a candidate says:

"Map and queue form one logical state, so I'd put a mutex around the whole should_emit() method."

---