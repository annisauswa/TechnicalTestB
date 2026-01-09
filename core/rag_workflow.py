from langgraph.graph import StateGraph, END
from core.agent_state import AgentState
from core.document_store import DocumentStore

class RagWorkflow():
    def __init__(self, document_store: DocumentStore):
        self.document_store = document_store

    def _retrieve(self, state: AgentState) -> AgentState:
        query = state["question"]
        state["context"] = self.document_store.search(query)
        return state

    def _answer(self, state: AgentState) -> AgentState:
        context = state["context"]
        if context:
            answer = f"I found this: '{context[0][:100]}...'"
        else:
            answer = "Sorry, I don't know."
        state["answer"] = answer
        return state
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        
        return workflow.compile()
    
    def ask(self, query:str) -> AgentState:
        workflow = self._build_graph()
        return workflow.invoke({"question": query})