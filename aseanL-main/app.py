from flask import Flask, render_template, request, jsonify
from faster_whisper import WhisperModel
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


if __name__ == "__main__":
    app.run(debug=True)