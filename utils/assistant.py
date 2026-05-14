import json
import os
import tempfile

import streamlit as st
import google.generativeai as genai
from gtts import gTTS


def load_profile():
    with open("data/roshni_profile.json", "r", encoding="utf-8") as f:
        return json.load(f)


def build_system_prompt():
    profile = load_profile()

    return f"""
You are "Strait of Hormuz - Unblocked", a luxurious AI relationship assistant.

Respond ONLY in Hindi.
Tone: playful, hilarious, romantic, cheesy, flirty, deeply reassuring.

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Emotional Needs: {', '.join(profile['needs'])}
- Favorite Dates: {', '.join(profile['favorite_dates'])}
- Favorite Foods: {', '.join(profile['favorite_foods'])}

When she is upset:
- Do: {', '.join(profile['when_upset']['do'])}
- Say: {', '.join(profile['when_upset']['say'])}

Rules:
1. Respond only in Hindi.
2. Be warm, funny, romantic, and emotionally intelligent.
3. Use approved pet names when appropriate.
4. Keep responses concise.
"""


def get_gemini_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def generate_answer(question: str) -> str:
    api_key = get_gemini_api_key()

    if not api_key:
        return "GEMINI_API_KEY सेट नहीं है।"

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content([
        build_system_prompt(),
        f"Akshay's question: {question}"
    ])

    return response.text.strip()


def text_to_speech(text: str) -> str:
    """
    Convert Hindi text to speech and return the path to an MP3 file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name

    tts = gTTS(text=text, lang="hi")
    tts.save(path)

    return path


def transcribe_audio(audio_bytes: bytes) -> str:
    # Kept only for compatibility with app.py
    return ""
