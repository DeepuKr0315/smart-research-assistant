from backend.gemini_client import generate_text
import re

def clean_output(text: str) -> str:
    """Removes markdown, numbers, and cleans up Gemini output."""
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)  # remove bold/italic
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)  # remove numbered lists
    return text.strip()

def generate_questions(context: str) -> dict:
    if not context:
        return {"questions": "Please upload a document first."}

    prompt = """
Generate exactly 3 logic-based or comprehension-focused questions from the document.
Do NOT use markdown formatting.
Use plain text only.
Make them meaningful and challenging.
"""

    questions = generate_text(prompt, context)
    return {"questions": clean_output(questions)}

def evaluate_answer(question: str, user_answer: str, context: str) -> dict:
    if not context:
        return {"feedback": "Please upload a document first."}

    prompt = f"""
Evaluate the user's answer to the following question based on the provided document content.

If the user's answer is blank, vague, or avoids addressing the question (e.g., 'I don't know', 'Not sure'), respond with:
"⚠️ The user did not provide a meaningful answer."

Otherwise, assess the correctness of the response:
- Is the answer factually accurate?
- Does it align with the information in the document?
- Provide justification citing relevant parts of the document.

Question: {question}
User Answer: {user_answer}

Document:
\"\"\"{context[:3000]}\"\"\"
"""

    feedback = generate_text(prompt, context)
    return {"feedback": clean_output(feedback)}