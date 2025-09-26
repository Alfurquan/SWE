# Circuit Breaker Pattern

The Circuit Breaker Pattern is a design strategy used in distributed systems to detect failures and encapsulate the logic of preventing a failure from constantly recurring.

## How the Circuit Breaker Pattern Works?

The circuit breaker sits between a client and a service. It monitors the service’s behavior, and if failures reach a certain threshold, it trips—stopping further requests until the service recovers.

There are three main states:

1. Closed State
Normal Operation: The circuit breaker allows requests to pass through to the service.
Monitoring: It monitors the success and failure rates of the requests.
2. Open State
Failure Threshold Exceeded: When failures surpass a pre-defined threshold, the circuit breaker "trips" and moves to the open state.
Short-Circuiting Requests: In this state, further requests are not sent to the failing service. Instead, the client immediately receives an error or fallback response.
Cooling-Off Period: The circuit remains open for a specified time, allowing the system to recover.
3. Half-Open State
Testing for Recovery: After the cooling-off period, the circuit breaker allows a limited number of test requests to pass through.
If the test requests succeed, the circuit resets to the closed state.
If they fail, the circuit reopens, and the cooling-off period restarts.
