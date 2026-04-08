from langchain_core.messages import HumanMessage

from vectorstore.pinecone_store import get_vectorstore


def retrieve_node(state):

    messages = state["messages"]

    last_message = messages[-1]

    query = last_message.content

    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever()

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return {
        "context": context
    }