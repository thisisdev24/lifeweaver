
# Detailed Setup Instructions (WSL Ubuntu + VS Code + Docker)

These instructions assume nothing is installed. Follow every step exactly. Use a clean WSL Ubuntu distribution.

## 1) WSL Ubuntu: ensure you have WSL2 and Ubuntu installed
- On Windows: enable WSL and install Ubuntu from Microsoft Store.
- Set WSL version to 2: `wsl --set-default-version 2`
- Launch Ubuntu and update packages:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl wget git
```

## 2) Install Docker Desktop and enable WSL 2 integration
- Install Docker Desktop for Windows (https://www.docker.com/get-started). During install, enable WSL 2 and integrate your Ubuntu distribution.
- After installation, open Docker Desktop > Settings > Resources > WSL Integration, and enable your Ubuntu distro.
- Verify Docker in WSL:
```bash
docker version
docker run hello-world
```

## 3) Install VS Code and required extensions
- Install VS Code on Windows.
- In VS Code, install these extensions:
  - "Remote - WSL" (ms-vscode-remote.remote-wsl)
  - "Remote - Containers" (ms-vscode-remote.remote-containers)
  - "Python" (ms-python.python)
  - "Jupyter" (ms-toolsai.jupyter)
  - "Pylance" (ms-python.vscode-pylance)

## 4) Clone this repo inside WSL Ubuntu
From WSL terminal:
```bash
cd ~
git clone <this-repo-url-or-copy-files-here> lifeweaver
cd lifeweaver
```

(If you downloaded the scaffold archive, extract it into `~/lifeweaver`)

## 5) Build the Docker dev container (one-time)
Inside WSL terminal (in the repo root):
```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh build
```

This will build an image named `lifeweaver-dev:latest`. Building may take 10-30 minutes because Python packages and models are installed.

## 6) Open the project in VS Code and attach to the container
- In VS Code, open the `lifeweaver` folder.
- Press `F1` → `Remote-Containers: Reopen in Container` (or use the green bottom-left icon).
- VS Code will build/attach to the container and install recommended extensions inside it.

## 7) Run the service
Inside the container terminal in VS Code:
```bash
python -m app.main
# or run the API server with uvicorn:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000/docs` to see API docs (if running uvicorn).

## 8) Using the CLI
There are simple CLI scripts under `app/cli` (see files). Example:
```bash
python -m app.cli.ingest_file --file sample_data/sample.pdf
python -m app.cli.query --q "summarize project X"
```

## Troubleshooting
- If Docker build fails due to package installs, ensure WSL has internet and Docker Desktop integration is enabled.
- If `faiss` install fails, the Dockerfile has a fallback to install `faiss-cpu` or a pure Python fallback; follow the logs and ask for help.
- If local LLM models are too large, the scaffold uses small/sentence-transformers for embeddings and small local models for summarization. You can also configure hosted LLM keys via `.env` to use OpenAI temporarily.

