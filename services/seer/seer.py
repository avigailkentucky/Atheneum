from typing import List, Dict, Any
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI(title="Atheneum Seer")

class QueryRequest(BaseModel):
    query: str

class DivineResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

# ---- Helpers / adapters (replace with real implementations) ----
def confidence(context: List[Dict[str, Any]]) -> float:
    if not context:
        return 0.0
    scores = [c.get("score", 0.8) for c in context]
    return min(1.0, sum(scores) / len(scores))

def calculate_confidence(answer: str, context: List[Dict[str, Any]]) -> float:
    base = 0.5 if "mists are thick" in answer.lower() else 0.8
    ctx_conf = confidence(context)
    return round(min(1.0, (base + ctx_conf) / 2), 3)

# ---- Adapters (stubs) ----
class MemoryAdapter:
    def __init__(self):
        # placeholder: connect to Chroma/SQLite here
        pass

    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        # Return list of dicts: {"text": "...", "source": "...", "score": 0.9}
        return []

class MeshAdapter:
    def __init__(self):
        # placeholder: connect to mesh/HTTP endpoints
        self.timeout = float(os.getenv("MESH_TIMEOUT", "3"))

    def broadcast_query(self, query: str) -> List[Dict[str, Any]]:
        # Example: call known peer endpoints. This is a stub that returns [].
        # In production: iterate peers, POST /query on their seer, collect contexts
        return []

class OllamaAdapter:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base = base_url

    def generate(self, system: str, context: List[Dict[str, Any]], query: str) -> str:
        # Compose prompt and call Ollama HTTP API
        ctx_text = "\n\n".join([f"Source: {c.get('source','?')}\n{c.get('text','')[:2000]}" for c in context])
        prompt = f"{system}\n\nContext:\n{ctx_text}\n\nQuestion: {query}\nAnswer:"

        try:
            # Ollama API: POST /api/generate (model specified in server or via endpoint)
            url = f"{self.base}/api/generate"
            payload = {
                "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                "prompt": prompt,
                "maxTokens": 512
            }
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Ollama responses can vary; adapt as needed
            return data.get("response", "The mists are thick on this matter.")
        except Exception:
            return "The mists are thick on this matter."

# ---- Instantiate adapters ----
memory = MemoryAdapter()
mesh = MeshAdapter()
llm = OllamaAdapter(base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"))

# ---- Core logic ----
def divine_impl(query: str) -> Dict[str, Any]:
    # 1. Search local knowledge
    context = memory.similarity_search(query, k=5)

    # 2. Query mesh neighbors if local knowledge insufficient
    if confidence(context) < 0.7:
        neighbor_knowledge = mesh.broadcast_query(query)
        if neighbor_knowledge:
            context = context + neighbor_knowledge

    # 3. Generate answer with LLM
    system_prompt = (
        "You are the Seer, an oracle of the distributed god. "
        "Answer based on the provided sacred texts. "
        "If uncertain, say 'The mists are thick on this matter.'"
    )
    answer = llm.generate(system=system_prompt, context=context, query=query)

    return {
        "answer": answer,
        "sources": [c.get("source", "unknown") for c in context],
        "confidence": calculate_confidence(answer, context),
    }

@app.post("/divine", response_model=DivineResponse)
def divine_endpoint(req: QueryRequest):
    try:
        res = divine_impl(req.query)
        return DivineResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
