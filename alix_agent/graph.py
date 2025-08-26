from langgraph.graph import StateGraph, END
from .models.types import State
from .agents.classifier import classify_node
from .agents.compliance import compliance_node

def build_graph():
    g = StateGraph(State)
    g.add_node("classify", classify_node)
    g.add_node("compliance", compliance_node)
    g.set_entry_point("classify")
    g.add_edge("classify", "compliance")
    g.add_edge("compliance", END)
    return g.compile()

APP = build_graph()