import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Loaded Gemini API key: {GEMINI_API_KEY}")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def clean_output(text: str) -> str:
    """
    Remove markdown and unwanted formatting from Gemini output.
    """
    if not text:
        return ""
    # Remove markdown bold/italic
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
    # Remove numbered list prefixes
    text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)
    return text.strip()

def generate_summary(text: str, max_words: int = 150) -> dict:
    """
    Generates a concise summary of the provided document text using Gemini.

    Args:
        text (str): The full extracted text from the document
    
    Returns:
        dict: {"summary": str, "word_count": int}
    """
    if not text or "Error" in text:
        return {
            "summary": "No document uploaded or invalid input.",
            "word_count": 0
        }

    prompt = """
Generate a concise summary of the following research document in under 150 words.
Focus on key findings, methodology, and conclusions.
Avoid markdown and keep it plain text.
"""

    try:
        # Only one model call
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite-preview-06-17")
        full_prompt = f"{prompt}\n\n{text[:3000]}"
        
        print("Sending prompt to Gemini...")
        response = model.generate_content(full_prompt)
        summary = response.text.strip()

        if not summary:
            return {
                "summary": "⚠️ Empty summary received from Gemini.",
                "word_count": 0
            }

        # Enforce word limit
        summary = ' '.join(summary.split()[:max_words]) + ('...' if len(summary.split()) > max_words else '')

        return {
            "summary": clean_output(summary),
            "word_count": len(summary.split())
        }

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return {
                "summary": "⚠️ Rate limit exceeded. Please upgrade to a paid plan or try again later.",
                "word_count": 0
            }
        return {
            "summary": f"⚠️ Error generating summary: {error_msg}",
            "word_count": 0
        }