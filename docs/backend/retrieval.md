# Retrieval

Search (`POST /api/v1/search`) embeds the query with `EmbeddingService`, fetches semantic tab results and PostgreSQL full-text results, then uses a rule-based `SearchIntentService` to select keyword, semantic, domain, or hybrid reciprocal-rank-fused output. The route validates only `tab_id`, `title`, `url`, and `score`; repositories return additional ad hoc fields.

Chat retrieval (`ContextSelectionService`) embeds the question, classifies fact/history/research/browsing/general intent, attempts graph expansion, retrieves chunks plus optional topic/session/cluster vector matches, deduplicates by tab, and builds a text prompt. It does not call the existing compression or ranking services.

Current limits and risks:

- Retrieval and search are not filtered by authenticated user.
- Semantic/full-text queries use runtime vector string formatting and full scans/index assumptions not verified in migrations.
- Scores use incompatible scales (0-100, rank scores multiplied by 1000, and raw full-text rank).
- No reranker, context token budget, citation verification, or retrieval telemetry exists.
- Graph expansion currently depends on a traversal query with obsolete columns.

GraphRAG v2 is a future phase. Its design must first restore user-scoped, tested base retrieval, then add entity/topic expansion and traversal behind measurable retrieval contracts.
