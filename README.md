# 📄 Smart Research Assistant 🤖

An AI-powered assistant that reads research papers (PDF/TXT), generates concise summaries, answers custom questions with document-backed justifications, and challenges users with logic-based questions. Built with 🧠 LLaMA 3, 🧰 FastAPI, and 💡 Gradio.

---

## 🚀 Features

- 📂 **Upload PDF or TXT** documents
- 📝 **Auto-summary** (≤150 words) using LLaMA 3
- ❓ **Ask Anything** – free-form Q&A with contextual understanding
- 🧠 **Challenge Me** – logic-based questions generated from the document
- 🧾 **Justifications** – every answer backed with a document snippet
- 🎯 Designed for researchers, students, and document reviewers

---

## 🧱 Project Structure
```
smart-research-assistant/
│
├── app.py               # Gradio interface
├── app_streamlit.py     # Optional Streamlit interface
├── parser.py            # PDF/TXT parser
├── summarization.py     # LLaMA 3-based summarizer
├── qa_engine.py         # Ask Anything engine
├── challenge_engine.py  # Challenge Me logic
├── README.md            # Project overview
├── .gitignore           # Excludes pycache, env files, etc.
```

---

## 🛠️ Tech Stack

- **Frontend:** Gradio / Streamlit
- **Backend:** FastAPI
- **LLM:** LLaMA 3 via Ollama
- **Vector Search:** FAISS
- **Parsing:** PyMuPDF
- **Embeddings:** sentence-transformers
- **Extras:** LangChain (optional memory), Markdown formatting, Justification snippets

---

## ⚙️ Setup Instructions

### 1. 🧩 Install Dependencies
```
pip install fastapi uvicorn gradio langchain sentence-transformers faiss-cpu pymupdf
```

### 2. 📥 Install Ollama & LLaMA 3
•	Download Ollama: https://ollama.com/download
•	Pull the model:
    `ollama pull llama3`

### 3. 🚀 Run the Application
Option A: Gradio Interface
`python app.py`

Option B: Streamlit Interface
`streamlit run app_streamlit.py`

## 💡 Usage Guide
	1.	Upload a .pdf or .txt file.
	2.	View auto-generated summary in the Summary tab.
	3.	Switch to Ask Anything tab to ask questions.
	4.	Use Challenge Me tab to test your understanding with AI-generated logic questions.

## 🙌 Credits

Built by Deepanshu Kumar as part of EZ’s Intern Task.

Inspired by real-world document assistants and powered by open-source LLMs.
