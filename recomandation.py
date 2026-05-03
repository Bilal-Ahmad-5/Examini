import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
from typing import List, Dict
from dotenv import load_dotenv
import sqlite3
import json
from datetime import datetime

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = str(os.getenv("GOOGLE_API_KEY"))


# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RecommendOS · AI Advisor",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── APPLE-STYLE PREMIUM CSS ────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:           #f5f5f7;
    --surface:      #ffffff;
    --surface-2:    #fafafa;
    --border:       rgba(0,0,0,0.08);
    --border-hover: rgba(0,0,0,0.18);
    --text-primary: #1d1d1f;
    --text-second:  #6e6e73;
    --text-third:   #a1a1a6;
    --accent:       #0071e3;
    --accent-soft:  rgba(0,113,227,0.08);
    --success:      #34c759;
    --success-soft: rgba(52,199,89,0.10);
    --danger:       #ff3b30;
    --danger-soft:  rgba(255,59,48,0.10);
    --radius-sm:    10px;
    --radius:       16px;
    --radius-lg:    24px;
    --shadow-xs:    0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-sm:    0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.04);
    --shadow:       0 8px 32px rgba(0,0,0,0.09), 0 2px 8px rgba(0,0,0,0.05);
    --font-sans:    'Figtree', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-display: 'Playfair Display', Georgia, serif;
    --transition:   all 0.22s cubic-bezier(0.4,0,0.2,1);
}

[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--font-sans) !important;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="block-container"] {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1100px;
    margin: 0 auto;
}

/* ── TYPOGRAPHY ── */
h1,h2,h3,h4 { font-family: var(--font-sans) !important; color: var(--text-primary) !important; }
.stMarkdown p { font-family: var(--font-sans) !important; color: var(--text-second) !important;
    font-size: 0.93rem !important; line-height: 1.65 !important; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3.5rem 2rem 3rem;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 1.3rem;
}
.hero-eyebrow::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: pdot 2s infinite;
}
@keyframes pdot {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:.4; transform:scale(.75); }
}
.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(2.1rem,4.5vw,3.3rem) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    line-height: 1.15 !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 0.9rem !important;
    border: none !important;
}
.hero-subtitle {
    font-size: 1rem !important;
    color: var(--text-second) !important;
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-third);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── PANEL ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-sm);
    height: 100%;
}

/* ── INPUTS ── */
.stTextInput label, .stTextArea label {
    font-family: var(--font-sans) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}
.stTextInput input, .stTextArea textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-size: 0.93rem !important;
    font-family: var(--font-sans) !important;
    padding: 0.68rem 1rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-xs) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft), var(--shadow-xs) !important;
    background: var(--surface) !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: var(--text-third) !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.62rem 1.3rem !important;
    transition: var(--transition) !important;
    cursor: pointer !important;
}

/* Primary submit button */
div[data-testid="column"]:first-child .stButton > button[kind="primary"],
.primary-btn .stButton > button {
    background: var(--text-primary) !important;
    color: #fff !important;
    width: 100% !important;
    padding: 0.8rem 2rem !important;
    font-size: 0.93rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.16) !important;
}

/* Full-width black button */
[data-testid="stFormSubmitButton"] > button {
    background: var(--text-primary) !important;
    color: #fff !important;
    width: 100% !important;
    padding: 0.8rem !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.16) !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: #000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.28) !important;
}

/* Ask button — accent blue */
.ask-btn .stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    width: 100% !important;
    padding: 0.8rem !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 2px 8px rgba(0,113,227,0.22) !important;
}
.ask-btn .stButton > button:hover {
    background: #005bbf !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(0,113,227,0.35) !important;
}

/* Clear / danger button */
.clear-btn .stButton > button {
    background: var(--danger-soft) !important;
    color: var(--danger) !important;
    border: 1px solid rgba(255,59,48,0.25) !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1rem !important;
}
.clear-btn .stButton > button:hover {
    background: rgba(255,59,48,0.16) !important;
}

