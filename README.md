# 🤖 RAG AI Tutor Bot (Offline & Intelligent)

## 📌 Problem Statement
In large-scale learning environments, students often struggle to get timely, accurate, and personalized answers. Traditional AI systems may generate incorrect responses (hallucinations), leading to misinformation.

## 💡 Solution
This project implements a **Retrieval-Augmented Generation (RAG) based AI Tutor** that:
- Retrieves relevant information from a knowledge base
- Generates accurate, context-based answers
- Eliminates hallucinations by grounding responses in real data

---

## 🧠 System Architecture

User Query  
→ Embedding Model  
→ Vector Database (FAISS)  
→ Relevant Context Retrieval  
→ LLM (Ollama - Mistral/Phi)  
→ Final Answer  

---

## 🚀 Features

- 📄 Upload and process PDF study materials  
- 💬 ChatGPT-style conversational UI  
- 🧠 Context-aware memory (multi-turn chat)  
- 🔍 Accurate answers using RAG (no hallucination)  
- ⚡ Fully offline (no API cost, no rate limits)  
- 📖 Source context display for transparency  

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- LangChain  
- FAISS (Vector Database)  
- Ollama (Local LLM - Mistral / Phi)  
- Sentence Transformers (Embeddings)  

---

---

## ▶️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/rag-ai-tutor.git
cd rag-ai-tutor
pip install -r requirements.txt
streamlit run app.py