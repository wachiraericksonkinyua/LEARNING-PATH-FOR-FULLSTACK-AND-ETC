"""
Angaza FastAPI Backend
Voice-first church AI assistant API
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64, os, tempfile

# ─── Import Angaza modules ───
# from rag_engine import AngazaRAGEngine, UserContext
# from voice_pipeline import transcribe_audio, synthesize_speech

app = FastAPI(
    title="Angaza API",
    description="Church-Oriented AI Voice Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────

class TextQueryRequest(BaseModel):
    user_id: str
    text: str
    language: str = "en"          # "en" | "sw"
    emotional_state: Optional[str] = None

class ScriptureResponse(BaseModel):
    reference: str
    text: str
    version: str
    devotional_note: str
    audio_base64: Optional[str] = None   # TTS output

class PrayerRequest(BaseModel):
    user_id: str
    prayer_text: str
    category: str = "general"    # "healing" | "provision" | "thanksgiving" | "general"
    language: str = "en"

class EventQueryRequest(BaseModel):
    user_id: str
    query: str                   # "What time is the youth service?"
    church_id: str

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/")
def health():
    return {"status": "🕊️ Angaza is alive", "version": "1.0.0"}


@app.post("/voice/transcribe")
async def transcribe_voice(audio: UploadFile = File(...), language: str = "en"):
    """
    ASR endpoint - Accepts audio file, returns transcript.
    Uses: OpenAI Whisper (local, free) or Groq Whisper API (free tier)
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        # transcript = transcribe_audio(tmp_path, language=language)
        transcript = "I feel anxious about tomorrow"   # STUB for demo

        return {"transcript": transcript, "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/scripture/by-emotion", response_model=ScriptureResponse)
async def get_scripture_by_emotion(req: TextQueryRequest):
    """
    Core RAG endpoint: Returns a scripture verse matched to user's emotional state.
    Also generates TTS audio of the verse + devotional note.
    """
    # ctx = UserContext(
    #     user_id=req.user_id,
    #     emotional_state=req.emotional_state or "",
    #     language=req.language
    # )
    # result = rag_engine.retrieve_scripture(ctx, req.text)
    # audio = synthesize_speech(f"{result.reference}. {result.text}. {result.devotional_note}", lang=req.language)

    # STUB RESPONSE for documentation purposes
    return ScriptureResponse(
        reference="Philippians 4:6-7",
        text="Do not be anxious about anything, but in every situation, by prayer...",
        version="NIV",
        devotional_note="God's peace surpasses human understanding. Your worries are safe in His hands.",
        audio_base64=None
    )


@app.post("/scripture/ask")
async def ask_theological_question(req: TextQueryRequest):
    """General theological Q&A with safety guardrails."""
    # answer = rag_engine.answer_question(req.text, language=req.language)
    return {
        "answer": "The Bible teaches that God is with you in every season. (Stub response)",
        "source": "Angaza Scripture Engine v1"
    }


@app.post("/prayer/submit")
async def submit_prayer_request(req: PrayerRequest):
    """
    Records a prayer request for the pastoral team.
    Production: Store in PostgreSQL, notify pastor via email/SMS
    """
    # TODO: db.save_prayer_request(req)
    # TODO: notify_pastor(req)
    return {
        "status": "received",
        "message": "Your prayer request has been received. The pastoral team will be praying for you. 🙏",
        "prayer_id": f"PR-{req.user_id}-001"
    }


@app.get("/church/{church_id}/events")
async def get_church_events(church_id: str, query: Optional[str] = None):
    """
    Returns upcoming church events. Production: Connect to church CMS/Google Calendar.
    """
    # TODO: Integrate with church management system
    stub_events = [
        {"name": "Sunday Service", "time": "9:00 AM", "day": "Sunday", "location": "Main Sanctuary"},
        {"name": "Youth Service", "time": "4:00 PM", "day": "Friday", "location": "Youth Hall"},
        {"name": "Bible Study", "time": "7:00 PM", "day": "Wednesday", "location": "Room 101"},
        {"name": "Choir Practice", "time": "5:00 PM", "day": "Saturday", "location": "Music Room"},
    ]
    return {"church_id": church_id, "events": stub_events}


@app.post("/giving/guide")
async def voice_giving_guide(req: TextQueryRequest):
    """Voice-guided digital giving instructions."""
    instructions = {
        "en": "To give your tithe, visit our church website or dial *123# on your mobile phone. May God bless your giving. 🙏",
        "sw": "Kutoa zaka yako, tembelea tovuti yetu au piga *123# kwenye simu yako. Mungu akubariki. 🙏"
    }
    return {"instructions": instructions.get(req.language, instructions["en"])}
