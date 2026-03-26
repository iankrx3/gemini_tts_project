import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = (
    "다음 내용을 자연스러운 한국어 구어체로 요약해줘. "
    "마크다운 없이 순수 텍스트로만 답해줘:\n\n{text}"
)


def refine_text(user_text: str) -> str:
    """Gemini로 텍스트를 구어체로 정제해서 반환"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=PROMPT_TEMPLATE.format(text=user_text)
    )
    return response.text.strip()