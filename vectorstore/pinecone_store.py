from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from ingest.embedder import get_embedding
from app.config import settings


def init_pinecone_index():

    pc = Pinecone(
        api_key=settings.PINECONE_API_KEY
    )

    index_name = settings.PINECONE_INDEX_NAME

    # 如果 index 不存在就创建
    if index_name not in pc.list_indexes().names():

        pc.create_index(
            name=index_name,
            dimension=384,  # MiniLM-L6-v2 = 384
            metric="cosine"
        )

    return pc.Index(index_name)


def get_vectorstore():

    embedding = get_embedding()

    index = init_pinecone_index()

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embedding
    )

    return vectorstore