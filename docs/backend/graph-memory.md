# Graph and Memory

Implemented persistence structures are:

- Topic: a globally unique title with summary, vector, and importance.
- Entity: a globally unique name/type with aliases, vector, importance, and tab links.
- TabEntity: a tab-to-entity mention link with confidence and mention count.
- EntityRelationship: directed source/target/type/confidence relationship.
- TabRelationship: directed similar-tab link with a similarity score.
- Session: a topic-oriented browsing grouping connected to tabs.
- MemoryCluster: a semantic grouping connected to sessions.

`GraphService` exposes topic and entity graph projections. `GraphAnalysisService` builds an in-memory NetworkX graph for rankings and communities. `RecommendationService` derives topics/tabs from it. `KnowledgeGraphService` is a separate SQL projection by entity name.

This is useful graph-oriented storage, but it is not yet a reliable GraphRAG graph. Entity relationships are stored but graph traversal SQL and a legacy `EntityRelationshipService` refer to a prior `entity_a/entity_b/weight` schema. Graph APIs are unauthenticated and global. Repairing that contract, adding ownership, and measuring retrieval contribution must precede multi-hop GraphRAG.
