import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Safety check for missing key
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, context: str = "", max_tokens: int = 200) -> str:
    """
    Calls Gemini API with a structured prompt grounded in document context.

    Args:
        prompt (str): User instruction (question/task)
        context (str): Document content (used as grounding)
        max_tokens (int): Max output length

    Returns:
        str: Gemini response or error message
    """

    if not context or "Error" in context:
        return "⚠️ Please upload a valid document first."

    # Build prompt
    full_prompt = f"""
You are an AI assistant. Answer based strictly on the context below.
Provide a short, clear response. If unknown, say so.
Also add: "Justification: ..." at the end of your answer.

Instruction: {prompt}

Context:
{context[:3000]}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")
        response = model.generate_content(full_prompt)
        result = response.text.strip()

        return result if result else "⚠️ Empty response from Gemini."

    except Exception as e:
        error_msg = str(e).lower()
        print("Gemini API Error:", error_msg)

        if "429" in error_msg:
            return (
                "⚠️ Rate limit exceeded. Wait for daily reset or upgrade plan.\n"
                "🔗 https://aistudio.google.com/app/billing"
            )
        elif "400" in error_msg:
            return "❌ Invalid API request. Check your input or model name."
        elif "permission" in error_msg:
            return "🚫 Access denied. Verify your API key permissions."
        else:
            return f"❌ Gemini API Error: {str(e)}"