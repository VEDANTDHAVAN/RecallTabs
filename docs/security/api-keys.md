# API Keys

No per-user provider credential storage exists. The backend reads process-level configuration from `services/api/.env`; the active embedding implementation uses a literal local `ollama` API key. The environment example contains `OPENAI_API_KEY`, but current `LLMService` and `EmbeddingService` are configured around local Ollama.

Do not add API keys to extension storage, source control, request payloads, logs, or global application configuration for user-specific providers. The future provider-settings phase requires encrypted-at-rest keys, key identifiers rather than returned secrets, connection testing, provider ownership checks, deletion/rotation, and redacted structured logging.
