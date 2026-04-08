from langchain_core.prompts import ChatPromptTemplate

def get_prompt():

    return ChatPromptTemplate.from_template(
        """
Use the following context to answer:

{context}

Question:
{question}
"""
    )