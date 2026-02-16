
# Devcontainer Dockerfile for LifeWeaver starter
ARG VARIANT="3.10"
FROM python:${VARIANT}-slim

# Install basic deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    wget \
    curl \
    ca-certificates \
    tesseract-ocr \
    ffmpeg \
    poppler-utils \
    libgl1 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user 'vscode' with home
RUN useradd -m vscode && mkdir -p /home/vscode/workspace && chown -R vscode:vscode /home/vscode
WORKDIR /workspace

# Copy repo contents (done by devcontainer build context)
COPY . /workspace
RUN chown -R vscode:vscode /workspace

USER vscode
ENV PATH="/home/vscode/.local/bin:$PATH"

# Install pip requirements (inside container this runs postCreateCommand as well)
RUN python -m pip install --upgrade pip && pip install --user -r requirements.txt || true

CMD ["/bin/bash"]
