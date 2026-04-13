import os
import shutil
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# File path
file_path = os.path.join("data", "notes.txt")

# Read file
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

print("✅ Text loaded")

# Split text
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.create_documents([text])

print(f"✅ Documents created: {len(docs)}")

# Local embeddings
embeddings = HuggingFaceEmbeddings()

# DB path
db_path = os.path.join(os.getcwd(), "db")

# Delete old DB
if os.path.exists(db_path):
    shutil.rmtree(db_path)

# Create DB
db = FAISS.from_documents(docs, embeddings)

# Save DB
db.save_local(db_path)

print("✅ SUCCESS: Data embedded and stored!")