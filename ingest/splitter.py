from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def split_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,  # 每块最大字符数
        chunk_overlap=settings.CHUNK_OVERLAP,  # 块之间的重叠字符数
        length_function=len,  # 计算长度的函数
        separators=["\n\n", "\n", "。", "！", "？", " ", ""]  # 分割优先级
    )

    return splitter.split_documents(docs)