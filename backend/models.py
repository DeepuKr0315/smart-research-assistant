from pydantic import BaseModel

# Document Upload
class DocumentResponse(BaseModel):
    filename: str
    text_preview: str
    full_text: str

# Summary
class DocumentRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    word_count: int

# QA Mode
class QuestionRequest(BaseModel):
    question: str
    context: str

class AnswerResponse(BaseModel):
    answer: str
    justification: str

# Challenge Mode
class ChallengeRequest(BaseModel):
    context: str

class ChallengeResponse(BaseModel):
    questions: str

class EvaluationRequest(BaseModel):
    question: str
    user_answer: str
    context: str

class EvaluationResponse(BaseModel):
    feedback: str