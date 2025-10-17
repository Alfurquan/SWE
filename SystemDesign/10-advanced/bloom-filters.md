# Bloom filters

Have you ever wondered how Netflix knows which shows you've already watched? Or how Amazon avoids showing you products you've already purchased?
Using a traditional data structure like a hash table for these checks could consume significant amount of memory, especially with millions of users and items.
Instead, many systems rely on a more efficient data structure—a Bloom Filter.

## What is a Bloom Filter ?

- A Bloom Filter is a probabilistic data structure that allows you to quickly check whether an element might be in a set.
- It’s useful in scenarios where you need fast lookups and don’t want to use a large amount of memory, but you’re okay with occasional false positives.

### Key components of a bloom filter

- Bit Array: The Bloom Filter consists of a bit array of a fixed size, initialized to all zeros. This array represents whether certain elements are in the set.
- Hash Functions: To add or check an element, a Bloom Filter uses multiple hash functions. Each hash function maps an element to an index in the bit array.

## How does a bloom filter work ?

A Bloom filter works by using multiple hash functions to map each element in the set to a bit array.

1. Initialization

- A Bloom filter starts with an empty bit array of size m (all bits are initially set to 0).
- It also requires k independent hash functions, each of which maps an element to one of the m positions in the bit array.

2. Inserting an Element

- To insert an element into the Bloom filter, you pass it through each of the k hash functions to get k positions in the bit array.
- The bits at these positions are set to 1.

3. Checking for Membership

