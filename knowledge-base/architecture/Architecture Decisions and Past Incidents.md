# Architecture Decisions and Past Incidents

## ADR-001: Use asynchronous order-status processing

### Decision

Process eligible orders in a controlled periodic status flow and use Azure Service Bus for asynchronous communication between services.

### Reason

The order delivery lifecycle includes work that should not depend on one synchronous request completing. Controlled processing helps recover orders in a limbo state and makes work visible through queue and service metrics.

### Operational consequence

The status processor must be idempotent. It must record correlation IDs, avoid duplicate transitions, and expose processing failures for investigation.

## ADR-002: Retry only transient failures

### Decision

Use bounded retries with exponential backoff and jitter for selected transient failures. Do not retry permanent 400 client errors by default.

### Reason

A production incident demonstrated that retrying 400 errors can create a 100x traffic amplification loop. The retries increased load while the original request could never succeed without a correction.

### Code review questions

- Is the retryable status-code list explicit?
- Is the maximum attempt count bounded?
- Is the operation idempotent?
- Are retry reason and attempt count logged?
- Are 400 and other permanent errors covered by tests?

## Incident-001: 100x traffic amplification loop

### Impact

During an API failure, the system generated excessive repeat traffic and made recovery harder.

### Cause

A retry policy treated 400 client errors as retryable. Multiple request layers amplified the behavior.

### Resolution

The retry policy was optimized to bypass 400 client errors. Follow-up work should add retry metrics, status-code tests, and alerts on abnormal retry ratios.

## Incident-002: Orders stuck in limbo

### Impact

Some orders needed manual intervention because periodic status processing did not complete the expected transition.

### Investigation path

Search logs and traces by order ID and correlation ID. Inspect queue delivery count and dead-letter information. Compare the downstream API response with the retry policy. Then consult the order delivery troubleshooting runbook.

### Resolution pattern

Automate periodic processing for eligible limbo orders, make the consumer idempotent, prevent retries for permanent errors, and verify that the order reaches its expected terminal state.

## Decision search examples

Useful questions for the knowledge base include:

- Why should a 400 response not be retried?
- Which architecture decision addresses orders stuck in limbo?
- What evidence links the 100x traffic incident to retry policy behavior?
- Which documents should an engineer read before changing the order-status processor?
