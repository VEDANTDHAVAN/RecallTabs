# Providers

Current provider implementation:

| Component | Current behavior |
| --- | --- |
| `BaseLLMProvider` | Abstract `chat`, `stream_chat`, and `completion` methods only. |
| `OllamaLocalProvider` | Uses the Ollama Python client and the configured host/model. `chat` asks Ollama for JSON format. |
| `LLMService` | Imports `OllamaLocalProvider` directly for answer, complete, chat, stream, and JSON-oriented calls. |
| `EmbeddingService` | Independently uses an OpenAI SDK pointed to `http://localhost:11434/v1`, hard-codes API key `ollama`, model `text-embedding-3-small`, and 384 dimensions. |

There is no provider registry, provider settings model, provider health endpoint, model enumeration, tool-call transport, cloud adapter, generic compatibility adapter, or per-user key selection. The README’s OpenAI wording does not match the active local implementation.

Provider work belongs in Phase 5 after the retrieval/auth baseline. Preserve `LLMService` behavior as a facade while adding a typed registry. The target interface is defined in [IMPLEMENTATION_PROMPT.md](../IMPLEMENTATION_PROMPT.md).
