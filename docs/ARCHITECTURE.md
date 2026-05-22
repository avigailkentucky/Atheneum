# Architecture

Atheneum is composed of several subsystems:

- mesh: P2P discovery and encrypted tunnels (WireGuard) for node-to-node communication
- crypto: Key management and quantum-resistant primitives
- message: Protocol buffers for node messaging
- heartbeat: Health checks and failure detection
- ingestion: semantic chunking and embedding (Ollama)
- storage: IPFS (Kubo) for immutable content storage
- index: SQLite + Chroma vector DB for queryable knowledge
- dashboard: React app for visualization and exploration

This document is an overview. Each subsystem lives under pkg/ and should expose a Start() or Init() function.
