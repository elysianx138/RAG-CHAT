from langchain_core.messages import AIMessage
from app.config import settings
from langchain.chat_models import init_chat_model

def generation_node(state):

    messages = state["messages"]

    context = state["context"]

    question = messages[-1].content

    llm = init_chat_model(
        model=settings.LLM_MODEL,
        api_key=settings.GROQ_API_KEY
    )

    prompt = f"""
Use context to answer:

{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "messages": [
            AIMessage(content=response.content)
        ]
    }