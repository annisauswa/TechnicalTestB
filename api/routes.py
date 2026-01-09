from fastapi import APIRouter, Request, HTTPException
from api.models import QuestionRequest, DocumentRequest
import time

def create_router(workflow, document_store):
    router = APIRouter()

    @router.post("/ask")
    def ask_question(req: QuestionRequest):
        start = time.time()
        try:
            result = workflow.ask(req.question)

            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add")
    def add_document(req: DocumentRequest):
        try:
            doc_id = document_store.add_document(req.text)

            return {
                "id": doc_id, 
                "status": "added"
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status")
    def status():
        return {
            "qdrant_ready": document_store.client is not None,
            "in_memory_docs_count": document_store.document_count,
            "graph_ready": workflow is not None
        }
    
    return router