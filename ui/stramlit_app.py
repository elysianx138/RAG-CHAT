import streamlit as st
import requests

st.title("Smart RAG Assistant")

query = st.text_input("Ask a question")

if query:

    response = requests.post(
        "http://localhost:8000/chat",
        json={"query": query}
    )

    st.write(response.json()["answer"])