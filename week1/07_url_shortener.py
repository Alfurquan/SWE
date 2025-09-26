"""
Week 1 - Problem 7: URL Shortener (Basic Version)
Difficulty: Medium | Time Limit: 30 minutes | Google L5 System Design + Algorithms

PROBLEM STATEMENT:
Design a URL shortener service like bit.ly (single machine version)

OPERATIONS:
- shorten(long_url): Return shortened URL
- expand(short_url): Return original long URL
- getStats(short_url): Return click count and metadata

REQUIREMENTS:
- Generate unique short URLs (6-8 characters)
- Use base62 encoding (a-z, A-Z, 0-9)
- Handle collisions gracefully
- O(1) time complexity for operations
- Support custom aliases (optional)

ALGORITHM APPROACHES:
1. Counter-based + base62 encoding
2. Random generation + collision detection
3. Hash-based with collision handling

REAL-WORLD CONTEXT:
Actual URL shortener services, marketing campaign tracking, analytics

FOLLOW-UP QUESTIONS:
- How to scale to billions of URLs?
- Database design considerations?
- Caching strategy?
- Analytics and click tracking?
- Expiration and cleanup?

EXPECTED INTERFACE:
shortener = URLShortener()
short = shortener.shorten("https://www.google.com")  # "abc123"
original = shortener.expand(short)  # "https://www.google.com"
stats = shortener.getStats(short)   # {'clicks': 0, 'created': timestamp}
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
