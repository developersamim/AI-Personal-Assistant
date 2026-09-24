# Runbooks and Technical Documentation

## Order delivery troubleshooting guide

The order delivery lifecycle uses services, asynchronous messaging, and periodic status processing. When an order is stuck, search by order ID and correlation ID across the order service, status processor, Azure Service Bus, and downstream API logs.

Use this sequence:

1. Confirm the current order state and the last successful transition.
2. Find the correlation ID and follow it across service logs and message properties.
3. Identify whether the failure is a client error, a transient server error, a timeout, or a message-processing problem.
4. Check retry count, backoff, queue delivery count, and dead-letter status.
5. Apply the relevant runbook and verify the state transition after the change.

## Retry policy reference

Retry only failures that may succeed when attempted again. A bounded retry policy should use exponential backoff and jitter, record the reason for every retry, and stop after a maximum attempt count.

Do not retry permanent 400 client errors by default. Retrying them can create a traffic amplification loop and hide the original validation problem. Treat 429 responses according to the dependency contract and use a server-provided delay when available. Review 409 responses based on whether the operation is idempotent. Retry selected 5xx responses and transport failures when the operation is safe to repeat.

## Message processing reference

For Azure Service Bus failures, inspect delivery count, lock duration, settlement state, dead-letter reason, and correlation properties. A growing delivery count may indicate a poison message or a consumer that cannot complete processing. Preserve the message identifier when escalating.

## Incident response and RAG search

The internal RAG assistant indexes runbooks, retry policies, service documentation, architecture decisions, and past incident reports. A question such as "Why are orders stuck in limbo?" should retrieve the order troubleshooting guide and the relevant incident record before generating an answer.

The assistant should provide:

- likely cause and supporting evidence
- immediate mitigation
- commands or checks to perform
- validation steps
- source document names
- uncertainty when the documents do not contain enough evidence

RAG provides operational context. Logs, traces, metrics, and source code remain the authority for the current live state.
