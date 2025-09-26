"""
Week 3 - Problem 2: Real-time Analytics Engine
Difficulty: Hard | Time Limit: 90 minutes | Google L5 Stream Processing

PROBLEM STATEMENT:
Build real-time analytics engine for processing event streams

OPERATIONS:
- registerMetric(name, aggregation_type): Define new metric
- processEvent(event): Process incoming event
- query(metric, start_time, end_time): Query aggregated data
- setWindow(metric, window_type, size): Configure time windows
- getTopK(metric, k): Get top K values

REQUIREMENTS:
- Support sliding and tumbling windows
- Handle late-arriving events
- Multiple aggregation types (sum, avg, count, percentiles)
- High throughput (millions of events/second)

ALGORITHM:
Stream processing, time window management, incremental aggregation

REAL-WORLD CONTEXT:
Apache Kafka Streams, Apache Flink, real-time dashboards

FOLLOW-UP QUESTIONS:
- How to handle extremely late events?
- Exactly-once processing guarantees?
- State management and recovery?
- Scaling across multiple machines?

EXPECTED INTERFACE:
engine = AnalyticsEngine()
engine.registerMetric("page_views", "count")
engine.setWindow("page_views", "sliding", size=300)  # 5 minutes
engine.processEvent({"metric": "page_views", "timestamp": 1000, "value": 1})
result = engine.query("page_views", start=900, end=1100)
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
