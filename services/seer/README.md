# Seer service

This service provides the /divine endpoint to query the local Seer (Ollama + Chroma memory).

Planned endpoints:
- POST /divine { "query": "..." } -> { answer, sources, confidence }
- GET /health -> basic liveness

Adapters are stubs and must be replaced with real Chroma/mesh/Ollama integrations.
