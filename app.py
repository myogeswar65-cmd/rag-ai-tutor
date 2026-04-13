import os
import shutil
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.document_loaders import PyPDFLoader

# Page config
st.set_page_config(page_title="AI Tutor", layout="wide")

# UI styling
st.markdown("""
<style>
html, body { background-color: #0e1117; }

.chat-container {
    max-width: 800px;
    margin: auto;
    padding-bottom: 100px;
}

.user-msg {
    background-color: #1f6feb;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    width: fit-content;
    margin-left: auto;
}

.bot-msg {
    background-color: #30363d;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    width: fit-content;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Advanced RAG AI Tutor")

# Sidebar (PDF Upload)
st.sidebar.header("📄 Upload Study Material")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs", type="pdf", accept_multiple_files=True
)

# Embeddings
embeddings = HuggingFaceEmbeddings()

db_path = os.path.join(os.getcwd(), "db")

# Process PDFs
if uploaded_files:
    all_docs = []

    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())

        loader = PyPDFLoader(file.name)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(all_docs)

    # Reset DB
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    db = FAISS.from_documents(split_docs, embeddings)
    db.save_local(db_path)

    st.sidebar.success("✅ PDFs processed successfully!")

# Load DB
if os.path.exists(db_path):
    db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
else:
    st.warning("⚠️ Upload PDFs to start")
    st.stop()

# LLM
llm = Ollama(model="mistral")

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
query = st.chat_input("Ask your question...")

if query:
    docs = db.similarity_search(query, k=5)
    context = "\n".join([doc.page_content for doc in docs])

    # Memory context
    history = "\n".join([f"{r}: {m}" for r, m in st.session_state.messages])

    prompt = f"""
You are a helpful AI tutor.

Use previous conversation if relevant.

Chat History:
{history}

Context:
{context}

Question:
{query}

Give a detailed, simple explanation with examples.
"""

    response = llm.invoke(prompt)

    st.session_state.messages.append(("User", query))
    st.session_state.messages.append(("Bot", response))

# Display chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "User":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sources
if st.session_state.messages:
    with st.expander("📖 Source Chunks"):
        docs = db.similarity_search(query, k=3)
        for i, doc in enumerate(docs):
            st.write(f"Chunk {i+1}")
            st.write(doc.page_content)
            st.write("---")