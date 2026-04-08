from langchain.chat_models import init_chat_model

from rag.prompt import get_prompt
from app.config import settings

def build_chain(retriever, memory):

    llm = init_chat_model(
        model=settings.LLM_MODEL,
        api_key=settings.GROQ_API_KEY
    )

    prompt = get_prompt()

    chain = (
        {
            "context": retriever,
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
    )

    return chain