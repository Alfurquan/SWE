# LSM Tree — Complete Deep Dive

## Part 1: The Fundamental Problem

You're building a database. You need to store key-value pairs on disk and support:
- `put(key, value)` — store/update a key
- `get(key)` — retrieve a value
- `range(start, end)` — get all keys in a range
- `delete(key)` — remove a key

The naive approach: keep an unsorted file, append writes to the end.
- Writes: O(1) — just append. Great.
- Reads: O(n) — scan the entire file. Terrible.

The B-tree approach: keep a sorted on-disk tree structure (used by PostgreSQL, MySQL).
- Reads: O(log n) — traverse the tree. Great.
- Writes: O(log n) but with **random I/O** — you must find the right page and update it in-place.

**LSM trees ask**: what if we optimize for writes first, and make reads "good enough"?

---

## Part 2: Building Up from a Simple Log

### The Append-Only Log (Bitcask model)

Simplest possible storage:
```
file.db:
  [key1:value1][key2:value2][key1:value_updated][key3:value3]
```

- Write = append to end of file. Sequential. Fast.
- Read = scan from end to beginning, find most recent entry for key. Slow.
- Keep an **in-memory hash index**: `{key → byte offset in file}`. Now reads are O(1).

**Problem**: the hash index must fit in RAM. If you have billions of keys, this doesn't work. Also, range queries require scanning everything.

### The Insight: What if the file was sorted?

If keys are in sorted order on disk, you get:
1. Binary search for point lookups — no need to index every key
2. Efficient range scans — just read contiguously
3. Efficient merging of multiple files — merge-sort

But you can't keep an append-only file sorted — that would require inserting in the middle (random I/O).

**Solution**: sort in memory, then write sorted chunks to disk.

---

## Part 3: The LSM Tree Architecture

### Component 1: The Write-Ahead Log (WAL)

```
Every write → immediately append to WAL file on disk
```

This is a crash-safety mechanism. The WAL is:
- Append-only (fast sequential write)
- Unsorted (just records operations in order)
- Purely for durability — if the process crashes, replay the WAL to recover

The WAL is **not** used for reads. It exists only so you don't lose the memtable contents on crash.

### Component 2: The Memtable

```
Write also → insert into an in-memory sorted data structure
```

The memtable is typically a:
- Red-black tree, or
- AVL tree, or
- Skip list (used by LevelDB/RocksDB — simpler concurrent access)

**Properties:**
- All keys are kept sorted in memory
- Supports O(log n) insert and O(log n) lookup
- Has a size limit (e.g., 4MB, 64MB — configurable)

**Every write goes to both WAL and memtable simultaneously.**

### Component 3: SSTables (Sorted String Tables)

When the memtable fills up:

```
Memtable (full, sorted in memory)
    │
    ▼ in-order traversal → sequential write to disk
    │
SSTable file (sorted key-value pairs, immutable)
```

An SSTable file looks like this on disk:

```
┌─────────────────────────────────────────────────────────┐
│ Data Block 0: [aardvark:v1] [apple:v2] [avocado:v3]    │
│ Data Block 1: [banana:v4] [berry:v5] [blueberry:v6]    │
│ Data Block 2: [cherry:v7] [coconut:v8] [cranberry:v9]  │
│ ...                                                     │
│ Data Block N: [zebra:v99]                               │
├─────────────────────────────────────────────────────────┤
│ Index Block: [aardvark→offset0, banana→offset1,         │
│               cherry→offset2, ..., zebra→offsetN]       │
├─────────────────────────────────────────────────────────┤
│ Bloom Filter Block                                      │
├─────────────────────────────────────────────────────────┤
│ Footer (metadata, offsets to index & filter)            │
└─────────────────────────────────────────────────────────┘
```

**Critical properties of SSTables:**
1. **Immutable** — once written, never modified. Only deleted entirely.
2. **Sorted** — keys are in lexicographic order.
3. **Block-structured** — data is split into blocks (4-64KB each), each block is independently compressed.
4. **Sparse index** — the index block stores the first key of each data block + its offset. You don't index every key, just one per block.
5. **Bloom filter** — a compact structure that answers "is this key possibly in this file?" (false positives allowed, false negatives never).

