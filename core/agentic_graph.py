from langgraph.graph import StateGraph, END
from core.agent_state import AgentState
from core.rag import RAG

def build_graph(state_cls: type[AgentState], retriever: RAG):
    def simple_retrieve(state: AgentState) -> AgentState:
        query = state["question"]
        state["context"] = retriever.search(query)
        return state

    def simple_answer(state: AgentState) -> AgentState:
        ctx = state["context"]
        if ctx:
            answer = f"I found this: '{ctx[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state

    workflow = StateGraph(state_cls)
    workflow.add_node("retrieve", simple_retrieve)
    workflow.add_node("answer", simple_answer)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "answer")
    workflow.add_edge("answer", END)
    
    return workflow.compile()