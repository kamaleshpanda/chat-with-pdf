import os
import tempfile
import streamlit as st
from embedchain import App
import base64
from streamlit_chat import message

def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "llama3.2:latest",
                    "base_url": "http://localhost:11434",
                },
            },
            "vectordb": {
                "provider": "chroma",
                "config": {"dir": db_path},
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "llama3.2:latest",
                    "base_url": "http://localhost:11434",
                },
            },
        }
    )
#Inside the App we have all 3 components - llm, vectordb, embedder
st.title('Chat with PDF using Llama 3.2')
st.header('This is locally running')

db_path = tempfile.mkdtemp()
# we are making a temp. database [folder] to store embeddings
if 'app' not in st.session_state:
    st.session_state['app'] = embedchain_bot(db_path)
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    #This creates a empty list to store chat history
with st._main:
    st.header("Pdf Upload")
    pdf_file = st.file_uploader("Choose a pdf file", type=["pdf"])

    if pdf_file is None:
        st.write("There is no pdf file, pls upload a pdf")
    if pdf_file:
        st.success("Pdf Uploaded successfully")
    #Button to process pdf
    if st.button("Upload"):
        st.spinner("Uploading PDF...")


