import html
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from knowledge import get_system_prompt


st.set_page_config(
    page_title="UP Mindanao AI Assistant",
    page_icon="assets/upmin_logo.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown(
    """
<style>
    .stApp {
        background-color: #f0ede8;
        font-family: 'Segoe UI', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background-color: #7b1113;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25) !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255,255,255,0.15);
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 8px;
        width: 100%;
        padding: 8px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255,255,255,0.25);
    }

    .header-banner {
        background: linear-gradient(135deg, #7b1113, #a31f21);
        color: white;
        padding: 22px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .header-banner h1 {
        margin: 0 0 4px 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    .header-banner p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.85;
        color: white;
    }

    .chat-area {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 24px;
    }

    .msg-row-user {
        display: flex;
        justify-content: flex-end;
    }
    .msg-row-assistant {
        display: flex;
        justify-content: flex-start;
    }

    .bubble {
        max-width: 72%;
        padding: 12px 16px;
        border-radius: 16px;
        font-size: 0.92rem;
        line-height: 1.6;
        text-align: left;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: normal;
        display: block;
    }
    .bubble-user {
        background-color: #7b1113;
        color: #ffffff;
        border-radius: 16px 16px 4px 16px;
    }
    .bubble-assistant {
        background-color: #ffffff;
        color: #1a1a1a;
        border-radius: 16px 16px 16px 4px;
        border: 1px solid #ddd;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }

    .sender-label {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 4px;
        color: #888;
    }
    .sender-label-user {
        text-align: right;
        color: #7b1113;
    }

    .suggest-title {
        font-size: 0.82rem;
        color: #888;
        margin-bottom: 8px;
        font-weight: 500;
    }
    div[data-testid="column"] .stButton > button {
        background-color: #ffffff;
        color: #7b1113;
        border: 1px solid #c8a0a0;
        border-radius: 20px;
        font-size: 0.82rem;
        padding: 6px 12px;
        width: 100%;
        text-align: left;
        cursor: pointer;
        transition: background 0.2s;
    }
    div[data-testid="column"] .stButton > button:hover {
        background-color: #f7eded;
        border-color: #7b1113;
    }

    .stChatInput {
        border-top: 1px solid #ddd;
        padding-top: 12px;
    }
    .stChatInput textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
        border-radius: 24px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

if "system_prompt" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        st.session_state.system_prompt = get_system_prompt()


with st.sidebar:
    st.markdown("## UP Mindanao")
    st.markdown("### AI Assistant")
    st.markdown("---")

    st.markdown("**About**")
    st.markdown(
        "This assistant answers questions about UP Mindanao - "
        "programs, admission, student services, and more."
    )

    st.markdown("---")
    st.markdown("**Knowledge Sources**")
    st.markdown("- Core university facts")
    st.markdown("- UP Mindanao website")
    st.markdown("- Uploaded documents")

    st.markdown("---")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.active_prompt = None
        st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit + OpenAI")
    st.caption("UP Mindanao, Mintal, Davao City")


st.markdown(
    """
<div class="header-banner">
    <h1>UP Mindanao AI Assistant</h1>
    <p>Ask me anything about programs, admission, and student life.</p>
</div>
""",
    unsafe_allow_html=True,
)


SUGGESTED = [
    "What courses does UP Mindanao offer?",
    "How do I apply for admission?",
    "Is there a dormitory available?",
    "What is the academic calendar?",
    "What is the tuition fee structure?",
    "Where is UP Mindanao located?",
]


def render_bubble(content: str) -> str:
    return html.escape(content).replace("\n", "<br>")


typed = st.chat_input("Ask about UP Mindanao...")
if typed:
    st.session_state.pending_prompt = typed

if not st.session_state.messages and not st.session_state.active_prompt:
    st.markdown('<p class="suggest-title">Try asking:</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    for i, q in enumerate(SUGGESTED):
        with col1 if i % 2 == 0 else col2:
            if st.button(q, key=f"sq_{i}"):
                st.session_state.pending_prompt = q
                st.rerun()

if st.session_state.pending_prompt and not st.session_state.active_prompt:
    st.session_state.messages.append(
        {"role": "user", "content": st.session_state.pending_prompt}
    )
    st.session_state.active_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


if st.session_state.messages:
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
<div class="msg-row-user">
    <div>
        <div class="sender-label sender-label-user">You</div>
        <div class="bubble bubble-user">{render_bubble(msg["content"])}</div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
<div class="msg-row-assistant">
    <div>
        <div class="sender-label">Assistant</div>
        <div class="bubble bubble-assistant">{render_bubble(msg["content"])}</div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.active_prompt:
    api_messages = [{"role": "system", "content": st.session_state.system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-5.4-mini",
                messages=api_messages,
                temperature=0.7,
                max_completion_tokens=800,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = (
                f"Sorry, I encountered an error: {str(e)}\n\n"
                "Please check your API key or try again."
            )

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.active_prompt = None
    st.rerun()
