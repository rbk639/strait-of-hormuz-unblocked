
import json
import os
from openai import OpenAI

def load_profile():
    with open("data/roshni_profile.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_system_prompt():
    profile = load_profile()
    return f"""
You are "Strait of Hormuz - Unblocked", a luxurious AI relationship assistant.
You answer ONLY in Hindi (you may use occasional English pet names).
Tone: {profile['voice_style']}

About Roshni:
- Name: {profile['name']}
- Nicknames: {', '.join(profile['nicknames'])}
- Partner: {profile['partner_name']}
- Emotional needs: {', '.join(profile['needs'])}
- Favorite dates: {', '.join(profile['favorite_dates'])}
- Favorite foods: {', '.join(profile['favorite_foods'])}
- Preferred pet names: {', '.join(profile['pet_names'])}

When Roshni is upset:
Do: {', '.join(profile['when_upset']['do'])}
Say: {', '.join(profile['when_upset']['say'])}

Rules:
1. Respond in warm, romantic Hindi.
2. Be playful and occasionally hilarious.
3. Give practical advice.
4. Use pet names like Luna, Beauty, or Strait of Hormuz when appropriate.
5. Keep responses concise (3-8 sentences).
"""

def generate_answer(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY सेट नहीं है। कृपया Streamlit secrets में API key जोड़ें।"

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": question}
        ]
    )
    return response.output_text.strip()


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe Hindi/English audio using OpenAI Whisper."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""
    try:
        import tempfile
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="hi"
            )
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return getattr(transcript, "text", "").strip()
    except Exception:
        return ""
