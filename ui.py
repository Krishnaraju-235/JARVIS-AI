import streamlit as st
import os
from app import get_response

# --- Theme Defaults ---
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="wide")

# --- Sidebar Settings ---
st.sidebar.title("⚙️ Settings")
context_only = st.sidebar.toggle("Use Context Only (No AI Knowledge)", value=False)

# --- CSS Styling ---
st.markdown("""
    <style>
    /* Entire background as GOLDEN */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFD700 !important;  /* golden */
        color: #000000;  /* black text for contrast */
    }

    /* Scrollbar customization */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #666;
    }

    /* Navy Blue Jarvis Title Banner */
    .title-container {
        background: #001f3f;  /* navy blue */
        padding: 30px 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    }

    /* File uploader and chat container - white with soft border */
    .file-uploader-section, .chat-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ccc;
        margin-bottom: 30px;
    }

    /* Chat messages */
    .stChatMessage.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }

    .stChatMessage.assistant {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }

    /* Uploaded files in sidebar */
    .uploaded-files-list {
        font-size: 0.9rem;
        color: #333;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Jarvis Title Banner ---
st.markdown("""
<div class="title-container">
    <h1>🤖 Jarvis AI</h1>
    <p>Talk to Jarvis or upload files for document-based Q&A</p>
</div>
""", unsafe_allow_html=True)

# --- File Upload Section ---
st.markdown('<div class="file-uploader-section">', unsafe_allow_html=True)
uploaded_files = st.file_uploader("📂 Upload PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- File Handling ---
if "file_paths" not in st.session_state:
    st.session_state.file_paths = []

if uploaded_files:
    st.session_state.file_paths = []
    os.makedirs("temp_files", exist_ok=True)
    for file in uploaded_files:
        temp_path = os.path.join("temp_files", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        st.session_state.file_paths.append(temp_path)

    st.sidebar.subheader("📄 Uploaded Files")
    for path in st.session_state.file_paths:
        st.sidebar.markdown(f"✅ {os.path.basename(path)}")

# --- Chat History State ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat Interface ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

user_input = st.chat_input("💬 Ask Jarvis something...")
if user_input:
    response = get_response(user_input, st.session_state.history, st.session_state.file_paths, context_only=context_only)
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": response})

# --- Show Chat History ---
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(f"🧑‍💻 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(f"🤖 **Jarvis:** {msg['content']}")

st.markdown('</div>', unsafe_allow_html=True)
