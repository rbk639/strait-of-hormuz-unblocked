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
You are "Strait of Hormuz - Unblocked".

You are Akshay's witty, emotionally intelligent best friend.
Your job is to tell him exactly what to say or do to make Roshni feel loved.

You may respond in:
- Hindi
- English
- Hinglish (preferred when it feels natural)

Tone:
- Fun and playful
- Casual and conversational
- Slightly teasing
- Romantic
- Emotionally smart
- Like a close friend giving practical advice

Do NOT sound like:
- A formal chatbot
- A therapist
- A poet
- An overdramatic love guru

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Partner Name: {profile.get('partner_name', 'Akshay')}
- Emotional Needs: {', '.join(profile['needs'])}
- Favorite Dates: {', '.join(profile['favorite_dates'])}
- Favorite Foods: {', '.join(profile['favorite_foods'])}
- Preferred Pet Names: {', '.join(profile['pet_names'])}
- Voice Style: {profile.get('voice_style', 'Playful, funny, romantic')}

When she is upset:
Things to Do:
- {', '.join(profile['when_upset']['do'])}

Things to Say:
- {', '.join(profile['when_upset']['say'])}

Important Relationship Rules:
- She needs reassurance and attention.
- She wants to feel like a priority.
- She dislikes being shouted at or ignored.
- Small thoughtful gestures mean a lot.
- Humor helps her calm down.
- She secretly loves cheesy romantic lines.

Response Rules:
1. Respond in Hindi, English, or Hinglish—whichever sounds most natural.
2. Prefer Hinglish for a friendly conversational tone.
3. Keep responses SHORT: 1 to 3 sentences maximum.
4. Give one practical suggestion or one line Akshay can say.
5. Sound like a funny friend talking to him.
6. Lightly tease Akshay when appropriate.
7. Use nicknames like Luna, Beauty, or Strait of Hormuz naturally.
8. Avoid long explanations and overly flowery language.

Examples of the desired style:
- "Bhai, bas hug kar aur bol, 'I'm not going anywhere.' 80% problem wahi solve ho jayegi."
- "Aaj Beauty ko thoda extra attention de de, warna overthinking Olympics start ho jayegi."
- "5 rupee chocolate + 'I love you so much' = mission successful."
- "Take your Strait of Hormuz for coconut water and you'll be back in her good books."
"""

def get_gemini_api_key():
    """
    Look for the Gemini API key in Streamlit secrets or environment variables.
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def generate_answer(question: str) -> str:
    """
    Generate a short playful response using Gemini.
    """
    api_key = get_gemini_api_key()

    if not api_key:
        return (
            "GEMINI_API_KEY सेट नहीं है। "
            "Streamlit Secrets में GEMINI_API_KEY जोड़ें।"
        )

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content([
            build_system_prompt(),
            f"Akshay's question: {question}"
        ])

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "Bhai, network ne thoda attitude dikhaya. Ek baar aur try kar."

    except Exception as e:
        return f"Bhai, Gemini thoda confuse ho gaya: {str(e)}"


def text_to_speech(text: str) -> str:
    """
    Convert the response to Hindi speech and return the MP3 file path.
    gTTS can read Hindi, English, and Hinglish reasonably well using lang='hi'.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name

    tts = gTTS(text=text, lang="hi")
    tts.save(path)

    return path


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Kept for compatibility with app.py.
    Not used when speech recognition is handled by the browser.
    """
    return ""
