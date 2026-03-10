import speech_recognition as sr
import whisper
import tempfile
import os

# using medium model
model_name = "medium" 
print(f"Loading Whisper model '{model_name}' (this might take a moment)...")
model = whisper.load_model(model_name)

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()

    # Increase sensitivity to quiet speech
    recognizer.energy_threshold = 300 
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("--- Adjusting for ambient noise (please stay silent) ---")
        # Increase duration to 2 seconds for a better noise floor profile
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("Ready! Speak now...")
        audio = recognizer.listen(source,
                                  timeout=5,           # wait up to 5 seconds for speech to start
                                  phrase_time_limit=30)  # stop listening after 30 seconds of silence
        
        print("Processing locally using Whisper...")

        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio.get_wav_data())
            temp_audio_path = f.name

    try:
        # Initial prompt helps Whisper with context, punctuation, and specific terminology
        prompt = "This is a multilingual conversation. The user is speaking asean language. Please transcribe the speech."

        # beam_size=5 and best_of=5 improve accuracy by searching for more possible transcriptions
        result = model.transcribe(
            temp_audio_path, 
            initial_prompt=prompt,
            beam_size=5,
            best_of=5,
            temperature=0.0 # Greedy decoding at first, most stable
        )

        print("\n--- Transcription Result ---")
        print("Detected language:", result["language"])
        print("You said:", result["text"].strip())
        print("----------------------------")

    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

recognize_speech_from_mic()