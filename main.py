from fastapi import FastAPI
from qdrant_client import QdrantClient

from config import settings
from api.routes import create_router
from core.document_store import DocumentStore
from core.rag_workflow import RagWorkflow
from core.agent_state import AgentState
from embeddings.fake import EmbeddingService

def create_app() -> FastAPI:
    app = FastAPI(title="Learning RAG Demo")
    embedder = EmbeddingService()
    document_store = DocumentStore(
                embedder=embedder,
                collection_name=settings.collection_name
            )
    workflow = RagWorkflow(document_store)

    app.include_router(
            create_router(workflow, document_store)
        )

    return app

app = create_app()