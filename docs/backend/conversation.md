# Conversation

Conversation CRUD is exposed at `/api/v1/conversations`; chat and streaming chat are exposed at `/api/v1/chat/{conversation_id}` and `/api/v1/chat-stream/{conversation_id}`. Messages store role, content, optional sources, and importance. Assistant importance is a simple heuristic based on question/answer length and number of sources; tab importance rises when a tab is cited.

The extension has chat components and API helpers, but the active popup renders only sync status and search. Chat helpers do not send auth headers.

Current operational defects:

- Conversation create/list use a hard-coded UUID; other CRUD endpoints do not verify conversation ownership.
- Chat routers construct `ConversationService` with five arguments, while the current service requires seven, including a topic repository and graph context service.
- Streaming uses plain `text/plain`; it does not emit structured source/progress/error events.
- History has no ordering/pagination contract and includes the newly saved user message before LLM generation.

The next conversation change should start with auth/ownership tests and a compatibility-safe service factory, not a broad chat rewrite.
