import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from gtts import gTTS
from gemini_logic import refine_text

load_dotenv()
app = Flask(__name__, static_folder="static")

AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/generate-tts", methods=["POST"])
def generate_tts():
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "텍스트를 입력해주세요."}), 400

    user_text = data["text"].strip()

    # 1. Gemini로 텍스트 정제
    try:
        ai_text = refine_text(user_text)
    except Exception as e:
        return jsonify({"error": f"Gemini API 오류: {str(e)}"}), 500

    # 2. gTTS로 음성 변환
    try:
        filename = f"{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text=ai_text, lang="ko")
        tts.save(audio_path)
    except Exception as e:
        return jsonify({"error": f"TTS 변환 오류: {str(e)}"}), 500

    return jsonify({
        "message": "성공",
        "original_text": user_text,
        "ai_text": ai_text,
        "audio_url": f"/static/audio/{filename}"
    })


if __name__ == "__main__":
    app.run(debug=True, port=8080)