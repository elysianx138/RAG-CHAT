from langgraph.graph import StateGraph

from rag.state import GraphState
from rag.retriever_node import retrieve_node
from rag.generation_node import generation_node

from memory.sqlite_checkpoint import build_checkpointer


def build_graph():

    builder = StateGraph(GraphState)

    builder.add_node(
        "retrieve",
        retrieve_node
    )

    builder.add_node(
        "generate",
        generation_node
    )

    builder.set_entry_point("retrieve")

    builder.add_edge(
        "retrieve",
        "generate"
    )

    checkpointer = build_checkpointer()

    graph = builder.compile(
        checkpointer=checkpointer
    )

    return graph