from fastapi import APIRouter, Request, HTTPException
from api.models import QuestionRequest, DocumentRequest
import time

router = APIRouter()

@router.post("/ask")
def ask_question(req: QuestionRequest, request: Request):
    start = time.time()
    try:
        graph = request.app.state.graph
        result = graph.invoke({"question": req.question})

        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_document(req: DocumentRequest, request: Request):
    try:
        retriever = request.app.state.retriever
        doc_id = retriever.add_document(req.text)

        return {
            "id": doc_id, 
            "status": "added"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def status(request: Request):
    retriever = request.app.state.retriever
    docs_count = retriever.document_count

    return {
        "qdrant_ready": True if retriever.client else False,
        "in_memory_docs_count": docs_count,
        "graph_ready": request.app.state.graph is not None
    }