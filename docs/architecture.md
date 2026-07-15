## RecallTabs Architecture

### Project Vision

RecallTabs turns captured browser pages into a searchable personal memory. The implementation stores tab content, derived metadata, vector chunks, topics, entities, relationships, sessions, clusters, and conversation messages in PostgreSQL with pgvector.

This document describes the repository as it exists on 2026-07-15. Planned provider management, tool calling, background workers, GraphRAG v2, and a product dashboard are not represented as implemented architecture.

### Current Architecture

```text
Chrome extension (React + Manifest V3)
  -> FastAPI HTTP API
     -> synchronous service layer
        -> SQLAlchemy repositories -> PostgreSQL + pgvector
        -> Ollama Local Provider -> local Ollama server

Next.js web app: starter template only; not connected to the API.
```

The browser extension captures page text in a content script. Its background service worker queues capture jobs in `chrome.storage.local`, retries upload, and sends `POST /api/v1/tabs/capture`. The API processes a capture synchronously: persist tab, chunk and embed content, find similar tabs, request LLM metadata, assign a topic, extract entities and relationships, then attempt session and cluster assignment.

### Folder Structure

| Location | Responsibility |
| --- | --- |
| `apps/extension` | Manifest V3 browser extension: content extraction, durable local queue, API calls, popup search/status UI. |
| `apps/web` | Next.js starter application. No RecallTabs screens or API client yet. |
| `packages/ui` | Small shared React component package retained from the Turborepo starter. |
| `packages/eslint-config`, `packages/typescript-config` | Shared workspace configuration. |
| `services/api/app/api/v1` | FastAPI routers. |
| `services/api/app/services` | Application logic and orchestration. |
| `services/api/app/repositories` | SQLAlchemy persistence and raw PostgreSQL/pgvector queries. |
| `services/api/app/infrastructure/database/models` | SQLAlchemy 2 ORM models. |
| `services/api/app/providers` | LLM provider abstraction and the Ollama implementation. |
| `services/api/migrations` | Alembic configuration and migration history. |

### Dependency Rules Observed

Routers instantiate repositories and services directly from a synchronous SQLAlchemy session. Services call repositories and other services. Repositories import database models and own SQL, including raw pgvector SQL. Models import only the declarative base. This is the intended layering, although several services construct their own dependencies rather than receiving all dependencies through injection.

There is no package-level dependency enforcement, no container, and no asynchronous database layer. `TabCaptureService` is the main exception to narrow service responsibility: it creates many repositories and invokes most of the enrichment pipeline itself.

### Repository Pattern

Repositories are per aggregate/table and generally expose CRUD plus query helpers. `TabChunkRepository`, `TabRepository`, `TopicRepository`, `SessionRepository`, and `MemoryClusterRepository` contain database-specific vector and full-text queries. Each write operation commits independently, so a capture spans many transactions rather than one unit of work.

`MemoryImportanceRepository` duplicates simple tab lookup/save/list behavior already supplied by `TabRepository`; it is currently not used by the application path.

### Service Layer

Implemented services cover capture, embeddings, metadata analysis, semantic search, topics, entities, tab relationships, conversations, clusters, graph views, and recommendations. The service layer is synchronous and invokes local LLM/embedding calls inline. Some services are presently unreferenced (`ContextCompressionService`, `ContextRankingService`, `EntityRelationshipService`, `MemoryConsolidationService`, and `MemorySummaryService`) or incomplete.

### Database

The target database is PostgreSQL with pgvector. `tab_chunk.embedding` and `memory_clusters.embedding` use 384 dimensions; `topics.embedding` and `entities.embedding` use 1536 dimensions. The configured embedding service asks the local OpenAI-compatible Ollama endpoint for `text-embedding-3-small` with `dimensions=384`; this makes topic/entity embedding compatibility provider-dependent and must be reconciled before relying on all vector queries.

See [schema.md](database/schema.md) and [migrations.md](database/migrations.md).

### Pipeline

Current capture order is: validate/ignore URL, persist tab, skip non-searchable or empty content, chunk and embed, create similar-tab relationships, summarize/classify with the LLM, create/select topic, calculate tab importance, extract and connect entities, extract entity relationships, assign session, assign cluster.

