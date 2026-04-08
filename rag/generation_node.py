from functools import lru_cache

from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq

from app.config import settings


@lru_cache(maxsize=1)
def get_llm():
    return ChatGroq(
        model=settings.LLM_MODEL,
        api_key=settings.GROQ_API_KEY
    )


def generation_node(state):

    messages = state["messages"]

    context = state["context"]

    question = messages[-1].content
    history = "\n".join(
        f"{message.type}: {message.content}"
        for message in messages[:-1]
    )

    if settings.USE_LOCAL_RAG:
        if context.strip():
            answer = (
                "Based on the uploaded context, here is a concise answer:\n\n"
                f"{context}"
            )
        else:
            answer = "I could not find relevant information in the uploaded documents."
        return {
            "messages": [
                AIMessage(content=answer)
            ]
        }

    llm = get_llm()

    prompt = f"""
Use the conversation history and retrieved context to answer the user's question.
Prefer the history if the user is asking to recall something from the current chat.

Conversation history:
{history or "(no prior history)"}

Retrieved context:
{context or "(no retrieved context)"}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "messages": [
            AIMessage(content=response.content)
        ]
    }
