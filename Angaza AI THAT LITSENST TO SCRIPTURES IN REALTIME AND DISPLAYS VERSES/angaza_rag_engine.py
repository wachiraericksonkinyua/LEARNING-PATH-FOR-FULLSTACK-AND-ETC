"""
Angaza RAG Engine - Emotion-Aware Scripture Retrieval
Uses HuggingFace embeddings (free) + FAISS vector store (free) + Groq LLM (free tier)
Author: Angaza Lead AI Engineer
"""

import os
import json
import numpy as np
from dataclasses import dataclass
from typing import Optional
from groq import Groq
from sentence_transformers import SentenceTransformer
import faiss

# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class ScriptureResult:
    reference: str       # e.g. "Philippians 4:6-7"
    text: str            # Full verse text
    version: str         # KJV / NIV / ESV
    relevance_score: float
    devotional_note: str # Short AI-generated reflection

@dataclass
class UserContext:
    user_id: str
    emotional_state: str        # "anxious", "grieving", "joyful", etc.
    language: str = "en"        # "en" | "sw" (Swahili)
    church_id: Optional[str] = None
    previous_verses: list = None  # For avoiding repetition

# ─────────────────────────────────────────────
# EMOTION → THEOLOGICAL TOPIC MAPPING
# ─────────────────────────────────────────────

EMOTION_TOPICS = {
    "anxious":    ["peace", "trust in God", "do not worry", "casting cares"],
    "grieving":   ["comfort", "mourning", "God heals the brokenhearted", "hope"],
    "lonely":     ["God's presence", "community", "never forsaken", "Emmanuel"],
    "joyful":     ["praise", "thanksgiving", "rejoice", "celebration"],
    "angry":      ["forgiveness", "patience", "slow to anger", "grace"],
    "doubtful":   ["faith", "seeking God", "assurance of salvation", "trust"],
    "grateful":   ["thanksgiving", "praise", "God's faithfulness", "blessings"],
    "hopeless":   ["hope in Christ", "resurrection", "new life", "endurance"],
    "fearful":    ["courage", "God is with you", "perfect love casts out fear"],
    "overwhelmed":["rest", "burden", "come to me all who are weary", "strength"],
}

# ─────────────────────────────────────────────
# SCRIPTURE KNOWLEDGE BASE (seed data)
# Production: load from Bible API or local JSON file
# ─────────────────────────────────────────────

SCRIPTURE_KB = [
    {
        "reference": "Philippians 4:6-7", "version": "NIV",
        "text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
        "tags": ["anxious", "peace", "prayer", "trust in God"]
    },
    {
        "reference": "Isaiah 41:10", "version": "ESV",
        "text": "Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you, I will uphold you with my righteous right hand.",
        "tags": ["fearful", "courage", "God is with you", "strength"]
    },
    {
        "reference": "Psalm 34:18", "version": "NIV",
        "text": "The LORD is close to the brokenhearted and saves those who are crushed in spirit.",
        "tags": ["grieving", "comfort", "God heals the brokenhearted"]
    },
    {
        "reference": "Matthew 11:28-30", "version": "KJV",
        "text": "Come unto me, all ye that labour and are heavy laden, and I will give you rest. Take my yoke upon you, and learn of me; for I am meek and lowly in heart: and ye shall find rest unto your souls.",
        "tags": ["overwhelmed", "rest", "burden", "come to me all who are weary"]
    },
    {
        "reference": "Romans 8:28", "version": "NIV",
        "text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
        "tags": ["hopeless", "hope in Christ", "trust", "faith"]
    },
    {
        "reference": "Psalm 23:1-4", "version": "KJV",
        "text": "The LORD is my shepherd; I shall not want. He maketh me to lie down in green pastures: he leadeth me beside the still waters. He restoreth my soul... Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me.",
        "tags": ["fearful", "lonely", "God's presence", "comfort", "peace"]
    },
    {
        "reference": "1 Peter 5:7", "version": "ESV",
        "text": "Cast all your anxiety on him because he cares for you.",
        "tags": ["anxious", "casting cares", "trust in God"]
    },
    {
        "reference": "Nehemiah 8:10", "version": "NIV",
        "text": "Do not grieve, for the joy of the LORD is your strength.",
        "tags": ["grieving", "joyful", "strength", "hope"]
    },
    {
        "reference": "Psalm 46:1", "version": "ESV",
        "text": "God is our refuge and strength, a very present help in trouble.",
        "tags": ["fearful", "overwhelmed", "strength", "trust in God"]
    },
    {
        "reference": "Lamentations 3:22-23", "version": "NIV",
        "text": "Because of the LORD's great love we are not consumed, for his compassions never fail. They are new every morning; great is your faithfulness.",
        "tags": ["hopeless", "grateful", "God's faithfulness", "hope in Christ"]
    },
]

# ─────────────────────────────────────────────
# ANGAZA RAG ENGINE
# ─────────────────────────────────────────────

