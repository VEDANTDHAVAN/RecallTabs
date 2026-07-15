# Migrations

Alembic migrations live in `services/api/migrations/versions`. They create tabs/users, add tab metadata/chunks/AI metadata, tab relationships, sessions/clusters, conversations/messages/sources, searchability, memory importance, topics, entities, and entity relationships.

The migration history is not presently a trustworthy linear baseline. The recent topic migration (`07568a53edf0`) declares `8e1b19a7ac18` as its parent even though it creates structures referenced by earlier migrations. The entity-relationship migration (`bf7bf42cbc00`) contains only `pass`. Several SQLAlchemy models and repositories disagree on columns. An `alembic heads` diagnostic did not return within the audit timeout in the current environment, so the active database revision was not assumed.

Before any schema feature:

1. Run Alembic history/heads against the intended environment.
2. Compare model metadata, migration head, and a schema-only database inspection.
3. Add a dedicated reconciliation migration; never edit applied revisions.
4. Test upgrade and downgrade on an empty database and a representative existing database.
5. Plan data backfill and indexes separately from API behavior changes.

The `d40cdf6f45c2` migration drops an `idx_tabs_search` index during upgrade and only recreates it on downgrade. Search performance must be verified before production migration.
