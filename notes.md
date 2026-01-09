<div id="user-content-toc">
  <ul align="center" style="list-style: none;">
    <summary>
      <h1>Code Documentation</h1>
    </summary>
  </ul>
</div>

## Code Structure

```
project-root/
├── api/
│   ├── __init__.py
│   ├── models.py          # Request/response schemas
│   └── router.py          # HTTP endpoints (/ask, /add, /status)
│
├── core/
│   ├── __init__.py
│   ├── agent_state.py     # Shared workflow state definition
│   ├── document_store.py  # Qdrant + in-memory document storage
│   └── rag_workflow.py    # Retrieval and answer workflow (LangGraph)
│
├── embeddings/
│   ├── __init__.py
│   ├── base.py            # BaseEmbedding abstraction
│   └── fake.py            # Fake embedding implementation
│
├── config.py              # Environment-based configuration
├── main.py                # Application entry point
├── notes.md               # Design decisions and trade-offs
├── requirements.txt
└── README.md
```

## How to Run

```
conda create --name myenv python=3.9
conda activate myenv
pip install -r requirements.txt

docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

python main.py or uvicorn main:app --reload # for development
```

<h1> Refactored Codebase </h1>

## Main Design Decisions

I separated the codebase into four main responsibilities:

- `Embedding` part of the data access layer, responsible for vector generation
- `Document storage and retrieval` part of the data access layer, handling Qdrant and in-memory fallback
- `RAG workflow` business logic for retrieval and answer generation
- `API handling` web logic for processing HTTP requests

I introduced a dedicated embeddings module with a `BaseEmbedding` abstraction so future developers can easily replace the current fake embedder with a real implementation without changing the rest of the system.

I also defined base models for the workflow state and API schemas to make future changes more localized and easier to manage.

The `rag_workflow` and `document_store` modules are placed in the same `core` directory because they are closely related, and I think grouping them together improves readability and maintainability of the retrieval generation pipeline.

## Trade-offs Considered

A drawback of this refactoring is that it `increases the size and complexity` of the codebase, which may be unnecessary for a very small project.

The use of abstractions and interfaces introduces additional `indirection that isn't necessary` at this scale. With multiple files and modules, developers need more time to `understand the project structure` and how different `components interact`.

However, this trade-off was intentional `to achieve loose coupling, easier extensibility, and better long-term scalability`.

## How This Improves Maintainability

Although the codebase is larger, it is significantly easier to maintain and scale.

- The system is **modular**, with `clear responsibilities` for each component.
- `Changes` to embeddings, document storage, or workflow logic `don't affect the API layer` which means it's easier to maintain and scale.
- New implementations (e.g., a real embedding model or a different vector store) can be added `without modifying existing code`.
- The `abstraction layers` make the system easier to extend, test, and evolve over time.

Overall, the refactored structure favors long-term maintainability and scalability over short-term simplicity.
