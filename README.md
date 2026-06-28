# RecallTabs

AI-powered browser memory platform that turns saved browser tabs into a searchable, conversational knowledge base.

## Vision

People keep dozens of tabs open because closing them feels like losing context. RecallTabs captures useful pages automatically, stores their content and metadata, organizes them into memory structures, and lets users search or ask questions across their browsing history.

## Architecture

```text
Chrome Extension
    |
    v
FastAPI Backend
    |
    v
AI Pipeline
  - content extraction
  - text chunking
  - embeddings
  - semantic search
  - RAG/chat
    |
    v
PostgreSQL / Supabase / pgvector
    |
    v
Web Dashboard and Extension UI
```

## Tech Stack

- Monorepo: pnpm, Turborepo
- Backend: FastAPI, SQLAlchemy 2.0, Alembic
- Database: Supabase PostgreSQL, pgvector
- Extension: React, TypeScript, Manifest V3, CRXJS, Vite
- Web app: Next.js, TypeScript
- AI: OpenAI, FastEmbed, `BAAI/bge-small-en-v1.5`
- Auth: Clerk

## Project Structure

```text
RecallTabs/
  apps/
    extension/    Chrome extension
    web/          Next.js dashboard shell
  services/
    api/          FastAPI backend
  packages/
    ui/           Shared UI package
    eslint-config/
    typescript-config/
```

## Current Progress

### Phase 1 - Backend Foundation: Complete

Implemented:

- FastAPI application setup
- environment configuration
- structured logging
- SQLAlchemy database setup
- Alembic migrations
- Supabase/PostgreSQL connection
- `/health` endpoint

### Phase 2 - Authentication and Users: Complete, Needs Hardening

Implemented:

- users table
- user repository
- user provisioning service
- Clerk JWT verification layer
- current-user dependency

Known follow-up:

- several newer routes still use hardcoded development user IDs or do not consistently enforce auth.

### Phase 3A - Chrome Extension Foundation: Complete

Implemented:

- Manifest V3 extension
- CRXJS and Vite build setup
- React popup app
- background service worker
- content script
- tab update monitoring

### Phase 3B - Tab Capture Pipeline: Complete

Implemented:

- automatic page capture from the extension
- content extraction from page body text
- metadata extraction
- `POST /api/v1/tabs/capture`
- persistent tab storage
- favicon, description, word count, and capture metadata

### Phase 3C - Semantic Memory: Complete

Implemented:

- text chunking
- embedding generation
- pgvector-backed chunk storage
- semantic vector search
- `POST /api/v1/search`

Embedding model:

```text
BAAI/bge-small-en-v1.5
384 dimensions
```

### Phase 3D - RAG Question Answering: Complete

Implemented:

- query embeddings
- top-k chunk retrieval
- context assembly
- OpenAI-backed answer generation
- `POST /api/v1/ask`
- answer responses with sources

### Phase 4 - Knowledge Organization: Complete

Implemented:

- AI-generated tab summaries
- tab topics, categories, and keywords
- related-tab relationships
- topic endpoints
- knowledge graph endpoint

Key endpoints:

- `GET /api/v1/tabs/{tab_id}/related`
- `GET /api/v1/tabs/{tab_id}/graph`
- topic APIs under `services/api/app/api/v1/topics.py`

### Phase 5 - Sessions, Clusters, and Timeline: Complete

Implemented:

- browsing session detection
- session repository and API
- memory cluster model and service
- memory cluster query API
- timeline endpoint
- topic statistics endpoint

Key endpoints:

- `GET /sessions`
- `GET /clusters`
- `GET /timeline`
- `GET /timeline/topics`

### Phase 6A - Conversation Data Model: Complete

Implemented:

- conversation model
- message model
- repositories for conversations and messages
- migrations for conversation/message tables

### Phase 6B - Conversation Management API: Complete

Implemented:

- create conversation
- list conversations
- get conversation
- rename conversation
- delete conversation
- fetch conversation messages

Key endpoints:

- `POST /api/v1/conversations`
- `GET /api/v1/conversations`
- `GET /api/v1/conversations/{conversation_id}`
- `PATCH /api/v1/conversations/{conversation_id}`
- `DELETE /api/v1/conversations/{conversation_id}`
- `GET /api/v1/conversations/{conversation_id}/messages`

### Phase 6C - Chat Over Saved Tabs: Complete

Implemented:

- chat service
- message persistence for user and assistant turns
- retrieval over tab chunks
- answer generation with saved browsing context
- extension-side chat components

Key endpoint:

- `POST /api/v1/chat/{conversation_id}`

### Phase 6D - Search and Context Expansion: In Progress

Implemented or staged:

- hybrid search direction with semantic and keyword search repositories
- `is_searchable` filtering for ignored/internal pages
- extension search panel
- context selection across chunks, sessions, and memory clusters
- streaming chat endpoint scaffold

Known follow-ups before Phase 7 can be considered stable:

- align `/search` backend response with the extension `SearchPanel`
- repair streaming chat constructor and argument order
- consistently serialize pgvector query embeddings in session and cluster search
- restore or combine chat/search UI in the extension popup
- replace hardcoded user IDs with authenticated user context
- add focused API/service tests

## Current Status

```text
Phase 1   Complete  Backend foundation
Phase 2   Complete  Authentication and users, hardening needed
Phase 3A  Complete  Extension foundation
Phase 3B  Complete  Tab capture pipeline
Phase 3C  Complete  Semantic memory
Phase 3D  Complete  RAG question answering
Phase 4   Complete  Knowledge organization
Phase 5   Complete  Sessions, clusters, and timeline
Phase 6A  Complete  Conversation data model
Phase 6B  Complete  Conversation management
Phase 6C  Complete  Chat over saved tabs
Phase 6D  In progress  Search and context expansion
Phase 7   Next  Search/chat stabilization and extension memory UX
```

## Recommended Next Phase

Phase 7 should focus on stabilizing the product loop:

```text
capture tabs -> search saved memory -> ask/chat with sources -> revisit useful pages
```

Recommended split:

- Phase 7A: Search and chat contract stabilization
- Phase 7B: Extension memory UI
- Phase 7C: minimal tests for capture, search, and chat

## Development

Install dependencies:

```bash
pnpm install
```

Run all workspace development tasks:

```bash
pnpm dev
```

Run the API:

```bash
cd services/api
uvicorn app.main:app --reload
```

Run migrations:

```bash
cd services/api
alembic upgrade head
```

Build the extension:

```bash
pnpm --filter @recalltabs/extension build
```

Load the extension from:

```text
apps/extension/dist
```

## Verification

Recently verified:

- `python -m compileall app`
- `pnpm --filter @recalltabs/extension build`

The backend still needs integration tests with database, OpenAI, and authenticated route coverage.