- To check if an element is in the set, you again pass it through the k hash functions to get k positions.
- If all the bits at these positions are set to 1, the element is considered to be in the set (though there's a chance it might be a false positive).
- If any bit at these positions is 0, the element is definitely not in the set.

## Real world applications of bloom filters

### Web Caching

**Problem:** Web servers often cache frequently accessed pages or resources to improve response times. However, checking the cache for every resource could become costly and slow as the cache grows.

**Solution:** A Bloom Filter can be used to quickly check if a URL might be in the cache. When a request arrives, the Bloom Filter is checked first. If the Bloom Filter indicates the URL is “probably in the cache,” a cache lookup is performed.

If it indicates the URL is “definitely not in the cache,” the server skips the cache lookup and fetches the resource from the primary storage, saving time and resources.

### Databases

**Problem:** Databases, especially distributed ones, often need to check if a key exists before accessing or modifying data. Performing these checks for every key directly in the database can be slow.

**Solution:** Many databases, such as Cassandra, HBase, and Redis, use Bloom Filters to avoid unnecessary disk lookups for non-existent keys. The Bloom Filter quickly checks if a key might be present. If the Bloom Filter indicates “not present,” it can skip the database lookup.

### Content Recommendation Systems

**Problem:** Recommendation systems, such as those used by streaming services, need to avoid recommending content that users have already consumed.

**Solution:** A Bloom Filter can track the content each user has previously watched or interacted with. When generating new recommendations, the Bloom Filter quickly checks if an item might already have been consumed.

### Social Network Friend Recommendations

**Problem:** Social networks like Facebook or LinkedIn recommend friends or connections to users, but they need to avoid recommending people who are already friends.

**Solution:** A Bloom Filter is used to store the list of each user’s existing connections. Before suggesting new friends, the Bloom Filter can be checked to ensure the user isn’t already connected with them.

## Limitations

### False positives

- Bloom Filters can produce false positives, meaning they may incorrectly indicate that an element is present in the set when it is not.
- Such false positives can lead to unnecessary processing or incorrect assumptions about data.
- For instance, in a database system, this might trigger unnecessary cache lookups or wasted attempts to fetch data that doesn’t actually exist.

### No Support for Deletions

- Standard Bloom Filters do not support element deletions. Once a bit is set to 1 by adding an element, it cannot be unset because other elements may also rely on that bit.
- This limitation makes Bloom Filters unsuitable for dynamic sets where elements are frequently added and removed.
- Variants like the Counting Bloom Filter can allow deletions by using counters instead of bits, but this requires more memory.

### Limited to Set Membership Queries

- Bloom Filters are specifically designed to answer set membership queries. They do not provide information about the actual elements in the set, nor do they support complex queries or operations beyond basic membership checks.
- If you need to know the details of an element (e.g., full information about a user ID), you would need another data structure in addition to the Bloom Filter.

### Vulnerable to Hash Collisions

- Hash collisions are more likely as the number of elements in the Bloom Filter grows. Multiple elements can end up setting or relying on the same bits, increasing false positives.
- As hash collisions accumulate, the filter’s effectiveness decreases. With a high load factor, the filter may perform poorly and become unreliable.

---

## How Bloom Filters Work (In-Depth)

A Bloom filter is a bit array of size `m` and uses `k` independent hash functions. When adding an item, each hash function maps the item to a position in the array and sets that bit to 1. To check membership, the item is hashed with all `k` functions; if all bits are 1, the item is possibly in the set (false positives possible), if any bit is 0, the item is definitely not in the set.

**Properties:**

- Space-efficient for large sets.
- Fast O(k) insert and query.
- No false negatives, but possible false positives.
- Standard Bloom filters do not support deletion.

---

## More Real-World Use Cases

- **Databases (Cassandra, HBase, Bigtable):** Avoid unnecessary disk reads by checking Bloom filters before accessing storage.
- **Google Chrome:** Checks URLs against a list of malicious sites using Bloom filters.
- **CDNs:** Quickly check if a resource is cached before fetching from origin.
- **Bitcoin:** Lightweight clients use Bloom filters to filter relevant transactions.
- **Email Spam Filtering:** Quickly check if an email address is blacklisted.

---

## System Design Applications

- **Cache Filtering:** Place a Bloom filter in front of a cache to avoid unnecessary lookups for non-existent keys.
- **Database Indexing:** Reduce disk I/O by ruling out non-existent rows or keys.
- **Distributed Systems:** Summarize sets and send compact representations to reduce network traffic.
- **Membership Testing:** Efficiently test membership for large sets (e.g., millions of URLs, user IDs).

**Design Tips:**

- Choose bit array size and number of hash functions based on expected elements and acceptable false positive rate.
- Use Counting Bloom Filters if you need to support deletions.
- Use alongside other data structures for exact membership or element details.

---

## Python Example: Simple Bloom Filter

```python
import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, n, p):
        self.size = self.get_size(n, p)
        self.hash_count = self.get_hash_count(self.size, n)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def check(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    @staticmethod
    def get_size(n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(m, n):
        k = (m / n) * math.log(2)
        return int(k)

# Usage
bf = BloomFilter(n=1000, p=0.01)
bf.add("example.com")
print(bf.check("example.com"))  # True
print(bf.check("not-in-set.com"))  # False or True (false positive)

```
*Requires `bitarray` and `mmh3` libraries:*
```bash
pip install bitarray mmh3
```

---

## Summary

Bloom filters are powerful tools for space-efficient membership testing, widely used in databases, distributed systems, and networking. They help optimize performance and resource usage in large-scale systems, but should be used with awareness of their probabilistic nature and limitations.

---

## How big tech uses bloom filters ?

### Netflix

#### Content discovery

- Instantly filters out irrelevant movies/shows before expensive database searches. Powers the "Continue Watching" and recommendation systems.

### Google

#### Web crawling

- Prevents crawlers from revisiting the same URLs. Bloom filters check if a URL has been crawled before hitting the massive URL database.

### Instagram

#### Username validation

- Quick check if username "might be taken" before querying user database. Prevents most database hits during username selection.

---

## Selecting right size

To select the right size for a bloom filter and minimize hash collisions (and false positives), we need to consider:

- Expected number of elements (n): How many items you plan to store.
- Desired false positive probability (p): Acceptable rate of false positives (e.g., 1%).

Formula for Bit Array Size (m)

```shell
m = -(n * ln(p)) / (ln(2)^2)
```

Formula for Number of Hash Functions (k)

```shell
k = (m / n) * ln(2)
```

### Practical tips

- Lower p (false positive rate) → larger m (more memory).
- More items (n) → larger m
