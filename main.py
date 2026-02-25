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
                    "model": "nomic-embed-text",
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
with st.sidebar:
    st.header("Pdf Upload")
    pdf_file = st.file_uploader("Choose a pdf file", type=["pdf"])

    if pdf_file is None:
        st.write("There is no pdf file, pls upload a pdf")
    ## not needed if pdf_file:
    ## not needed st.success("Pdf Uploaded successfully")
    #Button to process pdf
    if st.button("Upload"):
        with st.spinner("Uploading PDF..."):

            #uploaded pdf saved temporarily
            with tempfile.NamedTemporaryFile(delete=False , suffix ='.pdf') as tmp:
                tmp.write(pdf_file.getvalue())
                temp_path = tmp.name

                #add pdf to RAG
            st.session_state['app'].add(temp_path, data_type='pdf_file')

                #delete temporarily file
            os.remove(temp_path)

        st.success("All set. You can now ask questions about it.")

question = st.text_input("Ask a question about the PDF")

if question:
    with st.spinner("Thinking........"):
        response = st.session_state["app"].chat(question)
    st.write("### Answer:")
    st.write(response)

