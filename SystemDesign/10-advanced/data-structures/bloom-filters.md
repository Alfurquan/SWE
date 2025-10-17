# Bloom Filters

A bloom filter is a probabilistic data structure which is analogous to a set (refresher: sets allow you to insert elements and check their membership).

The most common implementation of a set uses a hash table. With a hash table we can insert elements in O(1) time and check membership in O(1) time. Very fast! Unfortunately, we need to have memory for each possible element in a hash table, which is infeasible for very large sets. Imagine we had trillions of items and we wanted to keep track of all their ids.

Bloom filters help us here by making a compromise. They are dramatically more memory efficient than hash tables but relax the guarantees of a set. Bloom filters can tell you:

- Whether an element is likely in a set, with some configurable probability
- When an element is definitely not in a set

## How it Works ?

For each element we insert, we'll hash its value k times, using k different hash functions.
If we set the bit to 1 at each of these positions, we get a bitmask.

A Bloom filter is a bit array of size `m` and uses `k` independent hash functions. When adding an item, each hash function maps the item to a position in the array and sets that bit to 1. To check membership, the item is hashed with all `k` functions; if all bits are 1, the item is possibly in the set (false positives possible), if any bit is 0, the item is definitely not in the set.

## Use Cases

The use-cases for a bloom filter meet three conditions:

- You need to be querying for membership in a set.
- You need to be space constrained (otherwise just use a hash table!).
- You need to be able to tolerate a false positive rate.

In practice, while (1) is common, (2) is rarer for many systems as a hard constraint, and (3) is difficult to design around. The most common use-cases in an interview setting we see overlap with caching.

Another thing to note is that standard bloom filters do not support removing elements. The "stamp" is permanent! As a result, they're not great for sets where items are updated or removed commonly.

### Web Crawling

With web crawling, we're traversing a gigantic graph of web pages. We want to make sure we're not wasting work crawling the same page over and over, but don't want to waste excessive memory storing all the pages we've already seen.

URLs can be large and the set of all crawled URLs can be massive, so storing all of the visited URLs in a hash table can be cumbersome. Additionally, missing a page may be acceptable for our crawler, we can tolerate some false positives. This is a great use-case for a bloom filter.

Instead of keeping a hash table of all the visited URLs, we can have a centralized bloom filter. This will allow us to make a statement like "we've probably seen this URL before" without having to store the full URL itself.
Cache Optimizations

### Cache Optimizations

With most caches, we're storing the result of an expensive calculation in a cache, using a distributed cache like Redis or Memcached. A common pattern is to first check the cache to see if it has the result we're looking for and, if it doesn't, we can fire off the expensive calculation, store the result in the cache, and then return it to the user.

Most caches are very fast (single digit millisecond latency), but even so we're adding a small amount of time to all requests to check the cache. This dramatically speeds up cache hits and saves our expensive operation from being run needlessly, but adds even more latency to cache misses. If the time to hit the cache is C milliseconds, and the time for the expensive operation is E milliseconds, cache misses take C+E milliseconds.

Can we improve this? Behold our trusty bloom filter. When we get a request we can check our bloom filter. If the item is definitely not in the cache, we can skip straight to running our expensive operation directly. If it's possible it's in the cache, we fall back to the previous behavior of checking the cache first.

**Two things should be noted here. First: most caches support an eviction policy like a Time to Live (TTL). Our bloom filter explicitly does not support removal of items so will become less accurate over time.
Secondly: most caches have multiple clients/writers. If we're using a bloom filter to shortcut cache checks, we may be missing out on potential cache hits where other clients have already written the result to the cache.
Tradeoffs!**
