# Backend Services

The API services are synchronous Python classes instantiated directly by routers or by higher-level services.

| Area | Current services | Actual responsibility |
| --- | --- | --- |
| Capture | `TabCaptureService`, `TabEmbeddingService`, `TabAIService`, `TabSimilarityService`, `TextChunker` | Captures, enriches, chunks, embeds, classifies, and relates tabs. |
| Search/retrieval | `SearchService`, `SearchIntentService`, `RetrievalIntentService`, `AskService`, `ContextSelectionService` | Rule-based intent handling, vector/full-text search, prompt context assembly. |
| Conversation | `ConversationService`, `ConversationManagementService`, `MemoryImportanceService` | Conversation CRUD, chat/stream persistence, citation-driven importance updates. |
| Knowledge | `TopicGraphService`, `EntityGraphService`, `EntityExtractionService`, `TabEntityService`, `RelationshipExtractionService` | LLM extraction and storage of topic/entity knowledge. |
| Graph/memory | `GraphService`, `GraphAnalysisService`, `GraphContextService`, `GraphTraversalService`, `KnowledgeGraphService`, `RecommendationService`, `SessionDetectionService`, `MemoryClusterService` | Views, analysis, intended expansion, sessions, clusters, recommendations. |
| Support | `EmbeddingService`, `LLMService`, `UserProvisioningService`, `TimelineService` | External model calls, auth provisioning, timeline projection. |

`ContextCompressionService`, `ContextRankingService`, `EntityRelationshipService`, `MemoryConsolidationService`, and `MemorySummaryService` exist but are unused by the active routers/capture path. `MemoryConsolidationService` is an empty stub.

Service dependencies are mostly constructed internally. This is convenient for the prototype but makes retry policy, provider substitution, transaction scope, and isolated unit testing difficult. Future extraction should introduce constructor injection at boundaries while retaining the current public method contracts.