class AngazaRAGEngine:
    """
    Free-tier RAG pipeline:
    - Embeddings: sentence-transformers/all-MiniLM-L6-v2 (HuggingFace, free)
    - Vector Store: FAISS (local, free)
    - LLM: Groq (llama3-8b-8192, free tier ~14,400 req/day)
    """

    def __init__(self, groq_api_key: str):
        print("🕊️  Initializing Angaza RAG Engine...")

        # Load free HuggingFace embedding model
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Initialize Groq client (free LLM)
        self.llm = Groq(api_key=groq_api_key)
        self.llm_model = "llama3-8b-8192"   # Free tier

        # Build FAISS index
        self._build_vector_index()
        print("✅ Engine ready. Serving scripture with love.")

    def _build_vector_index(self):
        """Embed all scriptures into FAISS index."""
        texts = [f"{s['reference']}: {s['text']}" for s in SCRIPTURE_KB]
        embeddings = self.embedder.encode(texts, show_progress_bar=False)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype="float32"))
        self.scripture_texts = texts
        print(f"📖 Indexed {len(texts)} scriptures into FAISS.")

    def _detect_emotion(self, user_text: str) -> str:
        """
        Lightweight emotion detection using Groq LLM.
        Returns one of the keys in EMOTION_TOPICS.
        """
        emotion_list = list(EMOTION_TOPICS.keys())
        prompt = f"""You are an empathetic assistant for a church AI.
Classify the primary emotion in the following text into ONE word from this list:
{emotion_list}

User said: "{user_text}"

Respond with ONLY the single emotion word, nothing else."""

        response = self.llm.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.1
        )
        detected = response.choices[0].message.content.strip().lower()
        return detected if detected in EMOTION_TOPICS else "anxious"

    def retrieve_scripture(self, user_context: UserContext, query: str) -> ScriptureResult:
        """
        Main RAG function: Retrieves a Bible verse based on emotional state.

        Flow:
        1. Detect emotion from user query
        2. Enrich query with theological topics for that emotion
        3. Embed enriched query → FAISS similarity search
        4. Generate warm devotional note via Groq LLM
        5. Return structured ScriptureResult
        """

        # Step 1: Detect emotion (use provided or auto-detect)
        emotion = user_context.emotional_state or self._detect_emotion(query)
        topics = EMOTION_TOPICS.get(emotion, ["God's love"])

        # Step 2: Build enriched semantic query
        enriched_query = f"Bible verse about {', '.join(topics[:2])} for someone who feels {emotion}"
        print(f"🔍 Query: '{enriched_query}'")

        # Step 3: FAISS vector search
        query_vec = self.embedder.encode([enriched_query], show_progress_bar=False)
        distances, indices = self.index.search(np.array(query_vec, dtype="float32"), k=3)

        best_idx = indices[0][0]
        best_score = float(1 / (1 + distances[0][0]))  # Convert L2 to similarity score
        scripture_data = SCRIPTURE_KB[best_idx]

        # Step 4: Generate devotional note via Groq
        lang_instruction = "Respond in Swahili." if user_context.language == "sw" else "Respond in English."
        devotional_prompt = f"""You are Angaza, a warm and spiritually grounded church AI assistant.
A person shared they feel {emotion}. You've selected this Bible verse for them:

{scripture_data['reference']}: "{scripture_data['text']}"

Write a SHORT (2-3 sentences), warm, and encouraging devotional reflection on this verse
tailored to someone feeling {emotion}. Be gentle, personal, and faith-affirming.
Do NOT give pastoral counseling. {lang_instruction}"""

        devotional_response = self.llm.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": devotional_prompt}],
            max_tokens=150,
            temperature=0.7
        )
        devotional_note = devotional_response.choices[0].message.content.strip()

        return ScriptureResult(
            reference=scripture_data["reference"],
            text=scripture_data["text"],
            version=scripture_data["version"],
            relevance_score=round(best_score, 3),
            devotional_note=devotional_note
        )

    def answer_question(self, question: str, language: str = "en") -> str:
        """
        General theological Q&A with safety guardrails.
        Uses RAG context + Groq LLM.
        """
        GUARDRAILS = [
            "abortion", "politics", "election", "party", "democrat", "republican",
            "which church is correct", "other religions are false"
        ]

        # Safety check
        q_lower = question.lower()
        if any(term in q_lower for term in GUARDRAILS):
            return ("That's a meaningful question that deserves thoughtful pastoral guidance. "
                    "I encourage you to consult your Pastor for this one. 🙏")

        lang_instruction = "Answer in Swahili." if language == "sw" else "Answer in English."
        system_prompt = """You are Angaza, a warm, knowledgeable, and spiritually grounded church AI.
You help congregants understand scripture and church matters.
Rules:
- Be warm, reverent, and encouraging
- Ground answers in scripture where possible
- For complex counseling needs, direct users to their Pastor
- Never engage in political debates
- Keep answers concise (under 120 words)"""

        response = self.llm.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{question}\n\n{lang_instruction}"}
            ],
            max_tokens=200,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────
# DEMO USAGE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize engine (set GROQ_API_KEY in environment)
    engine = AngazaRAGEngine(groq_api_key=os.environ.get("GROQ_API_KEY", "your-key-here"))

    # Example 1: Emotion-based scripture
    ctx = UserContext(user_id="user_001", emotional_state="anxious", language="en")
    result = engine.retrieve_scripture(ctx, query="I feel so anxious about my job interview tomorrow")

    print("\n" + "="*60)
    print(f"📖 {result.reference} ({result.version})")
    print(f"   \"{result.text}\"")
    print(f"\n💬 Devotional: {result.devotional_note}")
    print(f"   Relevance: {result.relevance_score}")

    # Example 2: Swahili query
    ctx_sw = UserContext(user_id="user_002", emotional_state="", language="sw")
    result_sw = engine.retrieve_scripture(ctx_sw, query="Nahisi huzuni sana leo")  # "I feel very sad today"
    print("\n" + "="*60)
    print(f"📖 {result_sw.reference} — Kiswahili")
    print(f"💬 {result_sw.devotional_note}")
