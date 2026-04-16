"""
文件名：api/chat_routers.py
最后修改时间：2026-04-16
模块功能：提供聊天接口，接收用户问题与会话 ID，并返回答案和检索调试信息。
模块相关技术：FastAPI、Pydantic、LangGraph、LangChain 消息类型、异常处理。
"""

from functools import lru_cache

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter()


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    session_id: str = "default"


@lru_cache(maxsize=1)
def get_graph():
    from rag.graph import build_graph

    return build_graph()


@router.post("/chat")
def chat(payload: ChatRequest):
    from langchain_core.messages import HumanMessage

    try:
        response = get_graph().invoke(
            {
                "messages": [
                    HumanMessage(content=payload.query)
                ]
            },
            config={"configurable": {"thread_id": payload.session_id}},
        )
    except Exception as exc:
        error_name = exc.__class__.__name__
        if error_name == "AuthenticationError":
            provider_label = "OpenAI" if "openai" in str(type(exc)).lower() else "Groq"
            key_name = "OPENAI_API_KEY" if provider_label == "OpenAI" else "GROQ_API_KEY"
            raise HTTPException(
                status_code=502,
                detail=(
                    f"{provider_label} 鉴权失败：当前 {key_name} 无效或已失效。"
                    f"请更新 .env 中的 {key_name}，或把 USE_LOCAL_RAG 设为 true 后重启服务。"
                ),
            ) from exc
        raise HTTPException(
            status_code=500,
            detail=f"聊天流程执行失败：{exc}",
        ) from exc

    return {
        "answer": response["messages"][-1].content,
        "session_id": payload.session_id,
        "debug_context": response.get("context", ""),
        "retrieval_query": response.get("retrieval_query", ""),
        "retrieval_scores": response.get("retrieval_scores", []),
    }
