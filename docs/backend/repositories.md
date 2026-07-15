# Repositories

Repositories wrap synchronous SQLAlchemy sessions and commit each mutation independently.

| Repository | Data/query responsibility | Notes |
| --- | --- | --- |
| `TabRepository` | tab CRUD, user tab list, timeline, topic statistics, PostgreSQL full-text and domain search | Search/timeline are currently not user scoped. |
| `TabChunkRepository` | chunk writes, semantic tab search, chunk retrieval | pgvector raw SQL and fixed 45% filter for search results. |
| `TopicRepository`, `EntityRepository` | lookup/create/update and vector similarity | Topic/entity vectors are defined as 1536 dimensions. |
| `SessionRepository`, `MemoryClusterRepository` | CRUD and vector search | Session vector query expects an `embedding` column absent from the current model/migration. |
| `ConversationRepository`, `MessageRepository`, `UserRepository` | conversation/message/user persistence | Ownership is not enforced in fetch/update/delete operations. |
| `TabEntityRepository`, `EntityAliasRepository`, `EntityRelationshipRepository`, `TabRelationshipRepository` | graph link persistence | `EntityRelationshipRepository` matches the current typed relationship model. |
| `GraphRepository`, `KnowledgeGraphRepository`, `GraphTraversalRepository` | graph view/traversal SQL | Some queries use obsolete relationship or importance column names. |
| `MemoryImportanceRepository` | basic tab lookup/save/list | Duplicates `TabRepository` and has no active caller. |

Raw SQL is parameterized for values, but repository result DTOs are ad hoc dictionaries. The codebase should add stable read models before changing external API response shapes.

Important query/model mismatches: `GraphTraversalRepository` expects `entity_a_id`, `entity_b_id`, and `weight`; the model stores `source_entity_id`, `target_entity_id`, `relationship_type`, and `confidence`. `KnowledgeGraphRepository` orders by non-existent `memory_clusters.importance` and `tabs.importance` instead of current fields. These queries need tests and a migration/model audit before activation.
