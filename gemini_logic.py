import os
import time
import random
from google import genai
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = (
    "다음 내용을 자연스러운 한국어 높임말로 바꿔줘. "
    "마크다운 없이 순수 텍스트로만 답해줘:\n\n{text}"
)

def refine_text(user_text: str, max_retries: int = 5) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=PROMPT_TEMPLATE.format(text=user_text)
            )
            return response.text.strip()
        
        except Exception as e:
            if "429" in str(e):
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited. {attempt + 1}/{max_retries}번 재시도 중... ({wait:.1f}초 대기)")
                time.sleep(wait)
            else:
                raise  # 429 외 다른 에러는 즉시 raise
    
    raise RuntimeError("최대 재시도 횟수 초과. 잠시 후 다시 시도해주세요.")