### After the flush:

```
Memory:                 Disk:
┌──────────────┐       ┌──────────────┐
│ New Memtable │       │ WAL (new)    │
│ (empty)      │       ├──────────────┤
└──────────────┘       │ SSTable-3    │ ← newest
                       │ SSTable-2    │
                       │ SSTable-1    │ ← oldest
                       └──────────────┘
```

The old WAL is discarded (its data is now safely in the SSTable). A new empty WAL and memtable begin.

---

## Part 4: The Read Path (In Full Detail)

To read key `K`:

```
Step 1: Check Memtable
   └─ Key found? → Return value. Done.
   └─ Not found? → Continue.

Step 2: Check SSTable-3 (most recent)
   └─ Check Bloom filter: "Could K be in this file?"
      └─ Bloom says NO → Skip this file entirely. Go to Step 3.
      └─ Bloom says MAYBE → Continue.
   └─ Binary search the sparse index → find the data block that could contain K
   └─ Read that one data block from disk (one I/O)
   └─ Scan within the block for K
      └─ Found? → Return value. Done.
      └─ Not found? → Continue.

Step 3: Check SSTable-2
   └─ (same process)

Step 4: Check SSTable-1
   └─ (same process)

Step 5: Key not found in any SSTable → Return "not found"
```

**Why Bloom filters are critical**: Without them, a read for a non-existent key would require reading a block from EVERY SSTable. With Bloom filters (typically 10 bits per key, <1% false positive rate), you skip most files without any disk I/O.

**Why newest-to-oldest order matters**: If the same key was written multiple times, the newest SSTable has the latest value. Once you find the key, you stop — no need to check older files.

---

## Part 5: Deletes — The Tombstone Mechanism

You can't just remove a key from an SSTable (they're immutable). Instead:

```
delete("apple") → put("apple", TOMBSTONE)
```

A tombstone is a special marker that says "this key is deleted."

During reads:
- If you find a tombstone for key K in SSTable-3, you return "not found" — even if SSTable-1 has an older valid value for K.

During compaction:
- When the tombstone and the original value end up in the same compaction, both are discarded.
- **But**: you can only discard the tombstone when you're sure no older SSTable contains that key. In leveled compaction, this means the tombstone must reach the lowest level before it can be removed.

---

## Part 6: Compaction — The Heart of the System

Without compaction, you'd accumulate infinite SSTable files. Reads would get progressively slower (more files to check). Disk space would grow unbounded (old versions of updated keys still take space).

### How Compaction Works (The Merge)

Take two sorted SSTables and merge them into one:

```
SSTable-A: [apple:3, cherry:7, fig:2]
SSTable-B: [banana:5, cherry:9, date:1]
                         ↑ duplicate key!

Merge (keep newer value for duplicates):
Result:    [apple:3, banana:5, cherry:9, date:1, fig:2]
```

This is exactly **merge-sort's merge step** — O(n) time, sequential reads from both inputs, sequential write to output. Three sequential I/O streams = very efficient.

### Strategy 1: Size-Tiered Compaction

```
Level concept (but not strict):
- Small SSTables (recent flushes) accumulate
- When you have ~4 similar-sized SSTables, merge them into one larger one
- When you have ~4 of those larger ones, merge into an even larger one

Looks like:
  4MB, 4MB, 4MB, 4MB → merge → 16MB
  16MB, 16MB, 16MB, 16MB → merge → 64MB
  64MB, 64MB, 64MB, 64MB → merge → 256MB
```

**Pros:**
- High write throughput (less total I/O spent on compaction)
- Simple to implement

**Cons:**
- Space amplification: during compaction, you temporarily have both old and new files
- A single key might exist in multiple SSTables at different size tiers
- Reads may check many files → slower reads

**Used by**: Cassandra (default), HBase

