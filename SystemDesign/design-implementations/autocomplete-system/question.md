# 💻 Phase 1: Coding / Algorithmic Design (Individual Machine)

“Imagine you’re working on an autocomplete feature — for example, the search bar in Google, Gmail, or YouTube. As a user types characters, you want to suggest the top-k most relevant completions based on historical query frequency.”

## Problem Statement

You’re given:

- A set of strings representing previously searched queries.
- Each query has an associated frequency (number of times it was searched).
- A stream of input characters (typed one at a time by the user).

Your task:

Design a data structure that supports:

- insert(query, frequency) — inserts or updates a query and its frequency.
- getSuggestions(prefix, k) — returns the top k most frequent queries that start with prefix.

Optimize for real-time performance (the user expects <100ms latency per keystroke).

## Follow-ups:

- How would you handle ties in frequency?
- How would you make it case-insensitive?
- What’s the time/space complexity of your operations?

---

# 🏗️ Phase 2: System Design (Distributed, Scalable Autocomplete)

“Now imagine you have to build this autocomplete feature for Google Search, where billions of queries are made daily and millions of users type simultaneously.”

High-Level Design Goals

Design a scalable, fault-tolerant, and low-latency system that:

- Supports real-time suggestions as the user types.
- Updates rankings dynamically based on query popularity trends.
- Provides personalized results (optional follow-up).
- Has Strong avaialbility

You should discuss:

- Functional requirements and non-functional requirements
- API design and query flow (frontend → backend → datastore)
- Data model — how queries, frequencies, and user preferences are stored
- Caching and indexing strategy (e.g., Trie, prefix tree, inverted index, etc.)
- Scaling and sharding (how to partition data across servers)
- Real-time updates — how to update frequencies and propagate to replicas
- Consistency and availability trade-offs (CAP)
- Latency optimization — where and how caching/CDN/edge computing comes in
- Failure handling and monitoring