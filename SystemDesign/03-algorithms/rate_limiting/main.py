from rate_limiting.token_bucket import TokenBucket
import time

def main():
    limiter = TokenBucket(capacity=5, refill_rate=2)
    key = "user-123"

    for _ in range(8):
        print(limiter.allow_request(key))
        time.sleep(0.1)

    time.sleep(2)
    print(limiter.allow_request(key))

if __name__ == '__main__':
    main()