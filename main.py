from fastapi import FastAPI
from qdrant_client import QdrantClient

from config import settings
from api.routes import router
from core.document_store import DocumentStore
from core.rag_workflow import RagWorkflow
from core.agent_state import AgentState
from embeddings.fake import EmbeddingService


def create_app() -> FastAPI:
    app = FastAPI(title="Learning RAG Demo")

    embedder = EmbeddingService()

    try:
        client = QdrantClient(settings.qdrant_url, port=settings.port)
    except Exception:
        client = None

    store = DocumentStore(
        client=client,
        embedder=embedder,
        collection_name=settings.collection_name
    )

    workflow = RagWorkflow(AgentState, store)

    app.state.store = store
    app.state.workflow = workflow

    app.include_router(router)

    return app

app = create_app()