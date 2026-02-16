
# Top-level Dockerfile to build the development image (same as devcontainer/Dockerfile)
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential wget curl ca-certificates tesseract-ocr ffmpeg poppler-utils libgl1 libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m devuser
WORKDIR /home/devuser/app
COPY . /home/devuser/app
RUN chown -R devuser:devuser /home/devuser/app
USER devuser
ENV PATH="/home/devuser/.local/bin:$PATH"
RUN python -m pip install --upgrade pip && pip install --user -r requirements.txt || true
CMD ["/bin/bash"]
