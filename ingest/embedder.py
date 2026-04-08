from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings


def get_embedding():

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )