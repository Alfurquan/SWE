# Schema Evolution — Interview-Ready Notes

## What Is Schema Evolution?

The ability to change the structure of your data (add/remove/rename fields, change types) without breaking existing producers, consumers, or stored data. Essential in any system where multiple services or versions coexist.

## Three Compatibility Directions

**Backward Compatible (most common requirement):**
- New code (reader) can read old data
- Achieved by: adding fields with default values, never removing required fields
- Example: You add a `device_type` field to your view event. New Spark consumer reads old events → `device_type` is null/default. No crash.

**Forward Compatible:**
- Old code (reader) can read new data
- Achieved by: readers skip/ignore unknown fields
- Example: Old consumer deployed a week ago encounters a new field `device_type` it doesn't know about → ignores it, continues working.

**Full Compatible (gold standard):**
- Both directions simultaneously
- Rule: only add optional fields with defaults. Never delete. Never change types. Never reuse field numbers/names.

## Serialization Format Comparison

| Format | Schema evolution support | Used where |
|--------|------------------------|-----------|
| **Protobuf** | Excellent. Field numbers are stable. Unknown fields preserved. | gRPC, internal service communication |
| **Avro** | Excellent. Writer schema stored with data. Reader resolves diffs at read time. | Kafka, data lakes, Hadoop ecosystem |
| **JSON** | Poor. No schema enforcement. Consumers break on unexpected types/missing fields. | REST APIs (use with caution) |
| **Thrift** | Good. Similar to Protobuf. | Legacy systems (Facebook origin) |

## Schema Registry (Kafka Context)

**What it does:**
- Central store of all schema versions for each topic
- Producers register schema before publishing; registry assigns a schema ID
- Consumers fetch schema by ID to deserialize
- Registry enforces compatibility rules (rejects breaking changes)

**How it works in practice:**
```
Producer → registers schema v2 with registry
        → registry checks: is v2 backward-compatible with v1? 
        → if yes: assigns ID, producer publishes with schema ID in header
        → if no: rejects registration, producer deploy fails (good — caught early)

Consumer → reads message, extracts schema ID from header
         → fetches schema v2 from registry
         → deserializes using v2, projects onto its expected schema
```

**Key point:** The registry acts as a *gate* — breaking changes are caught at deploy time, not at runtime in production.

## Safe vs Unsafe Changes

**Always safe (backward + forward compatible):**
- Add an optional field with a default value
- Add a new enum value (if readers handle unknown values)
- Deprecate a field (stop writing, keep in schema)

**Unsafe (breaks compatibility):**
- Remove a required field
- Rename a field (old readers can't find it)
- Change a field's type (int → string)
- Reuse a deleted field number (Protobuf) or name (Avro)
- Change a field from optional to required

**Risky but manageable:**
- Add a required field → only backward compatible if it has a default
- Remove an optional field → only forward compatible (old data still has it)

## API Versioning (REST/gRPC)

**REST approaches:**

| Strategy | Example | Trade-off |
|----------|---------|-----------|
| URL versioning | `/v1/videos`, `/v2/videos` | Simple, explicit. Requires routing logic. |
| Header versioning | `Accept: application/vnd.api.v2+json` | Cleaner URLs. Harder to test/debug. |
| Query param | `/videos?version=2` | Easy but messy. |

**Best practice for interviews:**
> "I'd use URL versioning for major breaking changes (v1 → v2). Within a version, I'd evolve additively — new optional fields, new endpoints. Old clients ignore fields they don't recognize. I'd deprecate old versions with a sunset header and monitoring on usage."

**gRPC/Protobuf:**
- Wire format inherently handles evolution (field numbers are stable)
- Add new fields → old clients ignore them
- Never reuse field numbers
- Use `reserved` keyword to prevent accidental reuse of deleted fields

## Storage Layer Evolution

**Parquet/Delta Lake:**
- Schema stored in file metadata
- Adding columns: new files have the column, old files return null when queried
- Removing columns: just stop writing them, old data still has them (schema-on-read)
- Delta Lake: `mergeSchema` option allows automatic schema evolution on write
- Type changes: generally unsafe — requires rewriting data

**Event sourcing / Kafka long-term storage:**
- Events written months ago are in schema v1, current is v5
- Avro's writer/reader schema resolution handles this: reader says "I expect fields A, B, C, D, E." Old event has A, B, C → D, E filled with defaults.
- Never need to migrate old events in place — schema-on-read resolves at query time

## The "Backfill After Schema Change" Scenario

> Interviewer: "You deployed a bug fix and need to reprocess 30 days of events from Kafka. But the schema changed twice in those 30 days. How do you handle it?"

Answer:
> "Each event in Kafka carries its schema ID in the header. My reprocessing job fetches the correct schema version for each event from the registry, deserializes with the writer's schema, then maps it to the current internal model. Fields that didn't exist in old versions get defaults. Fields that were removed in newer versions are ignored. This is schema-on-read — I never need to rewrite historical data."

## When to Bring This Up in an Interview

**Proactively (one sentence) when you mention:**
- Kafka: "Events are serialized in Avro with a schema registry enforcing backward compatibility, so producers and consumers can evolve independently."
- Storage: "Parquet files in Delta Lake — schema evolution is handled by additive changes with `mergeSchema`."
- APIs: "I'd version the API at the URL level for breaking changes, and evolve additively within a version."

**If asked to go deeper:**
- Explain backward/forward/full compatibility
- Give the safe/unsafe change list
- Describe the registry's role as a compatibility gate

**Don't go deeper than this unless explicitly asked.** Schema evolution is a 2-minute supporting point, not a 15-minute deep dive.

## One-Sentence Cheat Sheet

> "Use Avro/Protobuf + schema registry. Only add optional fields with defaults. Registry rejects breaking changes at deploy time. Readers project their schema onto data — handles version mismatch at read time without data migration."
