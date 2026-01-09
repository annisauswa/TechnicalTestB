from fastapi import FastAPI
from qdrant_client import QdrantClient

from config import settings
from api.routes import router
from embeddings.fake import FakeEmbedding
from core.rag import RAG
from core.agentic_graph import build_graph
from core.agent_state import AgentState


def create_app() -> FastAPI:
    app = FastAPI(title="Learning RAG Demo")

    retriever = RAG()

    graph = build_graph(AgentState, retriever)

    app.state.retriever = retriever
    app.state.graph = graph

    app.include_router(router)

    return app

app = create_app()