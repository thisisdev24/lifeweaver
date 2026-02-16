
# LifeWeaver — Starter Repo (MVP scaffold)

This repository is a starter scaffold for **LifeWeaver 2.0** — an offline-first temporal-causal personal memory & action agent (MVP).
It includes a Python microservice skeleton, a VS Code devcontainer, Dockerfile, and sample modules for ingestion, embeddings, KG, RAG and a safe micro-action executor.

This scaffold is intentionally minimal and designed to run in **WSL Ubuntu** + **VS Code** + **Docker** using the Remote - Containers extension.

## What's included
- Python package skeleton: `app/` with modules: `ingest`, `embeddings`, `kg`, `rags`, `planner`, `executor`
- `requirements.txt` with recommended packages
- `Dockerfile` to build a reproducible dev environment (CPU-only)
- `.devcontainer/` for VS Code Remote - Containers integration
- `scripts/bootstrap.sh` to build and run the container locally for testing
- `docker-compose.yml` (optional) for future expansion
- Example CLI and FastAPI entrypoint: `app/main.py`

---
## Quick flow (high level)
1. Build Docker image (see `scripts/bootstrap.sh`)
2. Open repository in VS Code and attach to the container (Remote - Containers)
3. Run the app inside the container: `python -m app.main`
4. Use sample endpoints / CLI to ingest files and request summaries / suggestions.

---
## Next steps
Follow the detailed setup guide in `SETUP_INSTRUCTIONS.md` included in this repo (step-by-step for a fresh WSL Ubuntu + VS Code + Docker setup).
