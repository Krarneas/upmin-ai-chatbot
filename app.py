import html
import os
import re

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
    :root {
        --up-maroon: #7b1113;
        --up-maroon-2: #a32020;
        --up-gold: #f4c95d;
        --ink: #1c1716;
        --muted: #776b68;
        --paper: #fffaf1;
        --panel: rgba(255, 250, 241, 0.86);
        --line: rgba(123, 17, 19, 0.14);
        --shadow: 0 24px 70px rgba(82, 35, 25, 0.16);
    }

    .stApp {
        background:
            radial-gradient(circle at 14% 10%, rgba(244, 201, 93, 0.34), transparent 30%),
            radial-gradient(circle at 88% 6%, rgba(123, 17, 19, 0.18), transparent 34%),
            linear-gradient(135deg, #fff8eb 0%, #f6eee1 48%, #efe2d1 100%);
        color: var(--ink);
        font-family: "Aptos", "Segoe UI", sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 980px;
        padding-top: 42px;
        padding-bottom: 112px;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(123, 17, 19, 0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(123, 17, 19, 0.035) 1px, transparent 1px);
        background-size: 34px 34px;
        mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.75), transparent 72%);
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(165deg, rgba(123, 17, 19, 0.98), rgba(92, 14, 18, 0.96)),
            radial-gradient(circle at top left, rgba(244, 201, 93, 0.22), transparent 36%);
        border-right: 1px solid rgba(255, 255, 255, 0.18);
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
        color: rgba(255, 255, 255, 0.78) !important;
        line-height: 1.6;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255,255,255,0.12);
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 999px;
        width: 100%;
        padding: 0.68rem 1rem;
        font-size: 0.9rem;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255,255,255,0.24);
        border-color: rgba(244, 201, 93, 0.72);
        transform: translateY(-1px);
    }

    .sidebar-kicker {
        color: var(--up-gold) !important;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
    }

    .sidebar-title {
        font-size: 1.55rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: 1.1rem;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 22px;
        padding: 16px;
        margin: 18px 0;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.11);
    }

    .sidebar-card strong {
        color: #ffffff !important;
        display: block;
        margin-bottom: 0.4rem;
    }

    .sidebar-card ul {
        margin-bottom: 0;
        padding-left: 1.1rem;
    }

    .header-banner {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(135deg, rgba(123, 17, 19, 0.96), rgba(163, 32, 32, 0.9)),
            radial-gradient(circle at 82% 18%, rgba(244, 201, 93, 0.42), transparent 24%);
        color: #ffffff;
        padding: 34px 36px;
        border: 1px solid rgba(255, 255, 255, 0.42);
        border-radius: 30px;
        margin-bottom: 26px;
        box-shadow: var(--shadow);
        isolation: isolate;
    }
    .header-banner::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -82px;
        top: -86px;
        background: conic-gradient(from 120deg, rgba(244, 201, 93, 0.76), rgba(255, 255, 255, 0.16), transparent);
        border-radius: 999px;
        opacity: 0.72;
        z-index: -1;
    }
    .eyebrow {
        color: var(--up-gold);
        font-size: 0.78rem;
        font-weight: 850;
        letter-spacing: 0.15em;
        margin-bottom: 0.65rem;
        text-transform: uppercase;
    }
    .header-banner h1 {
        margin: 0 0 10px 0;
        max-width: 620px;
        font-size: clamp(2.05rem, 6vw, 4.15rem);
        font-weight: 900;
        letter-spacing: -0.065em;
        line-height: 0.95;
        color: #ffffff;
    }
    .header-banner p {
        margin: 0;
        max-width: 590px;
        font-size: 1rem;
        line-height: 1.65;
        color: rgba(255, 255, 255, 0.84);
    }
    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 22px;
    }
    .hero-pill {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.24);
        border-radius: 999px;
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.8rem;
        font-weight: 700;
        padding: 8px 12px;
    }

    .chat-area {
        display: flex;
        flex-direction: column;
        gap: 16px;
        margin: 10px 0 24px;
        padding: 24px;
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 28px;
        box-shadow: 0 18px 44px rgba(99, 53, 31, 0.08);
        backdrop-filter: blur(18px);
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
        max-width: min(720px, 78vw);
        padding: 14px 17px;
        border-radius: 20px;
        font-size: 0.96rem;
        line-height: 1.65;
        text-align: left;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: normal;
        display: block;
    }
    .bubble-user {
        background: linear-gradient(135deg, var(--up-maroon), var(--up-maroon-2));
        color: #ffffff;
        border-radius: 22px 22px 6px 22px;
        box-shadow: 0 14px 28px rgba(123, 17, 19, 0.22);
    }
    .bubble-assistant {
        background-color: rgba(255, 255, 255, 0.92);
        color: var(--ink);
        border-radius: 22px 22px 22px 6px;
        border: 1px solid rgba(123, 17, 19, 0.1);
        box-shadow: 0 12px 30px rgba(70, 43, 30, 0.08);
    }
    .bubble strong {
        font-weight: 850;
    }
    .bubble em {
        font-style: italic;
    }

    .sender-label {
        font-size: 0.73rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
        color: var(--muted);
        text-transform: uppercase;
    }
    .sender-label-user {
        text-align: right;
        color: var(--up-maroon);
    }

    .suggest-panel {
        background: rgba(255, 250, 241, 0.72);
        border: 1px solid var(--line);
        border-radius: 26px;
        box-shadow: 0 18px 44px rgba(99, 53, 31, 0.08);
        margin-top: 10px;
        padding: 18px;
        backdrop-filter: blur(18px);
    }
    .suggest-title {
        color: var(--muted);
        font-size: 0.8rem;
        font-weight: 850;
        letter-spacing: 0.1em;
        margin: 0 0 12px;
        text-transform: uppercase;
    }
    div[data-testid="column"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.78);
        color: var(--up-maroon);
        border: 1px solid rgba(123, 17, 19, 0.14);
        border-radius: 18px;
        box-shadow: 0 10px 22px rgba(78, 45, 24, 0.06);
        font-size: 0.88rem;
        font-weight: 700;
        padding: 0.86rem 1rem;
        width: 100%;
        text-align: left;
        cursor: pointer;
        transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }
    div[data-testid="column"] .stButton > button:hover {
        background-color: #ffffff;
        border-color: rgba(123, 17, 19, 0.42);
        box-shadow: 0 14px 28px rgba(123, 17, 19, 0.12);
        transform: translateY(-2px);
    }

    .stChatInput {
        background: transparent;
    }
    .stChatInput textarea {
        background-color: #ffffff !important;
        color: var(--ink) !important;
        border: 1px solid rgba(123, 17, 19, 0.22) !important;
        border-radius: 999px !important;
        box-shadow: 0 12px 32px rgba(77, 45, 25, 0.12) !important;
        min-height: 54px !important;
    }
    .stChatInput textarea:focus {
        border-color: rgba(123, 17, 19, 0.55) !important;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-top: 24px;
            padding-left: 18px;
            padding-right: 18px;
        }
        .header-banner {
            border-radius: 24px;
            padding: 28px 24px;
        }
        .chat-area {
            border-radius: 22px;
            padding: 16px;
        }
        .bubble {
            max-width: 88vw;
        }
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
    st.markdown(
        """
<div class="sidebar-kicker">UP Mindanao</div>
<div class="sidebar-title">AI Assistant</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(
        """
<div class="sidebar-card">
    <strong>About</strong>
    <p>This assistant answers questions about UP Mindanao programs, admission, student services, and campus life.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-card">
    <strong>Knowledge Sources</strong>
    <ul>
        <li>Core university facts</li>
        <li>UP Mindanao website</li>
        <li>Uploaded documents</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

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
    <div class="eyebrow">Campus answers, faster</div>
    <h1>UP Mindanao AI Assistant</h1>
    <p>Ask about programs, admission, tuition, services, and student life with answers grounded in the local knowledge base.</p>
    <div class="hero-meta">
        <span class="hero-pill">Admissions</span>
        <span class="hero-pill">Academics</span>
        <span class="hero-pill">Student Services</span>
    </div>
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
    escaped = html.escape(content)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__(.+?)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped.replace("\n", "<br>")


typed = st.chat_input("Ask about UP Mindanao...")
if typed:
    st.session_state.pending_prompt = typed

if not st.session_state.messages and not st.session_state.active_prompt:
    st.markdown(
        '<div class="suggest-panel"><p class="suggest-title">Try asking</p></div>',
        unsafe_allow_html=True,
    )
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
