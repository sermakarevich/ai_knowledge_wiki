#!/bin/bash
# Chapter 12: start the RAGFlow stack (time-boxed experiment — see findings note).
# Clones RAGFlow at a pinned tag into data/ragflow/ (gitignored), selects the
# slim image in docker/.env, maps UI 8085 / API 9385, and starts compose.
# x86-only images: under Docker Desktop emulation on Apple Silicon this may
# fail — the failure is recorded in runs/12_findings.md, not retried past ~2h.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# NOTE (verified 2026-09-09 via Docker Hub tag list): `-slim` tags stop at
# v0.21.1 — there is NO slim build for the pinned v0.27.1, so "slim at a
# pinned recent tag" is impossible. The script pins the full image below;
# on this 16 GB-budget ARM Mac the stack is expected to fail (x86-only
# single-arch manifest + >=16 GB RAM minimum) — record the failure, keep the
# survey entry, do not retry past ~2 h.
TAG="${RAGFLOW_TAG:-v0.27.1}"
DEST="$ROOT/data/ragflow"

if [ ! -d "$DEST/.git" ]; then
  git clone --depth 1 --branch "$TAG" https://github.com/infiniflow/ragflow.git "$DEST"
else
  echo "reusing existing clone at $DEST"
fi

cd "$DEST/docker"
# Pin the same image the tag's own docker/.env defaults to.
sed -i.bak 's|^RAGFLOW_IMAGE=.*|RAGFLOW_IMAGE=infiniflow/ragflow:v0.27.1|' .env

# UI on 8085, API on 9385 (avoid clashing with the tutorial's other services).
SVR_HTTP_PORT="${SVR_HTTP_PORT:-8085}" API_PORT="${API_PORT:-9385}" docker compose up -d
echo "RAGFlow starting: UI http://localhost:8085 API http://localhost:9385"
