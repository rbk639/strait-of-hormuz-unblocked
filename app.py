import streamlit as st
from utils.assistant import generate_answer, transcribe_audio

try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

st.set_page_config(
    page_title="Strait of Hormuz - Unblocked",
    page_icon="💜",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #000000 0%, #0d061a 100%);
    color: white;
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
    font-size: 2.6rem;
    font-weight: 700;
    color: #D4AF37;
    margin-bottom: 2rem;
}

.response {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #D4AF37;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 2rem;
    line-height: 1.8;
    font-size: 1.05rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown(
    '<div class="title">Strait of Hormuz - Unblocked</div>',
    unsafe_allow_html=True
)

if speech_to_text is None:
    st.error(
        "Microphone component not installed. "
        "Run: pip install streamlit-mic-recorder"
    )
else:
    # This component works better across mobile and desktop.
    question = speech_to_text(
        language="hi",
        start_prompt="🎙️ Tap to Ask",
        stop_prompt="⏹️ Stop Recording",
        use_container_width=True,
        just_once=True,
        key="voice_input"
    )

    # Automatically generate answer when speech is captured.
    if question:
        with st.spinner("Consulting the heart..."):
            answer = generate_answer(question)

        st.markdown(
            f'<div class="response">{answer}</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
