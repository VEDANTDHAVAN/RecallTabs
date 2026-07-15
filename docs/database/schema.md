# Database Schema

The intended database is PostgreSQL with pgvector. SQLAlchemy models define these current tables.

| Table | Key fields and relationships |
| --- | --- |
| `users` | UUID-like string id, unique Clerk id/email, conversations. |
| `tabs` | user, optional session/topic, content/metadata, searchable flag, importance/open/chat fields, entity links. |
| `tab_chunk` | tab id, chunk text, required 384-dimension embedding. |
| `topics` | unique title, optional 1536-dimension embedding, importance, tabs. |
| `entities` | unique name/type, optional 1536-dimension embedding, aliases and tab links. |
| `entity_aliases` | unique alias to entity. |
| `tab_entities` | tab/entity link, confidence, mention count. |
| `entity_relationships` | directed source/target entity, relationship type, confidence; unique tuple constraint. |
| `tab_relationships` | directed similar-tab pair and score. |
| `sessions` | title/topic/summary and optional cluster. |
| `memory_clusters` | title/summary and required 384-dimension embedding. |
| `conversations` | user and optional title. |
| `messages` | conversation, role, content, optional sources JSON and importance. |

The schema currently has global topics/entities/sessions/clusters rather than user ownership. That is incompatible with multi-user isolation and must be resolved incrementally with backfill/migrations, not a destructive rewrite.

Model/query drift exists: session vector search expects an unmodeled `sessions.embedding`; knowledge/traversal queries expect several obsolete names. Treat ORM models plus the verified migration head as the source to reconcile before new schema features.
