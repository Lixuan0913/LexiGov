from flask import Flask, render_template, request, jsonify, send_file
from google.cloud import texttospeech
from faster_whisper import WhisperModel
import io
import os
from query_data import rag_engine
import tempfile



model = WhisperModel("medium", device="cpu")

app = Flask(__name__)

def transcribe_audio(audio_path):
    try:
        segments, info = model.transcribe(audio_path,
                                  task="transcribe",   # ensures no translation
                                   temperature=0,
                                   best_of=5,
                                   beam_size=5)

        text = " ".join([segment.text for segment in segments]).strip()
        language = info.language

        return text,language
    except Exception as e:
        print(f"Error in Whisper transcription: {e}")
        return None, None



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    response, sources = rag_engine(text)
    
    return jsonify({
        "answer": response,
        "sources": sources
    })


@app.route("/transcribe", methods=["POST"])
def transcribe():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]

    # Create a temporary file path but close the file immediately to avoid Windows locking issues
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio_path = temp_audio.name
    
    try:
        audio_file.save(temp_audio_path)
        raw_text, language = transcribe_audio(temp_audio_path)
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
    
    if not raw_text:
        return jsonify({"error": "Transcription failed"}), 500

    response,sources = rag_engine(raw_text)
    
    return jsonify({
    "language": language,
    "transcription": raw_text,
    "answer": response,
    "sources": sources
  })



@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("lang", "en")

    client = texttospeech.TextToSpeechClient()

    language_map = {
        "en": "en-US",
        "ms": "ms-MY",
        "zh": "cmn-CN",
        "th": "th-TH"
    }

    language_code = language_map.get(lang, "en-US")

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  # nicer voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return send_file(
        io.BytesIO(response.audio_content),
        mimetype="audio/mpeg"
    )
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
