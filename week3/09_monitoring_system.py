"""
Week 3 - Problem 9: Monitoring & Alerting System
Difficulty: Hard | Time Limit: 85 minutes | Google L5 Observability

PROBLEM STATEMENT:
Build comprehensive monitoring and alerting system

OPERATIONS:
- collectMetric(name, value, tags, timestamp): Ingest metrics
- createAlert(name, condition, severity): Define alert rules
- checkAlerts(): Evaluate all alert conditions
- sendNotification(alert, channels): Send alert notifications
- getMetrics(query, start_time, end_time): Query metrics

REQUIREMENTS:
- Time-series metric storage and querying
- Flexible alert condition evaluation
- Multiple notification channels (email, Slack, PagerDuty)
- Alert fatigue prevention (grouping, suppression)

ALGORITHM:
Time-series database, rule engine, notification routing

REAL-WORLD CONTEXT:
Prometheus + Alertmanager, DataDog, New Relic, Grafana

FOLLOW-UP QUESTIONS:
- How to handle metric explosion?
- Distributed tracing integration?
- Anomaly detection with ML?
- Cost optimization for metrics storage?

EXPECTED INTERFACE:
monitor = MonitoringSystem()
monitor.collectMetric("cpu_usage", 85.5, {"host": "web1"}, 1640995200)
monitor.createAlert("high_cpu", "cpu_usage > 90", "critical")
alerts = monitor.checkAlerts()
monitor.sendNotification(alerts[0], ["email", "slack"])
"""

# Your implementation here
if __name__ == "__main__":
    # Add your test cases here
    pass
