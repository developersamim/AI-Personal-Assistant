# Incident Response Runbook

## Scope

This runbook supports production incidents in the order delivery platform. It covers orders stuck in a limbo state, failed API calls, excessive retries, and delayed status processing.

## Incident: Orders Stuck in Limbo

### Symptoms

- Orders remain in an intermediate status and do not progress.
- The delivery team reports that manual intervention is required.
- The order-status processor may repeatedly pick up the same order.
- Downstream services may show incomplete or delayed updates.

### First checks

1. Identify the order ID, current status, and last status transition time.
2. Check application logs for the order-status processor and the downstream API.
3. Check Azure Service Bus messages, delivery count, lock loss, and dead-letter activity.
4. Check whether the latest API response is a permanent 400 client error or a transient 5xx failure.
5. Compare retry volume with normal traffic and check for duplicate processing.

### Immediate actions

- Do not retry a permanent 400 client error. Mark it for investigation or manual handling according to the business rule.
- Allow retries for transient 5xx failures only when the retry policy has a bounded attempt count and backoff.
- Pause or isolate the failing consumer if it is amplifying traffic.
- Use the order-status automation to process eligible limbo orders periodically instead of relying on uncontrolled repeated retries.
- Record the order ID, correlation ID, error code, retry count, and mitigation in the incident timeline.

### Validation

Confirm that the order leaves the limbo state, message delivery counts return to normal, downstream calls stop repeating, and no new duplicate orders or status transitions are created.

## Incident: Traffic Amplification During API Failure

A previous production incident caused a 100x traffic amplification loop. The retry policy treated 400 client errors as retryable, so every failed request produced more requests without a realistic chance of success.

### Root cause

The client retried a permanent validation or client error instead of stopping. Multiple layers of the system compounded the retry behavior.

### Fix

Bypass 400 client errors in retry policies. Keep retries for transient failures such as selected 5xx responses and transport failures, with exponential backoff, jitter, and a maximum attempt count.

### Prevention

- Maintain an explicit retryable-status allowlist.
- Add tests for 400, 404, 409, 429, and 5xx responses.
- Emit retry count and retry reason in structured logs.
- Alert on unusual retry-to-request ratios.
- Review retry behavior during incident retrospectives.

## Escalation checklist

Escalate to the service owner when data integrity is at risk, the queue continues to grow after mitigation, the same order is processed repeatedly, or the downstream dependency remains unavailable. Include logs, traces, message identifiers, retry policy, and the exact change made.
