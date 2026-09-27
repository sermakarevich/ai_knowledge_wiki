#!/bin/bash
# Chapter 12: stop the RAGFlow stack (keeps the gitignored clone + volumes).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/data/ragflow/docker"
docker compose down
echo "RAGFlow stopped"
