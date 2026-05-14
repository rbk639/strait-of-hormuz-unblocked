import streamlit as st
from streamlit_mic_recorder import speech_to_text
from utils.assistant import generate_answer, text_to_speech

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Strait of Hormuz - Unblocked",
    page_icon="💜",
    layout="centered"
)

# --------------------------------------------------
# Luxury Black & Gold Styling
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #000000 0%, #0d061a 100%);
    color: #ffffff;
}

.main-card {
    background: rgba(20, 10, 35, 0.90);
    border: 1px solid rgba(212, 175, 55, 0.35);
    border-radius: 30px;
    padding: 2.5rem;
    box-shadow: 0 0 40px rgba(212, 175, 55, 0.15);
    margin-top: 2rem;
}

.title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 700;
    color: #D4AF37;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}

.subtitle {
    text-align: center;
    color: #d8cfa0;
    font-size: 1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.response {
    background: rgba(255, 255, 255, 0.04);
    border-left: 4px solid #D4AF37;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 2rem;
    line-height: 1.8;
    font-size: 1.05rem;
    color: #ffffff;
}

.stAudio {
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Main Card
# --------------------------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">Strait of Hormuz - Unblocked</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask anything about how to love Roshni better.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Voice Input (Microphone Only)
# --------------------------------------------------
question = speech_to_text(
    language="hi",
    start_prompt="🎙️ Tap to Ask",
    stop_prompt="⏹️ Stop Recording",
    use_container_width=True,
    just_once=True,
    key="voice_input"
)

# --------------------------------------------------
# Generate Answer Automatically
# --------------------------------------------------
if question:
    with st.spinner("Consulting the heart..."):
        answer = generate_answer(question)

    # Display text response
    st.markdown(
        f'<div class="response">{answer}</div>',
        unsafe_allow_html=True
    )

    # Convert answer to Hindi speech and autoplay
    try:
        audio_path = text_to_speech(answer)

        with open(audio_path, "rb") as audio_file:
            st.audio(
                audio_file.read(),
                format="audio/mp3",
                autoplay=True
            )
    except Exception as e:
        st.warning(f"Audio playback error: {e}")

# --------------------------------------------------
# Close Main Card
# --------------------------------------------------
st.markdown('</div>', unsafe_allow_html=True)
