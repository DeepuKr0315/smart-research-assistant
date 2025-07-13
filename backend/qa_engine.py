from backend.gemini_client import generate_text
import re


def clean_output(text: str) -> str:
    """
    Cleans Gemini output: removes markdown and formatting artifacts.
    """
    if not text:
        return ""
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)           # Remove bold/italic markdown
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)    # Remove numbered prefixes
    return text.strip()


def answer_question(question: str, context: str) -> dict:
    """
    Uses Gemini to answer a question grounded in the provided document context.

    Returns:
        dict: {
            "answer": cleaned answer,
            "justification": extracted justification (or fallback)
        }
    """

    if not context or "Error" in context:
        return {
            "answer": "Please upload a valid document first.",
            "justification": ""
        }

    prompt = (
        f"Answer the following question based strictly on the document context. "
        f"If the answer is not in the document, say so clearly.\n\n"
        f"Include a brief justification — e.g., 'Based on paragraph 3' or similar.\n\n"
        f"Format:\nAnswer: <answer>\nJustification: <reasoning>\n\n"
        f"Question: {question}"
    )

    try:
        response = generate_text(prompt, context)

        if not response or "error" in response.lower():
            return {
                "answer": "⚠️ Unable to generate answer.",
                "justification": ""
            }

        # Attempt to extract Answer + Justification
        answer = response
        justification = "Justification: Based on document content."

        if "Justification:" in response:
            parts = response.split("Justification:", 1)
            answer = parts[0].strip()
            justification = parts[1].strip()

        return {
            "answer": clean_output(answer),
            "justification": clean_output(justification)
        }

    except Exception as e:
        err_msg = str(e)
        if "429" in err_msg:
            return {
                "answer": "⚠️ Rate limit exceeded. Try again later or upgrade your plan.",
                "justification": ""
            }

        return {
            "answer": f"⚠️ Error generating answer: {err_msg}",
            "justification": ""
        }