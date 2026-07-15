# RecallTabs Implementation Contract

You are modifying RecallTabs, an AI browser-memory monorepo. Read [architecture.md](architecture.md) and the relevant handbook pages before proposing or writing code.

## Non-Negotiable Rules

1. Analyze existing code first. Inspect the router, service, repository, model, schema, migration, extension client, and existing tests that participate in the requested behavior.
2. Reuse existing services and repositories when their responsibilities already match. Do not create parallel capture, search, conversation, embedding, or persistence paths.
3. Never rewrite working code merely to impose a new style. Make incremental, reviewable changes.
4. Preserve public APIs and database schema by default. Add compatibility layers or additive migrations when a change is unavoidable.
5. Keep routers thin and repositories free of application policy. Business decisions belong in services or explicit pipeline steps.
6. Use SQLAlchemy 2 typing, dependency injection, explicit types, and asynchronous boundaries only when the surrounding contract has been migrated safely.
7. Every feature requires focused tests and documentation. Update the affected handbook page in the same change.
8. Treat existing users’ data, capture queues, stored tabs, conversations, and provider credentials as production data.
9. Do not implement planned architecture as if it already exists. Current state is documented in [architecture.md](architecture.md).
10. Before critical changes such as migration application, schema removal, credential changes, authentication enforcement, provider/key storage, background job infrastructure, or deployment changes, request explicit approval.

## Required Phase Format

Every implementation phase document or pull request must contain these sections:

### Objective

State the narrow product and technical outcome. Name compatibility constraints.

### Files To Inspect

List all current router, schema, model, migration, service, repository, extension/web client, configuration, and test files that establish the behavior.

### Files To Modify

List only files whose existing responsibility genuinely needs to change.

### Files To Create

List additive files and justify why an existing module cannot own the behavior.

### Implementation Steps

Describe the smallest ordered changes. Preserve request/response contracts unless a compatibility plan is documented.

### Acceptance Criteria

State observable behavior, error handling, authorization, and backward-compatibility conditions.

### Tests

Add unit tests for deterministic logic, repository integration tests for SQL behavior, API tests for route/auth contracts, and extension tests where UI/client behavior changes. Avoid real network/LLM calls in normal test suites.

### Migration Notes

For database changes, describe forward migration, rollback, data backfill, index impact, lock risk, and model/repository alignment. Never edit an applied migration; create a new migration.

### Review Checklist

Confirm dependency direction, authorization and user scoping, transaction boundaries, error handling, logging, observability, performance, API compatibility, docs, and tests.

## Current Architecture Guardrails

- `TabCaptureService` currently owns an overly broad synchronous pipeline. Refactor it by extracting one existing behavior at a time into explicit steps; keep the existing capture endpoint compatible throughout.
- The only live LLM provider is local Ollama. Introduce a provider registry behind the existing `LLMService` compatibility surface before adding cloud providers.
- Provider API keys must become encrypted, per-user records. Do not add global cloud credentials as a substitute.
- Retrieval must be user scoped before it is made more capable. Do not add GraphRAG traversal that can cross user data.
- The extension has multiple API clients and request types. Consolidate only after tracing every caller and retaining the existing upload queue behavior.
- Current migrations and models have mismatches. Establish a verified migration baseline before schema evolution.

## Target Provider Interface

When Phase 5 begins, every provider adapter must implement an identical, typed interface with:

`chat()`, `stream_chat()`, `complete()`, `json_chat()`, `tool_call()`, `models()`, `health()`, and optional `embeddings()`.

Adapters may translate provider-specific HTTP payloads, but must not contain application tools, retrieval policy, or user-setting lookup. Support local Ollama, LM Studio, vLLM; cloud OpenAI, Gemini, Anthropic, Groq, Together AI, Fireworks AI, Cerebras, Azure OpenAI; OpenRouter; and generic OpenAI-compatible endpoints only after the registry and settings model are tested.

## Target Tool Boundary

Tool selection belongs outside providers:

```text
Planner -> Tool Registry -> Tool Execution -> Memory Retrieval -> Knowledge Graph -> Browser Boundary -> Answer
```

Tools must be registered, authorized, typed, observable, and independently testable. Providers only transport tool-call requests/results.

## Target Capture Pipeline

The eventual pipeline is validation, chunking, embedding, similarity, summary, topics, entities, relationships, sessions, clusters, importance, persistence, and completion. Extract it incrementally from `TabCaptureService`; each step must be independent, retryable, observable, and unit tested before backend queuing moves it out of the request path.

## Implementation Order

Follow [roadmap.md](roadmap.md). Do not skip stabilization and security to build future-facing features. Resolve current constructor, schema/query, migration, authorization, and test-baseline defects before broad architectural additions.
