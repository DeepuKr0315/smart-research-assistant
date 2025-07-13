# 📄 Smart Research Assistant 🤖

An AI-powered assistant that reads research papers (PDF/TXT), generates concise summaries, answers custom questions with document-backed justifications, and challenges users with logic-based comprehension questions.

Built using 💡 Google Gemini API, 🧠 FastAPI, and 🎨 Gradio — crafted for researchers, students, and professionals who need to quickly understand and explore lengthy documents.

---

## 🚀 Features

- 📂 **Upload** `.pdf` or `.txt` research papers
- 📝 **Auto-Summarization** (≤150 words) using Google Gemini
- ❓ **Ask Anything** — free-form Q&A with citation-style justifications
- 🧠 **Challenge Me** — logic-based question generator + evaluator
- 🧾 **Justification Support** — all answers backed by document snippets
- 🎯 Interactive **Gradio UI** + modular **FastAPI backend**
- 📡 Gemini fallback handling + API test utility

---

## 🧱 Project Structure

```
smart-research-assistant/
│
├── backend/                         # All backend logic + FastAPI entry point
│   ├── main.py                      # FastAPI main application
│   ├── parser.py                    # PDF/TXT document parser (pdfplumber)
│   ├── summarizer.py                # Summary generator using Gemini
│   ├── qa_engine.py                 # Q&A logic via Gemini
│   ├── challenge_engine.py          # Question generation + evaluation
│   ├── gemini_client.py             # Gemini API wrapper
│   └── models.py                    # Pydantic models for FastAPI
│
├── frontend/
│   └── app.py                       # Gradio interface
│
├── .env                             # Environment file (GEMINI_API_KEY)
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## 🛠️ Tech Stack

| Layer     | Tools/Frameworks              |
|-----------|-------------------------------|
| LLM       | 🌐 Google Gemini API (`gemini-2.5-flash`) |
| Frontend  | 🎨 Gradio                    |
| Backend   | ⚙️ FastAPI + Pydantic         |
| Parsing   | 📄 pdfplumber                 |
| Hosting   | 🔁 Uvicorn (Local Server)     |

---

## ⚙️ Setup Instructions

### 1. 📦 Install Required Packages

```pip install -r requirements.txt```
**Or manually:** ```pip install fastapi uvicorn gradio python-dotenv pdfplumber google-generativeai```

## 2. 🔐 Configure Environment

Create a `.env` file in the root directory with your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> 💡 Make sure you do **not** share your `.env` file or expose your API key in public repositories.

## 3. 🚀 Run the App

### ➤ Start the FastAPI backend server:

```
uvicorn backend.main:app --reload
```

This will start the backend on: `http://127.0.0.1:8000`

### ➤ Launch the Gradio frontend:

```
python frontend/app.py
```

This will open the smart assistant in your browser (usually at `http://127.0.0.1:7860`).

---

---

## 📮 API Endpoints (For Postman)

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | `/upload`      | Upload a document (PDF/TXT)        |
| POST   | `/summarize`   | Generate summary from text         |
| POST   | `/qa`          | Answer custom question             |
| POST   | `/challenge`   | Generate logic-based questions     |
| POST   | `/evaluate`    | Evaluate user’s answer             |

---

## 🧪 Usage Flow

1. 📂 Upload a `.pdf` or `.txt` document
2. 📝 Read its summary (auto-generated)
3. ❓ Ask questions about the document
4. 🧠 Try answering logic-based questions and get feedback
5. 📚 Review all justifications to build deeper understanding

---

## 🙌 Credits

Built with ❤️ by **Deepanshu Kumar**  
🎓 Task submitted for **EZ Intern Assignment (NIET - July 2025)**  
Inspired by document intelligence tools and educational copilots.