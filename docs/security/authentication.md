# Authentication

The API has Clerk JWT verification through `get_current_user`. It reads a bearer token, validates it using Clerk JWKS and issuer, requires an email claim, then provisions or returns a local `users` record.

Implemented authenticated routes are `/api/v1/tabs/me`, `POST /api/v1/tabs`, and `GET /api/v1/tabs`. The capture endpoint has its auth dependency commented out and uses a hard-coded user UUID. Conversation create/list use a hard-coded dependency, while read/update/delete and chat routes lack ownership checks. Search, ask, graph, sessions, clusters, timeline, topics, knowledge graph, and recommendations are also unauthenticated and use global data.

This is a critical production boundary. Phase 0 documentation does not alter it. The next authorization phase must establish a single current-user dependency, propagate `user_id` into every data query, enforce resource ownership, remove debug/hard-coded routes, and add cross-user isolation API tests before enabling multi-user provider settings.