/* Chat history item buttons */
.hist-btn .stButton > button {
    background: transparent !important;
    color: var(--text-second) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 0.81rem !important;
    padding: 0.55rem 0.9rem !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.hist-btn .stButton > button:hover {
    background: var(--surface-2) !important;
    border-color: var(--border-hover) !important;
    color: var(--text-primary) !important;
}

/* ── RESPONSE CARD ── */
.response-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-top: 1.2rem;
    border-left: 3px solid var(--accent);
    font-size: 0.93rem;
    color: var(--text-second);
    line-height: 1.75;
}
.response-label {
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
}

/* ── CHAT HISTORY ITEM ── */
.chat-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    transition: var(--transition);
}
.chat-item:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-xs);
}
.chat-user {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 5px;
}
.chat-user::before { content:'↑'; font-size:0.7rem; }
.chat-bot {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-third);
    margin: 0.5rem 0 0.2rem;
    display: flex;
    align-items: center;
    gap: 5px;
}
.chat-bot::before { content:'↓'; font-size:0.7rem; }
.chat-text {
    font-size: 0.83rem;
    color: var(--text-second);
    line-height: 1.55;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.chat-full-text {
    font-size: 0.83rem;
    color: var(--text-second);
    line-height: 1.55;
}

/* ── STUDENT BADGE ── */
.student-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}

/* ── ALERTS ── */
.stSuccess {
    background: var(--success-soft) !important;
    border: 1px solid rgba(52,199,89,0.28) !important;
    border-radius: var(--radius-sm) !important;
}
.stError {
    background: var(--danger-soft) !important;
    border: 1px solid rgba(255,59,48,0.25) !important;
    border-radius: var(--radius-sm) !important;
}
.stWarning {
    background: rgba(255,159,10,0.1) !important;
    border: 1px solid rgba(255,159,10,0.28) !important;
    border-radius: var(--radius-sm) !important;
}
.stInfo {
    background: var(--accent-soft) !important;
    border: 1px solid rgba(0,113,227,0.2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--accent) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 100px; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
}
.empty-icon { font-size: 2.2rem; margin-bottom: 0.8rem; opacity: 0.2; }
.empty-title { font-size: 0.9rem; font-weight: 600; color: var(--text-second); margin-bottom: 0.3rem; }
.empty-sub { font-size: 0.8rem; color: var(--text-third); }

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    font-size: 0.76rem;
    color: var(--text-third);
    letter-spacing: 0.02em;
}

/* Column border override */
[data-testid="column"] { border: none !important; }
</style>
""", unsafe_allow_html=True)


# ─── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by Gemini AI</div>
    <h1 class="hero-title">Advice that knows<br>your student.</h1>
    <p class="hero-subtitle">
        Enter a student's name to pull their exam history and get
        personalized AI-driven recommendations instantly.
    </p>
</div>
""", unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────────────────
def get_data_by_name(student):
    conn = sqlite3.connect('exam_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''SELECT * FROM attempts WHERE student_name = ?''', (student,))
    data = c.fetchall()
    conn.close()
    return data


