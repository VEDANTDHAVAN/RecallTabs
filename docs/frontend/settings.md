# Settings

There is no user settings implementation in the backend, extension, or web app. The only configuration is process-level environment configuration (`DATABASE_URL`, Clerk values, and local Ollama settings) plus a hard-coded extension development/production flag.

The requested future settings model must be per authenticated user and include provider connections, encrypted credentials, model choices, temperature, context length, embedding/reasoning/tool models, streaming, and a default provider. This is Phase 6 work and depends on Phase 5’s typed provider registry and a reviewed credential-encryption design.
