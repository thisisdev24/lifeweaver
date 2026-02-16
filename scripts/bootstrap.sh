
#!/usr/bin/env bash
set -e
CMD=${1:-build}
IMAGE_NAME=lifeweaver-dev:latest
if [ "$CMD" = "build" ]; then
  echo "Building Docker image ${IMAGE_NAME} ..."
  docker build -t ${IMAGE_NAME} .
  echo "Built ${IMAGE_NAME}. To run: ./scripts/bootstrap.sh run"
elif [ "$CMD" = "run" ]; then
  echo "Running container (interactive)..."
  docker run --rm -it -p 8000:8000 -p 8888:8888 -v $(pwd):/home/devuser/app ${IMAGE_NAME} /bin/bash
else
  echo "Unknown command. Usage: ./scripts/bootstrap.sh [build|run]"
fi