### Strategy 2: Leveled Compaction

```
Level 0:  SSTable SSTable SSTable  (direct flushes, may overlap)
              │
              ▼ compaction
Level 1:  [aaa─ddd] [eee─hhh] [iii─mmm] [nnn─zzz]  (non-overlapping ranges)
              │
              ▼ compaction
Level 2:  [aaa─bb] [cc─dd] [ee─ff] ... [yy─zz]  (10x more files, non-overlapping)
              │
              ▼
Level 3:  (100x more files, non-overlapping)
```

**Rules:**
- Level 0: SSTables are flushed directly from memtable. They CAN have overlapping key ranges.
- Level 1+: SSTables within a level have **non-overlapping key ranges**. Each key exists in exactly ONE file per level.
- Each level is ~10x the size of the previous level.
- Compaction picks one SSTable from level N, finds all overlapping SSTables in level N+1, merges them, writes new SSTables back to level N+1.

**Example compaction step:**
```
Level 1: [aaa─fff]  [ggg─mmm]  [nnn─zzz]
Level 2: [aaa─bbb] [ccc─ddd] [eee─fff] [ggg─hhh] [iii─jjj] ...

Pick [aaa─fff] from L1.
It overlaps with [aaa─bbb], [ccc─ddd], [eee─fff] in L2.
Merge all 4 files → produce new sorted files for L2.
Delete the originals.
```

**Pros:**
- A key exists in at most one file per level → reads check at most one file per level
- Bounded space amplification (~10% overhead)
- Predictable read performance

**Cons:**
- Higher write amplification (a single write may be rewritten ~10-30 times as it moves through levels)
- More compaction I/O

**Used by**: LevelDB, RocksDB, Cassandra (optional)

---

## Part 7: Write Amplification — The Key Tradeoff

Write amplification = (total bytes written to disk) / (bytes of original data written by user)

**In leveled compaction:**
- A key is written to memtable → flushed to L0 (1 write)
- Compacted from L0 → L1 (rewritten)
- Compacted from L1 → L2 (rewritten)
- Compacted from L2 → L3 (rewritten)
- ... down to the final level

With a size ratio of 10 and worst case, a key at level N gets merged with up to 10 files from level N+1. Across all levels, write amplification is roughly **10 × number_of_levels** in the worst case (typically 10-30x in practice).

**Why this is acceptable**: each compaction write is sequential. 30 sequential writes are still faster than 1 random write in many cases on HDDs. On SSDs, it's a real concern and why RocksDB has many tuning knobs.

---

## Part 8: Concurrency — Why Immutability Helps

SSTables are immutable. This means:
- **Readers never block writers**: a read can scan an old SSTable even while compaction creates a new one.
- **Writers never block readers**: a flush creates a NEW file; old files remain readable.
- **No locks on data files**: you only need coordination on the metadata (which files are current).
- **Compaction is invisible to readers**: once new merged files are ready, atomically update the metadata to point to them, then delete old files.

The memtable is the only mutable structure and needs concurrency control (this is why skip lists are popular — they support concurrent inserts without global locks).

---

## Part 9: Putting It All Together — The Full Picture

```
                    ┌─────────────┐
   write(k,v) ────►│     WAL     │ (crash recovery)
        │           └─────────────┘
        │
        ▼
  ┌───────────────┐
  │   Memtable    │  (sorted, in memory, mutable)
  │  (skip list)  │
  └───────┬───────┘
          │ size threshold exceeded
          ▼
  ┌───────────────┐
  │  Level 0      │  SSTables (possibly overlapping)
  │  (immutable)  │
  └───────┬───────┘
          │ compaction
          ▼
  ┌───────────────┐
  │  Level 1      │  SSTables (non-overlapping, ~10MB total)
  └───────┬───────┘
          │ compaction
          ▼
  ┌───────────────┐
  │  Level 2      │  SSTables (non-overlapping, ~100MB total)
  └───────┬───────┘
          │ compaction
          ▼
  ┌───────────────┐
  │  Level 3      │  SSTables (non-overlapping, ~1GB total)
  └───────────────┘

  Read path: Memtable → L0 (all files) → L1 (1 file) → L2 (1 file) → L3 (1 file)
                         ↑                  ↑              ↑              ↑
                    Bloom filter        Bloom filter    Bloom filter   Bloom filter
```