The steps are not independently retryable, observable, or transactionally coordinated. The extension has a client-side upload queue, but the API has no background queue or job model.

### Retrieval

Search embeds the query, gets semantic tab results and PostgreSQL full-text results, detects a rule-based search intent, and fuses hybrid results with reciprocal rank fusion. Conversational retrieval embeds the question, classifies a rule-based retrieval intent, attempts graph entity expansion, and retrieves varying combinations of chunks, topics, sessions, and clusters.

There is no reranker, user scoping in these retrieval queries, prompt budget enforcement, or persisted retrieval trace. See [retrieval.md](backend/retrieval.md).

### GraphRAG, Knowledge, and Entity Graphs

The repository stores entity-to-tab links, entity aliases, typed entity relationships, tab-to-tab similarity, topic membership, sessions, and clusters. It also exposes graph-shaped topic/entity views and NetworkX analysis. Entity extraction and relationship extraction are LLM driven.

Graph traversal and the legacy entity relationship service currently refer to columns that the current `EntityRelationship` model does not define. Graph expansion is therefore architectural intent with a broken persistence query, not an operational GraphRAG implementation.

### Conversation Memory

Conversations belong to users and messages belong to conversations. Chat persists the user message, builds context, calls the LLM, persists sources and an importance score, and increments importance for cited tabs. Streaming emits plain text tokens and persists the final assistant message only after the stream ends.

At the router boundary, the current `ConversationService` constructor requires topic and graph-context dependencies that its chat routers do not pass. This is a runtime integration defect recorded for remediation, not a documented feature guarantee.

### Browser Extension

The extension has a content script that extracts `document.body.innerText`, metadata, and favicon. A background worker captures on load, tab activation, and focused-window changes; deduplicates queued content by URL/hash; stores queue state locally; and retries failed API uploads. The popup displays queue state and search results. A separate sidebar shell exists but is commented out from the content script and only renders static text.

There are duplicate API clients and capture request types, no extension authentication token flow, and no settings/provider-management UI. See [extension.md](frontend/extension.md).

### Frontend

The extension is the only product-facing UI. `apps/web` is an unchanged Next.js/Turborepo starter page. Shared `@repo/ui` components are starter artifacts and are not a RecallTabs design system.

### Authentication and User Settings

Clerk JWT verification and just-in-time user provisioning exist. Only `/api/v1/tabs/me`, create tab, and list tabs consistently use it. Capture, search, graph, memory, ask, chat, and most conversation endpoints are unauthenticated or use a hard-coded development user. No user settings or encrypted per-user provider keys exist.

### LLM Providers

`BaseLLMProvider` defines `chat`, `stream_chat`, and `completion`. `OllamaLocalProvider` is the sole implementation. `LLMService` imports it directly, and `EmbeddingService` separately hard-codes an Ollama OpenAI-compatible endpoint. Cloud providers, provider selection, health checks, model enumeration, JSON/tool call contracts, and user-specific configuration are not implemented.

### Tool Calling and Agent Layer

No tool registry, planner, provider tool-call method, browser tool boundary, or agent loop exists. The LLM is used only for generation and JSON-oriented extraction prompts.

### Queue System

The extension’s `CaptureQueue` and `SyncManager` provide a local browser upload queue with retry. The backend runs enrichment synchronously inside the capture request; it has no durable queue, worker, retry policy, job status API, or progress stream.

### Logging, Metrics, and Testing

The API configures JSON logging but several services still use `print`. There are no structured request IDs, capture/job correlation IDs, metrics, tracing, health checks for dependencies, or alerting. Files under `services/api/tests` are executable local LLM smoke scripts, not pytest test cases with assertions or fixtures. The extension and web app have no tests.

### Deployment

No Dockerfile, compose file, CI workflow, or deployment manifests are present. The existing configuration assumes a local API, PostgreSQL-compatible database, pgvector, and local Ollama. See [docker.md](deployment/docker.md).

### Future Roadmap

The repository should evolve incrementally through the documented phases in [roadmap.md](roadmap.md): first stabilize contracts and security, then extract capture steps, add backend jobs/observability, introduce the provider architecture and settings, then tool calling, GraphRAG v2, agents, and production hardening.
