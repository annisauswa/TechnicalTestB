from fastapi import APIRouter, Request, HTTPException
from api.models import QuestionRequest, DocumentRequest
import time

router = APIRouter()

@router.post("/ask")
def ask_question(req: QuestionRequest, request: Request):
    start = time.time()
    try:
        workflow = request.app.state.workflow
        result = workflow.invoke({"question": req.question})

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
        store = request.app.state.store
        doc_id = store.add_document(req.text)

        return {
            "id": doc_id, 
            "status": "added"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def status(request: Request):
    store = request.app.state.store
    docs_count = store.document_count

    return {
        "qdrant_ready": store.client is not None,
        "in_memory_docs_count": docs_count,
        "graph_ready": request.app.state.workflow is not None
    }