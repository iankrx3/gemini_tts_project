import os
from google import genai
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = (
    "다음 내용을 자연스러운 한국어 높임말로 바꿔줘. "
    "마크다운 없이 순수 텍스트로만 답해줘:\n\n{text}"
)

def refine_text(user_text: str) -> str:
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=PROMPT_TEMPLATE.format(text=user_text)
    )
    
    # 최신 SDK에서는 response.text로 결과에 접근
    return response.text.strip()