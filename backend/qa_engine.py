from backend.gemini_client import generate_text
import re

def clean_output(text: str) -> str:
    """Remove markdown and unwanted formatting from Gemini output."""
    if not text:
        return ""
    # Remove markdown bold/italic
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
    # Remove numbered list prefixes
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    return text.strip()

def answer_question(question: str, context: str) -> dict:
    """
    Uses Gemini to answer a question based on the provided document context.
    Returns answer + justification.
    """
    if not context or "Error" in context:
        return {
            "answer": "Please upload a valid document first.",
            "justification": ""
        }

    prompt = f"""
Answer the following question clearly and accurately using only information from the document.
If the information is not present, say so clearly.

Include a brief justification stating where in the document this information comes from,
such as 'Based on paragraph 3 of section 2' or similar.

If the user's question is vague or cannot be answered due to insufficient context, respond with:
"⚠️ Unable to answer due to insufficient information."

Question: {question}

Document:
\"\"\"{context[:3000]}\"\"\"
"""

    try:
        response = generate_text(prompt, context)

        if not response or "error" in response.lower():
            return {
                "answer": "⚠️ Unable to generate answer.",
                "justification": ""
            }

        if "Justification:" in response:
            answer, justification = response.split("Justification:", 1)
        else:
            answer = response
            justification = "Justification: Based on document content."

        return {
            "answer": clean_output(answer),
            "justification": clean_output(justification)
        }

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return {
                "answer": "⚠️ Rate limit exceeded. Please upgrade to a paid plan or try again later.",
                "justification": ""
            }
        return {
            "answer": f"⚠️ Error generating answer: {error_msg}",
            "justification": ""
        }