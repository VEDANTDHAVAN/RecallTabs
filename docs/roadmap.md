# Roadmap

This is a staged proposal derived from the current codebase, not a statement of implemented status.

| Phase | Objective | Gate |
| --- | --- | --- |
| 0 | Architecture baseline and handbook | Completed by this documentation change; no runtime refactor. |
| 0.1 | Stabilize current contracts | Fix constructor/schema/query drift, migration baseline, auth/user scoping, and test foundation. |
| 1 | Pipeline refactor | Extract tested capture steps while preserving capture API behavior. |
| 2 | Backend background queue | Durable jobs, retry, idempotency, and progress state. |
| 3 | Streaming progress | Structured capture/chat progress events after jobs exist. |
| 4 | Observability | Structured events, metrics, traces, dependency health, and dashboards. |
| 5 | Provider architecture | Typed provider registry/adapters and per-user provider resolution. |
| 6 | Frontend provider management | Authenticated web/extension settings and encrypted credential workflows. |
| 7 | Tool calling | Authorized tool registry, planner boundary, and execution tracing. |
| 8 | GraphRAG v2 | User-scoped entity/topic expansion, traversal, reranking, and evaluation. |
| 9 | Agent architecture | Explicit planner/executor with durable state and guardrails. |
| 10 | Production hardening | Security review, load tests, deployment automation, backup/recovery, and SLOs. |

The immediate next implementation phase should be Phase 0.1, not the pipeline rewrite. It has four small approval checkpoints: verify Alembic/database state; repair model/repository/constructor contract mismatches; enforce authenticated user scoping; and establish automated tests. No destructive migration or auth enforcement should be applied without explicit approval.
