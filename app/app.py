import streamlit as st
import datetime
import os

# --- Page Config ---
st.set_page_config(page_title="Model Context Protocol", layout="wide")
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 16px !important;
    }
    .chat-message {
        padding: 0.8rem;
        margin-bottom: 1rem;
        border-radius: 1rem;
    }
    .user {
        background-color: #f0f2f6;
        color: #000;
    }
    .assistant {
        background-color: #e8f5e9;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Settings ---
st.sidebar.title("⚙️ MCP Settings")
client_type = st.sidebar.radio("Select Client Type", ["SSE", "STDIO", "REST"], index=0)
save_chat = st.sidebar.checkbox("💾 Save Chat", value=True)

default_name = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
filename = st.sidebar.text_input("Filename", default_name if save_chat else "", disabled=not save_chat)

st.sidebar.markdown("---")
st.sidebar.title("🧰 Tools")
available_tools = [
    "TAT Score DB",
    "Credit Risk Analyzer",
    "Market Data Reader",
    "Custom CSV Tool"
]
selected_tools = st.sidebar.multiselect("Enable Tools", available_tools, default=["TAT Score DB"])

if st.sidebar.button("🗑️ Clear Chat"):
    if st.session_state.get("chat_history"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# --- Chat Session Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Main Title ---
st.title("💬 Model Context Protocol - Claude Style UI")

# --- Display Chat History ---
for role, msg in st.session_state.chat_history:
    class_name = "user" if role == "user" else "assistant"
    st.markdown(f'<div class="chat-message {class_name}"><strong>{role.capitalize()}:</strong><br>{msg}</div>', unsafe_allow_html=True)

# --- Chat Input ---
prompt = st.chat_input("Ask your financial or database question...")

if prompt:
    st.session_state.chat_history.append(("user", prompt))

    # Placeholder response (replace with backend call)
    tools_text = ", ".join(selected_tools) if selected_tools else "No tools selected"
    response = f"🧠 *Responding via **{client_type}** using tools:* `{tools_text}`\n\n> {prompt}"
    st.session_state.chat_history.append(("assistant", response))

    if save_chat and filename.strip():
        os.makedirs("chat_history", exist_ok=True)
        with open(os.path.join("chat_history", filename.strip()), "a", encoding="utf-8") as f:
            f.write(f"[User]: {prompt}\n[Assistant]: {response}\n\n")

    st.experimental_rerun()  # Auto-refresh chat after response
