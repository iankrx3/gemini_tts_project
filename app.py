import os
from flask import Flask, request, send_file
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS

load_dotenv()
app = Flask(__name__)

# Gemini 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/generate-tts', methods=['POST'])
def generate_tts():
    user_text = request.json.get('text')
    
    # 1. Gemini로 텍스트 생성 (또는 입력된 텍스트 정제)
    response = model.generate_content(f"다음 내용을 자연스러운 구어체로 요약해줘: {user_text}")
    ai_text = response.text

    # 2. gTTS로 음성 변환
    tts = gTTS(text=ai_text, lang='ko')
    audio_path = "static/audio/result.mp3"
    tts.save(audio_path)

    return {"message": "성공", "text": ai_text, "audio_url": "/static/audio/result.mp3"}

if __name__ == '__main__':
    app.run(debug=True)