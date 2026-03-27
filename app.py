import io
from flask import Flask, request, jsonify, send_from_directory, Response
from dotenv import load_dotenv
from gtts import gTTS
from gemini_logic import refine_text

load_dotenv()
app = Flask(__name__, static_folder="static")


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

    # 2. ai_text를 JSON으로 먼저 반환 (프론트에서 /generate-audio로 별도 요청)
    return jsonify({
        "message": "성공",
        "original_text": user_text,
        "ai_text": ai_text,
    })


@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "텍스트를 입력해주세요."}), 400

    text = data["text"].strip()

    # gTTS로 음성 변환 → 메모리 버퍼에 저장
    try:
        tts = gTTS(text=text, lang="ko")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
    except Exception as e:
        return jsonify({"error": f"TTS 변환 오류: {str(e)}"}), 500

    return Response(
        buf,
        mimetype="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"}
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=9999)