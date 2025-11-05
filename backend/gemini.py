import google.generativeai as genai

# -------------------- API KEY (Hardcoded since you prefer it) --------------------
API_KEY = "AIzaSyAAwVW6h-qpSpLWu-uDevqT-VLuaez3F6Y"

if not API_KEY:
    raise ValueError("❌ No API key found. Hardcode it or use .env.")

genai.configure(api_key=API_KEY)


# -------------------- GENERATE NOTES FUNCTION --------------------
def generate_notes(text: str) -> str:
    """
    Convert raw text into structured study notes using Gemini.
    Ensures clean output with summary, key points, and takeaway.
    """

    prompt = f"""
You are an intelligent study notes generator.
Convert the following text into well-structured, easy-to-study notes.

Important Rules:
- Do NOT add any extra information not provided by the user.
- Keep the notes concise, clear, and academically formatted.

Return output in the following structure:

**Title**
A short and meaningful title.

**Summary (3-5 bullets)**
• Key high-level insights

**Key Points**
• Important statements, facts, or concepts

**Definitions / Terms (if applicable)**
Term: Meaning

**Conclusion / Takeaway**
1-2 sentence conclusion.

--- BEGIN TEXT ---
{text}
--- END TEXT ---
"""

    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            safety_settings={  # Allow academic output without blocking
                "HARASSMENT": "BLOCK_NONE",
                "HATE": "BLOCK_NONE",
                "SEXUAL": "BLOCK_NONE",
                "DANGEROUS": "BLOCK_NONE",
            }
        )

        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            return "⚠️ Could not generate notes. Try again."

        return response.text.strip()

    except Exception as e:
         print("⚠️ GEMINI FULL ERROR:", type(e).__name__, str(e))
         raise e  # ← let the backend show the real error in terminal


