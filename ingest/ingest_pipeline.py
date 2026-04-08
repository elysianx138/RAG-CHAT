from ingest.pdf_loader import load_pdf
from ingest.md_loader import load_markdown
from ingest.web_loader import load_web
from ingest.splitter import split_documents

from vectorstore.pinecone_store import get_vectorstore


def ingest_file(file_path):

    if file_path.endswith(".pdf"):
        docs = load_pdf(file_path)

    elif file_path.endswith(".md"):
        docs = load_markdown(file_path)

    else:
        raise ValueError("Unsupported file")

    chunks = split_documents(docs)

    vectorstore = get_vectorstore()

    vectorstore.add_documents(chunks)

    return len(chunks)