def init_chat_db():
    conn = sqlite3.connect('Chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    bilalgpt TEXT
                )''')
    # Safe column migration
    c.execute("PRAGMA table_info(chats);")
    columns = [col[1] for col in c.fetchall()]
    if 'bilalgpt' not in columns:
        c.execute('ALTER TABLE chats ADD COLUMN bilalgpt TEXT;')
    conn.commit()
    return conn, c


def get_chat_history(c):
    c.execute("SELECT * FROM chats ORDER BY id DESC")
    return c.fetchall()


# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if 'selected_chat' not in st.session_state:
    st.session_state.selected_chat = None
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'last_query' not in st.session_state:
    st.session_state.last_query = None


# ─── INIT DB ────────────────────────────────────────────────────────────────────
conn, c = init_chat_db()


# ─── MAIN LAYOUT ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT — ASK PANEL
# ═══════════════════════════════════════════════════════════════════════════════
with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Student Advisor</div>', unsafe_allow_html=True)

    student = st.text_input(
        "Student Name",
        placeholder="e.g. Ali Khan, Sara Ahmed",
        key="student_input"
    )

    if student:
        student_data = get_data_by_name(student)
        attempt_count = len(student_data)
        color = "var(--success)" if attempt_count > 0 else "var(--text-third)"
        st.markdown(f"""
        <div class="student-badge">
            ◎ &nbsp;{student}
            <span style="font-weight:400;color:{color};margin-left:4px;">
                · {attempt_count} exam attempt{'s' if attempt_count != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        student_data = []

    query = st.text_input(
        "Your Question",
        placeholder="e.g. What topics should I focus on next?",
        key="query_input"
    )

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ask-btn">', unsafe_allow_html=True)
        submit = st.button("Get Recommendations →", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not student:
            st.warning("Please enter a student name first.")
        elif not query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing student data…"):
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
                    prompt = f"""You are a personalized Recommendation System for students.
These are the exam attempt stats of the student named "{student}": {student_data}

Based on this data, provide clear, actionable, and encouraging recommendations.
Also respond directly to the user's query below.

User query: {query}"""
                    response = llm.invoke(prompt)
                    c.execute(
                        'INSERT INTO chats (user, bilalgpt) VALUES (?, ?)',
                        (query, str(response.content))
                    )
                    conn.commit()
                    st.session_state.last_response = response.content
                    st.session_state.last_query = query

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # ── Response display ──
    if st.session_state.last_response:
        st.markdown(f"""
        <div class="response-card">
            <div class="response-label">◆ &nbsp;AI Recommendation</div>
            {st.session_state.last_response}
        </div>
        """, unsafe_allow_html=True)

    # ── Selected chat expanded view ──
    if st.session_state.selected_chat:
        sel = st.session_state.selected_chat
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:0.5rem;">
            <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
            color:var(--text-third);margin-bottom:0.6rem;">Conversation #{sel[0]}</div>
            <div class="chat-user">You asked</div>
            <div class="chat-full-text" style="margin-bottom:0.8rem;">{sel[1]}</div>
            <div class="chat-bot">AI response</div>
            <div class="chat-full-text">{sel[2]}</div>
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
            if st.button("✕  Close", use_container_width=False):
                st.session_state.selected_chat = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT — CHAT HISTORY PANEL
# ═══════════════════════════════════════════════════════════════════════════════
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    # Header row
    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown('<div class="section-label">Conversation History</div>', unsafe_allow_html=True)
    with h2:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("Clear All", use_container_width=True):
            c.execute("DELETE FROM chats")
            conn.commit()
            st.session_state.selected_chat = None
            st.session_state.last_response = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    chats = get_chat_history(c)

    if not chats:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◎</div>
            <div class="empty-title">No conversations yet</div>
            <div class="empty-sub">Submit a query to start building history.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for chat in chats:
            chat_id, user_msg, bot_msg = chat
            user_preview = (user_msg or "")[:60] + ("…" if len(user_msg or "") > 60 else "")
            bot_preview  = (bot_msg  or "")[:90] + ("…" if len(bot_msg  or "") > 90 else "")

            is_active = (
                st.session_state.selected_chat is not None and
                st.session_state.selected_chat[0] == chat_id
            )
            border_style = "border-color:var(--accent);" if is_active else ""

            st.markdown(f"""
            <div class="chat-item" style="{border_style}">
                <div class="chat-user">{user_preview}</div>
                <div class="chat-text">{bot_preview}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="hist-btn">', unsafe_allow_html=True)
                if st.button(f"View full · #{chat_id}", key=f"load_{chat_id}"):
                    st.session_state.selected_chat = chat
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    RecommendOS &nbsp;·&nbsp; Personalized Student Intelligence &nbsp;·&nbsp; Powered by Gemini AI
</div>
""", unsafe_allow_html=True)

conn.close()