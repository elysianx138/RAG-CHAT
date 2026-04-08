from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from rag.graph import build_graph


router = APIRouter()

graph = build_graph()


@router.post("/chat")
def chat(query: str, session_id: str):

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        },
        config={
            "configurable": {
                "thread_id": session_id
            }
        }
    )

    return {
        "answer":
        response["messages"][-1].content
    }