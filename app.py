import streamlit as st
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

/* Large mobile-friendly button */
div.stButton > button {
    width: 100%;
    min-height: 80px;
    border-radius: 24px;
    border: 2px solid #D4AF37;
    background: linear-gradient(135deg, #1a1028 0%, #2d1b45 100%);
    color: #D4AF37;
    font-size: 1.4rem;
    font-weight: 700;
    box-shadow: 0 0 25px rgba(212, 175, 55, 0.15);
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
}

div.stButton > button:hover {
    border-color: #f4d76a;
}

div.stButton > button:active {
    transform: scale(0.98);
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
    '<div class="subtitle">Tap the microphone and ask in Hindi.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Mobile-Friendly Record Button
# --------------------------------------------------
if st.button("🎙️ Tap to Ask", use_container_width=True):
    # Ask for voice input using the browser's native speech recognition
    question = st.chat_input(
        "Speak your question using the microphone on your keyboard."
    )

    # If speech was captured, generate the response
    if question:
        with st.spinner("Consulting the heart..."):
            answer = generate_answer(question)

        # Show text response
        st.markdown(
            f'<div class="response">{answer}</div>',
            unsafe_allow_html=True
        )

        # Generate and autoplay Hindi audio
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

st.markdown('</div>', unsafe_allow_html=True)
