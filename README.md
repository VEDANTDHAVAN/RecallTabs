# RecallTabs

AI-powered browser memory platform that transforms browser tabs into a searchable knowledge base.

## Vision

Most people keep dozens (or hundreds) of browser tabs open because they fear losing information.

RecallTabs solves this problem by automatically:

* Capturing browser tabs
* Storing tab metadata
* Organizing browsing history
* Extracting page content
* Generating AI summaries
* Creating embeddings
* Enabling semantic search
* Allowing users to close tabs without losing context

---

# Architecture

```text
┌─────────────────┐
│ Chrome Extension│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FastAPI Backend │
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│ AI Pipeline        │
│ Text Chunking      │
│ FastEmbed          │
│ Semantic Search    │
└────────┬───────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL      │
│ Supabase        │
│ pgvector        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Next.js App     │
└─────────────────┘
```

---

# Tech Stack

## Frontend

* Next.js 15
* TypeScript
* TailwindCSS
* shadcn/ui

## Chrome Extension

* React
* TypeScript
* Manifest V3
* CRXJS
* Vite

## Backend

* FastAPI
* SQLAlchemy 2.0
* Alembic

## Database

* Supabase PostgreSQL
* pgvector

## AI

* FastEmbed
* BAAI/bge-small-en-v1.5
* Semantic Vector Search
* Text Chunking

## Authentication

* Clerk

## Deployment

* Vercel
* Railway

---

# Monorepo Structure

```text
RecallTabs/
│
├── apps/
│   │
│   ├── web/
│   │
│   └── extension/
│
├── services/
│   │
│   └── api/
│
├── packages/
│
├── turbo.json
│
└── pnpm-workspace.yaml
```

---

# Current Progress

## Phase 1 — Backend Foundation ✅

### Implemented

* FastAPI Application
* Configuration Management
* Environment Variables
* Structured Logging
* SQLAlchemy Setup
* Alembic Setup
* Supabase Connection
* Health Check Endpoint

### Health Endpoint

```http
GET /health
```

Response:

```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

## Phase 2 — Authentication & Users ✅

### Implemented

#### User Management

* Users Table
* User Repository
* User Provisioning Service

#### Authentication Infrastructure

* Clerk Configuration
* JWT Verification Layer
* Protected Routes
* Current User Dependency

#### Database Relationships

```text
Users
  └── Tabs
```

### Verified

* User Creation
* User Retrieval
* Database Persistence

Example Response:

```json
{
  "id": "125657ed-f496-4735-8391-696b96be49c8",
  "email": "test@example.com"
}
```

---

## Phase 3A — Chrome Extension Foundation ✅

### Implemented

#### Extension Infrastructure

* Manifest V3
* CRXJS Setup
* Vite Build System
* React Popup
* Background Service Worker

#### Tab Monitoring

* Tab Update Detection
* Tab Metadata Capture
* Service Worker Logging

### Verified

Extension successfully captures:

```json
{
  "id": 1003198318,
  "title": "Home - Chess.com",
  "url": "https://www.chess.com/home"
}
```

### Example Console Output

```text
RecallTabs Background Started

Tab Updated {
  id: 1003198318,
  title: "Home - Chess.com",
  url: "https://www.chess.com/home"
}
```

---
## Phase 3B — Tab Capture Pipeline ✅

### Implemented

* Automatic page capture
* Content extraction
* Metadata extraction
* FastAPI capture endpoint
* Persistent PostgreSQL storage

Captured fields:

- URL
- Title
- Content
- Description
- Favicon
- Word Count
- Captured At

### Endpoint

POST /api/v1/tabs/capture

---

## Phase 3C — Semantic Memory ✅

### Implemented

* Text Chunking
* Embedding Generation
* pgvector Integration
* Vector Similarity Search
* Search API

Embedding Model

BAAI/bge-small-en-v1.5

Embedding Dimensions

384

### Endpoint

POST /api/v1/search

# Example:

[
  {
    "tab_id": "...",
    "title": "ChatGPT",
    "url": "...",
    "score": 0.72
  }
]

---

# Backend Structure

```text
services/api/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── features/
│   │   │
│   │   ├── users/
│   │   │
│   │   └── tabs/
│   │
│   ├── infrastructure/
│   │   └── database/
│   │
│   └── main.py
│
├── migrations/
│
└── requirements.txt
```

---

# Extension Structure

```text
apps/extension/
│
├── src/
│   │
│   ├── background/
│   │   └── index.ts
│   │
│   ├── popup/
│   │   └── App.tsx
│   │
│   ├── content/
│   │
│   ├── options/
│   │
│   └── shared/
│
├── manifest.config.ts
├── vite.config.ts
├── tsconfig.json
│
└── package.json
```

---

# Setup

## Clone Repository

```bash
git clone <repository-url>

cd RecallTabs
```

---

## Install Dependencies

```bash
pnpm install
```

---

## Backend

```bash
cd services/api

python -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
services/api/.env
```

```env
APP_NAME=RecallTabs

ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://...

OPENAI_API_KEY=...

CLERK_JWKS_URL=...

CLERK_ISSUER=...

CLERK_AUDIENCE=...
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

---

## Run Migrations

```bash
alembic upgrade head
```

---

## Extension

```bash
cd apps/extension

pnpm install
```

Development:

```bash
pnpm dev
```

Production Build:

```bash
pnpm build
```

---

## Load Extension

Open:

```text
chrome://extensions
```

Enable:

```text
Developer Mode
```

Click:

```text
Load unpacked
```

Select:

```text
apps/extension/dist
```

---

# Testing

## Backend

Health Check:

```bash
curl http://localhost:8000/health
```

Expected:

```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

## Database

Verify Users:

```sql
SELECT * FROM users;
```

Verify Tabs:

```sql
SELECT * FROM tabs;
```

---

## Extension

Open several websites:

```text
https://github.com
https://openai.com
https://chess.com
```

Open Service Worker console.

Expected:

```text
RecallTabs Background Started

Tab Updated
```

events should appear.

---

# Roadmap

## Phase 3B ✅ Tab Capture Pipeline
## Phase 3C ✅ Semantic Memory
---

## Phase 3D 🚧 AI Question
Answering

AI Processing Pipeline

* GPT Summaries
* Embeddings
* Vector Storage

---

## Phase 4 🚧 Knowledge Organization

* Tab Clustering
* Topic Detection
* Session Detection

---

## Phase 6

Search & Retrieval

* Semantic Search
* RAG
* Context Retrieval

---

## Phase 7

Dashboard

* Search UI
* Knowledge Browser
* AI Chat over Tabs

---

# Current Status

```text
Phase 1   ✅ Complete
Phase 2   ✅ Complete
Phase 3A  ✅ Chrome Extension Foundation
Phase 3B  ✅ Tab Capture Pipeline
Phase 3C  ✅ Semantic Memory with pgvector
Phase 3D  🚧 AI Question Answering
```

**Current milestone:**
RecallTabs can automatically capture webpages, extract content,
generate embeddings, store vectors in pgvector, and perform
semantic search over browsing history.
