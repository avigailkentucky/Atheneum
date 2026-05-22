# Atheneum

Atheneum is a privacy-first, peer-to-peer knowledge management system.

It ingests content, semantically chunks it, generates local embeddings (via Ollama), stores immutable content on IPFS, and exposes a queryable index (SQLite + Chroma). It also includes a Veil Mesh P2P layer, quantum-resistant crypto primitives, and a dashboard for visualization ("The God's Eye").

This repository contains an initial scaffold for the Go backend and a placeholder for the frontend.

Quick start (backend):

1. Install Go (1.20+)
2. go build ./...
3. go run ./cmd

See docs/ARCHITECTURE.md for an overview of components and responsibilities.
