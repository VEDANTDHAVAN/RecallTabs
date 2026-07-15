# Deployment and Docker

No Dockerfiles, compose files, Kubernetes manifests, CI workflow, or deployment scripts are present in the repository. The `docker/` directory is empty.

Current local prerequisites are Node 18+, pnpm, Python 3.11+, PostgreSQL with pgvector, an API environment file, and local Ollama. The extension defaults to `http://localhost:8000`; its production mode is a source-level boolean rather than an environment-driven build configuration.

Production deployment is not yet ready. Before adding Docker artifacts, stabilize the migration baseline, authenticate all data paths, make provider configuration explicit, move long capture work off request threads, add dependency health checks, and define secret-management and observability requirements.
