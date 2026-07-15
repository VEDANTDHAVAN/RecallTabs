# Testing

The API `pyproject.toml` points pytest at `services/api/tests`, but current files are ad hoc scripts that call local Ollama or print results. They have no pytest test functions, assertions, fixtures, fake providers, test database, extension tests, or web tests. Normal automated verification coverage is effectively absent.

Priority test baseline:

1. Unit test pure logic: chunking, intent classification, reciprocal-rank fusion, importance scoring, and URL filtering.
2. Add repository integration tests against ephemeral PostgreSQL+pgvector for vector/full-text SQL and model/query compatibility.
3. Add FastAPI tests for auth, ownership, error handling, capture idempotency, search, chat, and stream contracts.
4. Add provider contract tests using fake adapters, never real credentials or local model servers.
5. Add extension tests for queue persistence, deduplication, retry, API payloads, and popup state.
6. Add migration upgrade/downgrade tests before schema evolution.

Every defect discovered in this handbook should be converted into a focused regression test before or alongside its repair.
