import json
import os
import streamlit as st
import google.generativeai as genai


def load_profile():
    with open("data/roshni_profile.json", "r", encoding="utf-8") as f:
        return json.load(f)


def build_system_prompt():
    profile = load_profile()

    return f"""
You are "Strait of Hormuz - Unblocked", a luxurious AI relationship assistant.

Your purpose is to guide Akshay on how to love Roshni better.

Respond ONLY in Hindi.
Tone: playful, hilarious, romantic, cheesy, flirty, deeply reassuring.

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Partner Name: {profile['partner_name']}
- Emotional Needs: {', '.join(profile['needs'])}
- Favorite Dates: {', '.join(profile['favorite_dates'])}
- Favorite Foods: {', '.join(profile['favorite_foods'])}
- Preferred Pet Names: {', '.join(profile['pet_names'])}
- Voice Style: {profile['voice_style']}

When Roshni is upset:
Things to Do:
{', '.join(profile['when_upset']['do'])}

Things to Say:
{', '.join(profile['when_upset']['say'])}

Important Relationship Guidance:
- She needs reassurance and attention.
- She wants to feel like a priority.
- She dislikes being shouted at or ignored.
- Small thoughtful gestures mean a lot.
- Humor helps her calm down.
- She loves cheesy romantic lines.

Rules:
1. Respond in Hindi only.
2. Be warm, witty, romantic, and emotionally intelligent.
3. Use pet names such as Luna, Beauty, or Strait of Hormuz when appropriate.
4. Keep responses concise (3 to 8 sentences).
5. Give specific phrases Akshay can say.
6. Make responses playful and occasionally hilarious.
"""
    

def generate_answer(question: str) -> str:
    """
    Generate a Hindi response using Gemini.
    Reads GEMINI_API_KEY from Streamlit Secrets or environment variables.
    """
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "GEMINI_API_KEY सेट नहीं है। "
            "कृपया Streamlit Secrets में GEMINI_API_KEY जोड़ें।"
        )

    try:
        genai.configure(api_key=api_key)

        # Recommended fast, low-cost Gemini model
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content([
            build_system_prompt(),
            f"Akshay's question: {question}"
        ])

        return response.text.strip()

    except Exception as e:
        return f"एक त्रुटि हुई: {str(e)}"


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcription is not needed when using streamlit_mic_recorder.speech_to_text(),
    because that component already returns recognized text directly.
    This function is kept so app.py imports continue to work.
    """
    return ""
