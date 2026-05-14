
import streamlit as st
from utils.assistant import generate_answer, transcribe_audio

try:
    from streamlit_mic_recorder import mic_recorder
except Exception:
    mic_recorder = None

PASSWORD = "151190"

st.set_page_config(page_title="Strait of Hormuz - Unblocked", page_icon="💜", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #000000 0%, #0d061a 100%); color: #ffffff; }
.main-card {
    background: rgba(20, 10, 35, 0.85);
    border: 1px solid rgba(212, 175, 55, 0.35);
    border-radius: 28px;
    padding: 2.5rem;
    box-shadow: 0 0 40px rgba(212, 175, 55, 0.12);
}
.title {
    text-align: center; font-size: 2.6rem; font-weight: 700;
    color: #D4AF37; margin-bottom: 0.5rem;
}
.response {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #D4AF37;
    border-radius: 16px;
    padding: 1.2rem;
    margin-top: 1.5rem;
    font-size: 1.05rem;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "transcribed_question" not in st.session_state:
    st.session_state.transcribed_question = ""

if not st.session_state.authenticated:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Strait of Hormuz - Unblocked</div>', unsafe_allow_html=True)
    password = st.text_input("Enter Password", type="password")
    if st.button("Unlock 💜", use_container_width=True):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="title">Strait of Hormuz - Unblocked</div>', unsafe_allow_html=True)

if mic_recorder:
    audio = mic_recorder(
        start_prompt="🎙️ Ask Your Question",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="webm",
        key="mic"
    )
    if audio and audio.get("bytes"):
        with st.spinner("Transcribing your question..."):
            text = transcribe_audio(audio["bytes"])
        if text:
            st.session_state.transcribed_question = text
        else:
            st.warning("Could not transcribe the audio. Please try again.")
else:
    st.error("Microphone package is not installed.")

question = st.text_area(
    "Your Question",
    value=st.session_state.transcribed_question,
    height=120,
    placeholder="रोशनी को अभी क्या बोलूँ?"
)

if st.button("Ask Strait of Hormuz 💜", use_container_width=True):
    if question.strip():
        with st.spinner("Consulting the heart..."):
            answer = generate_answer(question)
        st.markdown(f'<div class="response">{answer}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please record or type a question first.")

st.markdown('</div>', unsafe_allow_html=True)
