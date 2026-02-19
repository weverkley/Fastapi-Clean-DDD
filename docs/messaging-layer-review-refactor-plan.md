# Messaging Layer Review + Refactor Plan (Outbox + Idempotency)

## Summary

Current implementation is close to a standard outbox + at-least-once setup, but there are correctness bugs that break delivery guarantees and idempotency under concurrency.
Target contract: RabbitMQ-first, Pub/Sub as secondary adapter, isolated producer/consumer databases, at-least-once delivery with consumer-local idempotency.

## Review Findings (ordered by severity)

1. Critical: RabbitMQ ack/nack is not awaited
- `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py:42`
- `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py:43`
- `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py:48`
- `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py:52`
- `message.ack`/`message.nack` in `aio-pika` are async; current code calls them as sync functions. This can leave messages unacked and redelivered unexpectedly.

2. High: Consumer idempotency is race-prone (`exists` then `add`)
- `src/application/handlers/user_created_event_handler.py:14`
- `src/application/handlers/user_created_event_handler.py:20`
- `src/infrastructure/messaging/adapters/stores/processed_message_store_adapter.py:11`
- `src/infrastructure/messaging/adapters/stores/processed_message_store_adapter.py:17`
- Two concurrent deliveries can both pass `exists=false` and both run business logic before either writes dedupe record.

3. High: Message identity fallback can collapse distinct events
- `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py:35`
- If producer message_id is missing, hash(body) is used. Different business events with identical payload become the same idempotency key, causing false duplicates.

4. High: Outbox publish state has duplicate-delivery window
- `src/infrastructure/data/repository/outbox_repository.py:66`
- `src/application/handlers/publish_outbox_batch_handler.py:30`
- `src/infrastructure/data/repository/outbox_repository.py:82`
- Claim is committed before broker publish; if publish succeeds but DB update fails, row can be retried and republished later. This is acceptable only if consumers are strongly idempotent (currently not safe enough).

5. Medium: Failure path can run in broken DB transaction context
- `src/application/handlers/publish_outbox_batch_handler.py:31`
- `src/application/handlers/publish_outbox_batch_handler.py:33`
- If `mark_published` raises DB error, subsequent `mark_failed` may execute on an invalid transaction/session state.

6. Medium: Over-abstraction vs current need
- `src/application/interface/messaging/outgoing_event_publisher.py:5`
- `src/infrastructure/messaging/factories/outgoing_event_publisher_factory.py:5`
- Hexagonal boundaries are good, but current implementation has extra indirection without enforcing reliability invariants. Complexity is not paying off yet.

7. Medium: No verification suite for failure/retry/idempotency
- No tests found for duplicate deliveries, consumer concurrency, ack/nack behavior, or outbox retry transitions.

## Decision-Complete Implementation Plan

### 1) Reliability contract
- Keep at-least-once as explicit contract.
- Producer guarantees: transactional outbox write with business data.
- Consumer guarantees: local idempotent processing in consumer DB only.
- No consumer dependency on producer DB/outbox table.

### 2) Interface/type changes
- Update `IncomingEvent` ack/nack typing to support awaitable callbacks.
- Add explicit `idempotency_key` field to `IncomingEvent` (prefer broker `message_id`; fallback to `event_id` attribute/header; only then deterministic hash with event_type+payload).
- Replace `exists` + `add` store contract with atomic claim API:
  - `try_begin_processing(consumer_name, message_id) -> bool`
  - `mark_processed(consumer_name, message_id) -> None`
  - optional `mark_failed(...)` metadata for observability

### 3) Consumer flow (idempotency-first)
- On message receive:
  1. Derive stable message key.
  2. `try_begin_processing` using single SQL statement (`INSERT ... ON CONFLICT DO NOTHING`).
  3. If insert did nothing, ack and exit (duplicate).
  4. Execute business logic.
  5. Mark processed status and ack.
  6. On exception: nack/dead-letter according to policy.
- Do not use separate `exists` read.

### 4) Consumer DB schema (isolated)
- In consumer database, evolve `processed_messages` into an inbox ledger:
  - `consumer_name`, `message_id` unique key
  - `status` (`processing`, `processed`, `failed`)
  - `first_seen_at`, `processed_at`, `last_error`, `attempt_count`
- This keeps idempotency and replay metadata local to consumer.

### 5) Outbox worker hardening
- Keep current outbox table in producer DB.
- Keep claim/update approach but enforce safe session boundaries:
  - one transaction for claim
  - independent transaction per final state update (`published`/`failed`)
  - explicit rollback on DB exceptions before retry path
- Keep processing timeout reclaim behavior.
- Document expected duplicate window and dependency on consumer idempotency.

### 6) Simplification without breaking hexagonal design
- RabbitMQ remains primary concrete adapter.
- Pub/Sub stays as backup adapter behind same ports, but no Rabbit-specific assumptions in app layer.
- Remove only abstractions that are not carrying invariants (not the core ports).

### 7) Testing and acceptance criteria
- Unit: Rabbit adapter ack/nack awaited behavior.
- Unit: idempotency store `try_begin_processing` returns false on duplicate.
- Integration: same message delivered twice concurrently results in one business execution.
- Integration: publish succeeds + DB mark fails => eventual redelivery, consumer still processes once.
- Integration: message without broker message_id still gets stable dedupe key.
- Acceptance:
  - No duplicate business side effects under concurrent duplicate deliveries.
  - Consumer DB only for idempotency tracking.
  - Outbox retries continue functioning with dead-letter after max attempts.

## Assumptions and defaults

- Default chosen: at-least-once + idempotent consumer, not exactly-once.
- Producer and consumer use isolated databases.
- RabbitMQ is primary runtime; Pub/Sub remains adapter-compatible backup.
- Existing outbox table remains, with incremental hardening rather than full redesign.
