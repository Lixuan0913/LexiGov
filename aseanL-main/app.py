import os
import io
import tempfile
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from google.cloud import texttospeech
from faster_whisper import WhisperModel
from query_data import rag_engine

app = FastAPI()

# Sets up the templates folder just like Flask's render_template
templates = Jinja2Templates(directory="templates")

# --- LAZY LOADING WHISPER TO PREVENT TIMEOUTS ---
whisper_model = None

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        print("Loading Whisper model for the first time...")
        whisper_model = WhisperModel("small", device="cpu") 

    return whisper_model

def transcribe_audio(audio_path):
    try:
        model = get_whisper_model()
        segments, info = model.transcribe(
            audio_path,
            task="transcribe",
            temperature=0,
            best_of=5,
            beam_size=5
        )
        text = " ".join([segment.text for segment in segments]).strip()
        language = info.language
        return text, language
    except Exception as e:
        print(f"Error in Whisper transcription: {e}")
        return None, None

# --- DATA MODELS (FastAPI replaces request.json with Pydantic) ---
class ChatRequest(BaseModel):
    text: str

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(data: ChatRequest):
    if not data.text:
        raise HTTPException(status_code=400, detail="No text provided")

    response, sources = rag_engine(data.text)
    
    return {
        "answer": response,
        "sources": sources
    }


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    if not audio:
        raise HTTPException(status_code=400, detail="No audio file uploaded")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio_path = temp_audio.name
        # FastAPI reads files asynchronously
        content = await audio.read()
        temp_audio.write(content)
    
    try:
        raw_text, language = transcribe_audio(temp_audio_path)
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
    
    if not raw_text:
        raise HTTPException(status_code=500, detail="Transcription failed")

    response, sources = rag_engine(raw_text)
    
    return {
        "language": language,
        "transcription": raw_text,
        "answer": response,
        "sources": sources
    }


@app.post("/tts")
async def tts(data: TTSRequest):
    client = texttospeech.TextToSpeechClient()

    language_map = {
        "en": "en-US",
        "ms": "ms-MY",
        "zh": "cmn-CN",
        "th": "th-TH"
    }
    language_code = language_map.get(data.lang, "en-US")

    synthesis_input = texttospeech.SynthesisInput(text=data.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return StreamingResponse(
        io.BytesIO(response.audio_content),
        media_type="audio/mpeg"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)