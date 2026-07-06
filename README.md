# RecallTabs

RecallTabs is an AI-powered browser memory platform that turns saved tabs into a searchable, conversational knowledge base. The project already has a working foundation across the browser extension, backend API, and memory intelligence layers, and the next milestone is to turn that foundation into a more polished, reliable product experience.

## Current state

The core product loop is now functional:

- browser tabs can be captured and stored
- content can be indexed and searched semantically
- users can ask questions over saved context
- conversations and chat history are persisted
- memory structures such as topics, sessions, clusters, and timelines are available

This means the project is no longer just an early prototype; it is now a working MVP foundation ready for product hardening and user experience refinement.

## Recommended next development phase

### Phase 7: Product stabilization and end-to-end experience polish

This should be the next focus because the system is already technically capable, but it needs stronger consistency across the user experience.

Primary goals:

- make search and chat behavior more reliable and predictable
- tighten authentication and user-context handling across routes
- improve the extension UI so memory workflows feel cohesive
- add stronger testing around capture, search, chat, and session flows
- prepare the product for real-world usage with better observability and deployment readiness

Suggested sub-phases:

- Phase 7A: Search and chat contract stabilization
- Phase 7B: Extension memory UX and popup workflow polish
- Phase 7C: Automated tests and reliability hardening
- Phase 7D: Deployment, observability, and environment readiness

## Development roadmap

| Phase | Status | Focus |
| --- | --- | --- |
| Phase 1 | Completed | Backend foundation and API infrastructure |
| Phase 2 | Completed | Authentication and user model foundation |
| Phase 3 | Completed | Browser extension foundation and tab capture |
| Phase 4 | Completed | Semantic memory, embeddings, and retrieval |
| Phase 5 | Completed | Knowledge organization, topics, relationships, sessions, and clusters |
| Phase 6 | Completed | Conversation, chat, and saved-context interaction |
| Phase 7 | Upcoming | Product stabilization, UX polish, reliability, and tests |
| Phase 8 | Upcoming | Personalization, collections, reminders, and collaborative memory workflows |

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

The extension can capture page content and metadata and send it to the backend through the tab capture API. Stored data includes title, URL, summary, favicon, description, word count, and capture metadata.

### Semantic search

The backend exposes search endpoints that combine semantic and keyword-style retrieval over stored tab chunks and related memory structures.

### Ask and chat

Users can ask questions over saved tabs and receive answers grounded in retrieved context. The repository also includes conversation management and message persistence for multi-turn chat.

### Memory organization

The platform builds higher-level memory structures through topics, related-tab relationships, knowledge graphs, sessions, clusters, and timeline views.

## Local development

### Prerequisites

- Node.js 18+
- pnpm
- Python 3.11+
- PostgreSQL-compatible database with pgvector support
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

The API will be available at http://localhost:8000 and exposes a health endpoint at /health.

### 4. Run the web app

```bash
pnpm --filter web dev
```

### 5. Run the browser extension

```bash
pnpm --filter @recalltabs/extension dev
```

Then load the extension from the generated build output in your browser using the standard Chrome extension development flow.

## Development commands

```bash
pnpm install
pnpm dev
cd services/api
uvicorn app.main:app --reload
```

Build the extension:

```bash
pnpm --filter @recalltabs/extension build
```

## Verification notes

The current codebase has been exercised through the working backend and extension setup. The next phase should focus on:

- stronger API and service test coverage
- more stable chat/search integration
- better auth consistency and error handling
- a smoother extension user experience

