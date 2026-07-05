# RecallTabs

RecallTabs is an AI-powered browser memory platform that turns saved tabs into a searchable, conversational knowledge base. It combines a Chrome extension, a FastAPI backend, and a lightweight web interface so users can capture browsing context, search it semantically, and ask questions over their saved tabs.

## What is implemented

The repository already contains the core product surface for a working recall experience:

- A Manifest V3 Chrome extension with a popup experience, background worker, and content-script entry points.
- Automatic tab capture and metadata extraction from browsing activity.
- A FastAPI backend with routers for tabs, search, ask, related tabs, topics, knowledge graphs, sessions, clusters, timeline, conversations, chat, and streaming chat.
- Semantic memory features built around chunking, embeddings, vector search, and OpenAI-backed answer generation.
- Conversation and message persistence so chat can continue across sessions.
- A web app shell for future dashboard-style experiences.

## Architecture

```text
Chrome Extension
  └─ captures tab metadata and submits it to the API

FastAPI Backend
  └─ stores tabs, chunks, sessions, clusters, conversations, and chat state

AI Pipeline
  ├─ content extraction
  ├─ chunking
  ├─ embeddings
  ├─ semantic search
  └─ RAG / chat responses

Data layer
  └─ PostgreSQL + pgvector via Supabase
```

## Tech stack

- Monorepo tooling: pnpm + Turborepo
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Database: PostgreSQL with pgvector
- Extension: React, TypeScript, Vite, CRXJS, Manifest V3
- Web app: Next.js + TypeScript
- AI: OpenAI + embedding-based retrieval
- Auth: Clerk-based JWT verification hooks

## Repository structure

```text
apps/
  extension/   Chrome extension app
  web/         Next.js web app shell
services/
  api/         FastAPI backend and API routes
packages/
  ui/          Shared UI package
```

## Core capabilities

### Tab capture and storage

The extension can capture page content and metadata, then send it to the backend through the tab capture API. Stored data includes title, URL, summary, favicon, description, word count, and capture metadata.

### Semantic search

The backend exposes search endpoints that combine semantic and keyword-style retrieval over stored tab chunks and related memory structures.

### Ask and chat

Users can ask questions over saved tabs and receive answers grounded in retrieved context. The repository also includes conversation management and message persistence for multi-turn chat.

### Memory organization

The platform builds higher-level memory structures through topics, related-tab relationships, knowledge graph data, sessions, clusters, and timeline views.

## Local development

### Prerequisites

- Node.js 18+
- pnpm
- Python 3.11+
- Access to a PostgreSQL-compatible database with pgvector support
- OpenAI API key
- Clerk environment values if auth is enabled

### 1. Install workspace dependencies

```bash
pnpm install
```

### 2. Set up the API environment

```bash
cd services/api
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local environment file at services/api/.env with values such as:

```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=your-openai-key
CLERK_JWKS_URL=...
CLERK_ISSUER=...
CLERK_AUDIENCE=...
```

### 3. Run the backend

```bash
cd services/api
uvicorn app.main:app --reload
```

The API should be available at http://localhost:8000 and exposes a health endpoint at /health.

### 4. Run the web app

```bash
pnpm --filter web dev
```

### 5. Run the browser extension

```bash
pnpm --filter @recalltabs/extension dev
```

Then load the extension from the generated build output in your browser using the standard Chrome extension development flow.

## Current status

Implemented and wired in the current codebase:

- Extension foundation and tab capture flow
- FastAPI backend and API routing
- Semantic search and RAG-style ask workflow
- Topic, cluster, session, timeline, conversation, and chat capabilities
- Initial web shell and extension UI integration

## Known follow-ups

The current codebase is functional, but a few areas are still worth hardening:

- tighten authentication consistency across routes
- align the search payloads between backend and extension UI
- stabilize streaming chat behavior and constructor wiring
- add broader automated tests around API and service layers
- polish the extension popup and dashboard experience

## Next step

The next iteration should focus on making the product feel more cohesive: better auth enforcement, more stable chat/search UX, and a more complete end-to-end extension experience.

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
