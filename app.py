from datetime import datetime
import streamlit as st
import requests

# ---------------------------
# Configuration
# ---------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

st.set_page_config(
    page_title="Local AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Sidebar
# ---------------------------

with st.sidebar:
    st.header("📌 About")
    st.write("**Local AI Assistant**")
    st.write("🤖 Model: TinyLlama")
    st.write("⚙️ Backend: Ollama")
    st.write("🌐 Framework: Streamlit")
    st.write("---")
    st.write("Created during AI Internship")

# ---------------------------
# Main Page
# ---------------------------

st.title("🤖 Local AI Assistant")
st.caption("Powered by TinyLlama using Ollama")

# ---------------------------
# Session State
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# User Input
# ---------------------------

prompt = st.text_input(
    "Ask me anything...",
    placeholder="Type your question here..."
)

col1, col2 = st.columns(2)

with col1:
    ask = st.button("🚀 Ask", use_container_width=True)

with col2:
    clear = st.button("🗑️ Clear Chat", use_container_width=True)

# ---------------------------
# Clear Chat
# ---------------------------

if clear:
    st.session_state.messages = []
    st.rerun()

# ---------------------------
# Generate Response
# ---------------------------

if ask and prompt:

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    with st.spinner("🤖 TinyLlama is thinking..."):

        try:

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=60
            )

            answer = response.json()["response"]

            st.success("✅ Response generated successfully!")

        except Exception:

            answer = "❌ Ollama server is not running or could not generate a response."

    current_time = datetime.now().strftime("%I:%M %p")

    st.session_state.messages.append(
        ("You", prompt, current_time)
    )

    st.session_state.messages.append(
        ("TinyLlama", answer, current_time)
    )

# ---------------------------
# Chat History
# ---------------------------

st.divider()

for sender, message, time in st.session_state.messages:

    if sender == "You":

        with st.chat_message("user"):
            st.caption(time)
            st.write(message)

    else:

        with st.chat_message("assistant"):
            st.caption(time)
            st.write(message)