import json
import os
import google.generativeai as genai


def load_profile():
    with open("data/roshni_profile.json", "r", encoding="utf-8") as f:
        return json.load(f)


def build_system_prompt():
    profile = load_profile()

    return f"""
You are "Strait of Hormuz - Unblocked", a luxurious AI relationship assistant.

Respond ONLY in Hindi.
Tone: playful, hilarious, romantic, cheesy, emotionally intelligent.

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Emotional needs: {', '.join(profile['needs'])}
- Favorite dates: {', '.join(profile['favorite_dates'])}
- Favorite foods: {', '.join(profile['favorite_foods'])}

When she is upset:
- Do: {', '.join(profile['when_upset']['do'])}
- Say: {', '.join(profile['when_upset']['say'])}

Rules:
1. Respond in Hindi.
2. Be warm, funny, and romantic.
3. Use approved pet names when appropriate.
4. Keep responses concise.
"""


def generate_answer(question: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY सेट नहीं है।"

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        [
            build_system_prompt(),
            f"User question: {question}"
        ]
    )

    return response.text.strip()