---

## Part 10: Why Flushing Memtable to SSTable is Fast

### The Problem with Random Writes

On a spinning disk, each random write requires:
1. **Seek** — move the disk head to the right track (~4-10ms)
2. **Rotate** — wait for the right sector to spin under the head (~2-4ms)
3. **Transfer** — actually write the data (~microseconds)

Even on SSDs, random writes are slow because:
- SSDs can't overwrite — they must **erase** an entire block (128-512KB) then rewrite it
- Random small writes trigger **write amplification** inside the SSD's flash translation layer

### Why the Memtable Flush is Different

The memtable is a sorted in-memory tree. When you flush it:
1. You **in-order traverse** the tree — gives all keys in sorted order
2. You write them **one after another** into a single new file — pure sequential I/O

```
Memtable (in memory, sorted):
  [apple→3, banana→7, cherry→1, dog→9, egg→2]

Write to disk as one contiguous stream:
  → | apple:3 | banana:7 | cherry:1 | dog:9 | egg:2 | EOF
     ←————————— one sequential write ——————————————→
```

The disk head moves in one direction only. No seeking. One system call, one contiguous chunk.

### The Numbers

| Operation | HDD | SSD |
|-----------|-----|-----|
| Random write (4KB) | ~100 IOPS → 0.4 MB/s | ~10K-50K IOPS |
| Sequential write | ~100-200 MB/s | ~500-3000 MB/s |

Flushing a 4MB memtable sequentially:
- **Sequential**: 4MB ÷ 200 MB/s = **~20ms** on HDD
- **Random (4KB writes)**: 1000 writes × 10ms seek = **~10 seconds** on HDD

That's a **500x difference**.

---

## Part 11: Summary — What to Articulate in a Google Interview

1. **Writes are fast** because they go to memory (memtable) + sequential append (WAL). Never random I/O on the write path.

2. **Memtable flush is efficient** because you're writing a pre-sorted batch of data as one sequential stream to disk.

3. **SSTables are immutable and sorted**, enabling merge-sort-based compaction, lock-free concurrent reads, and sparse indexing.

4. **Reads check multiple levels** but are made practical through Bloom filters (skip files entirely) and sparse indexes (minimize disk reads per file).

5. **Compaction trades write amplification for bounded read amplification and space reclamation.** The choice between size-tiered and leveled compaction depends on your workload (write-heavy vs. read-heavy).

6. **Deletes use tombstones** — a delete is actually a write. Space is only reclaimed during compaction.

7. **The fundamental tradeoff**: LSM trees give you 10-100x better write throughput than B-trees, at the cost of higher read latency (especially worst-case/p99) and background compaction resource usage.

---

## Key Tradeoffs Table

| Aspect | LSM Tree | B-Tree |
|--------|----------|--------|
| **Writes** | Fast (sequential, append-only) | Slower (random I/O, page splits) |
| **Reads** | Slower (check multiple SSTables) | Fast (single tree traversal) |
| **Write amplification** | Can be high due to compaction | Lower per-write, but page rewrites |
| **Space amplification** | Temporary duplication during compaction | Fragmentation in pages |
| **Compaction interference** | Can impact latency at p99 | No background process |

---

## Real-World Systems Using LSM Trees

- **Google Bigtable** → the original
- **LevelDB** → Google's single-node implementation
- **RocksDB** → Facebook's fork of LevelDB (more features, better performance)
- **Apache Cassandra** → distributed, supports both compaction strategies
- **HBase** → Hadoop-based, size-tiered
- **InfluxDB** → time-series variant (TSM trees)
- **CockroachDB** → uses RocksDB/Pebble as storage engine
