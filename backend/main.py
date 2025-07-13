import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.parser import read_document
from backend.summarizer import generate_summary
from backend.qa_engine import answer_question
from backend.challenge_engine import generate_questions, evaluate_answer
from backend.models import (
    DocumentResponse,
    DocumentRequest,
    SummaryResponse,
    QuestionRequest,
    AnswerResponse,
    ChallengeRequest,
    ChallengeResponse,
    EvaluationRequest,
    EvaluationResponse,
)
app = FastAPI()

# Allow Postman or frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Smart Assistant for Research Summarization",
        "endpoints": {
            "/upload": "POST - Upload a document (PDF/TXT)",
            "/summarize": "POST - Generate summary from uploaded text"
        }
    }

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        temp_path = f"./temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)

        text = read_document(temp_path)

        os.remove(temp_path)  # 🧹 Delete after processing

        return {
            "filename": file.filename,
            "text_preview": text[:1000] + "..." if len(text) > 1000 else text,
            "full_text": text
        }
    except Exception as e:
        return {
            "filename": "",
            "text_preview": f"Error: {str(e)}",
            "full_text": f"Error: {str(e)}"
        }

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_document(request: DocumentRequest):
    result = generate_summary(request.text)

    if not result or not isinstance(result, dict) or not result.get("summary"):
        return {
            "summary": "Summary generation failed or returned no text.",
            "word_count": 0
        }

    return result

@app.post("/qa", response_model=AnswerResponse)
async def ask_anything(request: QuestionRequest):
    result = answer_question(request.question, request.context)
    return result

@app.post("/challenge", response_model=ChallengeResponse)
async def challenge_me(request: ChallengeRequest):
    result = generate_questions(request.context)
    return result

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_user_answer(request: EvaluationRequest):
    result = evaluate_answer(request.question, request.user_answer, request.context)
    return result