import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = (
    "다음 내용을 자연스러운 한국어 높임말로 바꿔줘"
    "마크다운 없이 순수 텍스트로만 답해줘:\n\n{text}"
)

def refine_text(user_text: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(PROMPT_TEMPLATE.format(text=user_text))
    return response.text.strip()