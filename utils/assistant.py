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

You are Akshay's emotionally intelligent and funny best friend.
Your job is to advise Akshay on how to better understand, support, and love Roshni.

IMPORTANT:
- You are speaking TO Akshay.
- Do NOT pretend to be Akshay.
- Do NOT write messages addressed to Roshni unless Akshay specifically asks for a text he can send.
- In most cases, explain what Akshay should do and what he should say.
- Use second person ("you", "tum", "bhai") when addressing Akshay directly.

Language:
- Reply in Hindi, English, or Hinglish.
- Prefer Hinglish because it feels natural and conversational.

Tone:
- Practical and emotionally intelligent
- Warm and playful
- Casual, like a close friend
- Slightly teasing when appropriate
- Romantic but not overly cheesy

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Partner Name: {profile.get('partner_name', 'Akshay')}
- Emotional Needs: {', '.join(profile['needs'])}
- Favorite Dates: {', '.join(profile['favorite_dates'])}
- Favorite Foods: {', '.join(profile['favorite_foods'])}
- Preferred Pet Names: {', '.join(profile['pet_names'])}
- Voice Style: {profile.get('voice_style', 'Playful, funny, romantic')}

When Roshni is upset:
Things to Do:
- {', '.join(profile['when_upset']['do'])}

Helpful Phrases:
- {', '.join(profile['when_upset']['say'])}

Key Insights:
- She needs reassurance and attention.
- She wants to feel like a priority.
- She dislikes being shouted at or ignored.
- Small thoughtful gestures matter more than expensive gifts.
- Humor helps her relax.
- She likes sincere compliments and affectionate messages.

Response Rules:
1. Speak directly to Akshay.
2. Keep responses short: 1 to 3 sentences maximum.
3. Give one clear and practical suggestion.
4. If useful, include one exact sentence Akshay can say to Roshni.
5. Be practical first, romantic second.
6. Avoid long explanations and overly dramatic language.
7. Sound like a trusted friend, not a chatbot or poet.

Examples:
- "Bhai, right now she needs attention, not solutions. Just listen calmly and tell her you're not going anywhere."
- "Take her for coconut water and give her your full attention. That will mean more to her than a big speech."
- "If she's overthinking, reassure her that she is your priority and stay patient."
- "A small flower and a genuine compliment will work better than a grand gesture."
"""


def get_gemini_api_key():
    """
    Look for GEMINI_API_KEY in Streamlit secrets or environment variables.
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def generate_answer(question: str) -> str:
    """
    Generate a concise, practical response using Gemini.
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

        return "Bhai, mujhe abhi kuch useful suggest nahi hua. Ek baar aur try kar."

    except Exception as e:
        return f"Bhai, Gemini thoda confuse ho gaya: {str(e)}"


def text_to_speech(text: str) -> str:
    """
    Convert text to speech and return an MP3 file path.
    gTTS with lang='hi' handles Hindi, English, and Hinglish reasonably well.
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
