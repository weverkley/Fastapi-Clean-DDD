# Integration Tests

These tests validate end-to-end behavior against a running stack (API + workers + RabbitMQ + Postgres).

## Run

```bash
python3 -m unittest discover -s tests/integration -p "test_*.py" -v
```

## Environment Variables

- `INTEGRATION_BASE_URL` (default: `http://localhost:8000`)
- `INTEGRATION_REQUEST_TIMEOUT_SECONDS` (default: `10`)
- `INTEGRATION_EVENTUAL_TIMEOUT_SECONDS` (default: `45`)
- `INTEGRATION_POLL_INTERVAL_SECONDS` (default: `1`)
