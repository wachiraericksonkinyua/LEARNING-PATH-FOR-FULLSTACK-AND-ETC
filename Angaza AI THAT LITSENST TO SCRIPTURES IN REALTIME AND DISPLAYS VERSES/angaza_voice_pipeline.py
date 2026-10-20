"""
Angaza Voice Pipeline (Optimized for Groq & Edge-TTS)
ASR: Groq Whisper API (Lightning fast, free tier)
TTS: Edge-TTS (High-quality Microsoft Neural voices, free)
"""

import os
import io
import asyncio
import base64
from pathlib import Path
from groq import Groq
import edge_tts

# Initialize Groq Client (Ensure GROQ_API_KEY is in your .env or export)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─────────────────────────────────────────────
# ASR - SPEECH TO TEXT (GROQ)
# ─────────────────────────────────────────────

def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """
    Uses Groq Whisper-large-v3. 
    Instant transcription that doesn't heat up your ThinkPad CPU.
    """
    if not os.environ.get("GROQ_API_KEY"):
        return "[Error: GROQ_API_KEY not set]"

    try:
        with open(audio_path, "rb") as f:
            # We use the large-v3 model as it has excellent Swahili (sw) support
            response = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f,
                language=language,
                response_format="text"
            )
        return response.strip()
    except Exception as e:
        return f"[ASR Error: {str(e)}]"


# ─────────────────────────────────────────────
# TTS - TEXT TO SPEECH (EDGE-TTS)
# ─────────────────────────────────────────────

async def synthesize_speech(text: str, language: str = "en") -> bytes:
    """
    Uses Microsoft Edge Neural voices. 
    'sw-KE-ZuriNeural' is specifically optimized for Kenyan Swahili.
    """
    # VOICE_MAP optimized for Angaza's reverent tone
    VOICE_MAP = {
        "en": "en-KE-ChilembaNeural",   # Kenyan English (Sounds local/authentic)
        "sw": "sw-KE-ZuriNeural",       # Kenyan Swahili (Very natural)
    }
    
    voice = VOICE_MAP.get(language, "en-KE-ChilembaNeural")
    
    # Rate -10% makes the scripture reading feel more calm and meditative
    communicate = edge_tts.Communicate(text, voice=voice, rate="-10%")

    buf = io.BytesIO()
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        return buf.getvalue()
    except Exception as e:
        print(f"TTS Error: {e}")
        return b""


# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────

def audio_to_base64(audio_bytes: bytes) -> str:
    """Convert audio bytes to base64 string for API response."""
    return base64.b64encode(audio_bytes).decode("utf-8")


# ─────────────────────────────────────────────
# DEMO / TEST RUN
# ─────────────────────────────────────────────

async def main_demo():
    print("🎙️ Starting Angaza Voice Pipeline (Groq + Edge)...")
    
    # Test TTS - Swahili
    test_text = "Usifadhaike, maana Bwana Mungu wako yu pamoja nawe."
    print(f"Generating Swahili Audio: '{test_text}'")
    
    audio_data = await synthesize_speech(test_text, "sw")
    
    if audio_data:
        output_file = "angaza_response.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"✅ Success! Audio saved to: {output_file}")
    else:
        print("❌ TTS Failed.")

if __name__ == "__main__":
    # To run the test: python angaza_voice_pipeline.py
    asyncio.run(main_demo())