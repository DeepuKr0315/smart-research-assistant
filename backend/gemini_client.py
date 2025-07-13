import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Add fail-safe check
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_text(prompt: str, context: str = "", max_tokens: int = 200):
    """
    Sends a prompt to Gemini API and returns the response.
    
    Ensures all answers are grounded in provided document context.
    
    Args:
        prompt (str): Instruction for Gemini
        context (str): Document content for grounding
        max_tokens (int): Max output length
    
    Returns:
        str: Gemini's response or error message
    """
    if not context or "Error" in context:
        return "⚠️ Please upload a valid document first."

    full_prompt = f"""
You are an AI assistant tasked with answering questions based on research documents.
Answer the following instruction using only information from the provided context.
If the information isn't present, say so clearly.
Include a brief justification citing where the answer comes from in the document.

Instruction:
\"\"\"{prompt}\"\"\"

Context:
\"\"\"{context[:3000]}\"\"\"
"""

    try:
        # Only one model is used — no fallbacks
        model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")
        response = model.generate_content(full_prompt)
        result = response.text.strip()

        if not result:
            return "⚠️ Empty response from Gemini."

        return result

    except Exception as e:
        error_msg = str(e).lower()
        print("Gemini API Error:", error_msg)

        if "429" in error_msg:
            return """
⚠️ You've exceeded your Gemini API quota. 

💡 Solutions:
1. Wait until your quota resets (usually daily).
2. Upgrade to a paid plan at https://aistudio.google.com/app/billing 
"""
        elif "400" in error_msg:
            return "❌ Invalid API request. Check your input or model name."
        elif "permission" in error_msg:
            return "🚫 Permission denied. Make sure your API key has access."
        else:
            return f"❌ Gemini API Error: {error_msg}"