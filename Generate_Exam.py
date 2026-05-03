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

# Database Setup
conn = sqlite3.connect('exam_history.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                topic TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mcqs TEXT,
                short_questions TEXT,
                long_questions TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER,
                student_name TEXT,
                answers TEXT,
                score INTEGER,
                total INTEGER,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(exam_id) REFERENCES exams(id)
            )''')
conn.commit()


def get_data_by_name(student):
    conn = sqlite3.connect('exam_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''SELECT * FROM attempts WHERE student_name = ?''', (student,))
    data = c.fetchall()
    conn.close()
    return data


# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExamOS · AI Exam Generator",
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
    --accent-hover: #0077ed;
    --accent-soft:  rgba(0,113,227,0.08);
    --success:      #34c759;
    --success-soft: rgba(52,199,89,0.10);
    --danger:       #ff3b30;
    --danger-soft:  rgba(255,59,48,0.10);
    --warning:      #ff9f0a;
    --warning-soft: rgba(255,159,10,0.10);
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
    max-width: 860px;
    margin: 0 auto;
}

/* ── TYPOGRAPHY ── */
h1,h2,h3,h4,h5,h6 { font-family: var(--font-sans) !important; color: var(--text-primary) !important; }
.stMarkdown p, .stMarkdown li {
    font-family: var(--font-sans) !important;
    color: var(--text-second) !important;
    font-size: 0.93rem !important;
    line-height: 1.65 !important;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3.8rem 2rem 3.2rem;
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
    margin-bottom: 1.4rem;
}
.hero-eyebrow::before {
    content:'';
    width:6px; height:6px;
    border-radius:50%;
    background: var(--accent);
    animation: pdot 2s infinite;
}
@keyframes pdot {
    0%,100%{opacity:1;transform:scale(1)}
    50%{opacity:.4;transform:scale(.75)}
}
.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(2.2rem,4.5vw,3.4rem) !important;
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
    max-width: 460px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── NAV TABS ── */
.nav-bar {
    display: flex;
    gap: 0.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 6px;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-xs);
}
.nav-bar-placeholder { display:none; }

/* Streamlit button resets for nav */
.stButton > button {
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.4rem !important;
    transition: var(--transition) !important;
    cursor: pointer !important;
}

/* Nav buttons (col-wrapped) */
div[data-testid="column"] .stButton > button {
    background: transparent !important;
    color: var(--text-second) !important;
    width: 100% !important;
    border-radius: var(--radius-sm) !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: var(--surface-2) !important;
    color: var(--text-primary) !important;
}

/* Full-width action buttons */
.stButton.full > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--text-primary) !important;
    color: #fff !important;
    width: 100% !important;
    padding: 0.82rem 2rem !important;
    font-size: 0.93rem !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.16) !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
.stButton.full > button:hover {
    background: #000 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.28) !important;
    transform: translateY(-1px) !important;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-third);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── INPUTS ── */
.stTextInput label, .stSelectbox label, .stRadio label, .stSelectSlider label {
    font-family: var(--font-sans) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
}
.stTextInput input {
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
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft), var(--shadow-xs) !important;
    background: var(--surface) !important;
}
.stTextInput input::placeholder { color: var(--text-third) !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
}

/* ── QUESTION CARD ── */
.q-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow-xs);
    transition: var(--transition);
}
.q-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
}
.q-num {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.q-text {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
    margin-bottom: 0.9rem;
}
.opt {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    font-size: 0.86rem;
    color: var(--text-second);
    margin-bottom: 6px;
    transition: var(--transition);
}
.opt-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: var(--border);
    display:inline-flex;
    align-items:center; justify-content:center;
    font-size:0.72rem; font-weight:700;
    color: var(--text-third);
    flex-shrink:0;
}
.opt.correct {
    background: var(--success-soft) !important;
    border-color: rgba(52,199,89,0.35) !important;
    color: #1a7a35 !important;
}
.opt.correct .opt-num { background: var(--success); color:#fff; }
.opt.wrong {
    background: var(--danger-soft) !important;
    border-color: rgba(255,59,48,0.3) !important;
    color: #b0190f !important;
}
.opt.wrong .opt-num { background: var(--danger); color:#fff; }
.correct-badge {
    display:inline-block;
    font-size:0.72rem; font-weight:700;
    color: var(--success);
    background: var(--success-soft);
    border-radius:100px;
    padding:3px 10px;
    margin-top:0.6rem;
}

/* ── SCORE CARD ── */
.score-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    margin-bottom: 2rem;
}
.score-big {
    font-family: var(--font-display) !important;
    font-size: 4rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 0.5rem;
}
.score-sub { font-size:0.88rem; color:var(--text-third); }
.score-pct {
    display:inline-block;
    background: var(--accent-soft);
    color: var(--accent);
    font-size:0.82rem; font-weight:700;
    border-radius:100px;
    padding:4px 14px;
    margin-top:0.6rem;
}

/* ── ALERTS ── */
.stSuccess {
    background: var(--success-soft) !important;
    border:1px solid rgba(52,199,89,0.28) !important;
    border-radius:var(--radius-sm) !important;
    color:#1a7a35 !important;
}
.stError {
    background: var(--danger-soft) !important;
    border:1px solid rgba(255,59,48,0.25) !important;
    border-radius:var(--radius-sm) !important;
}
.stWarning {
    background: var(--warning-soft) !important;
    border:1px solid rgba(255,159,10,0.28) !important;
    border-radius:var(--radius-sm) !important;
}
.stInfo {
    background: var(--accent-soft) !important;
    border:1px solid rgba(0,113,227,0.2) !important;
    border-radius:var(--radius-sm) !important;
    color:var(--accent) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border:1px solid var(--border) !important;
    border-radius:var(--radius-sm) !important;
    font-family:var(--font-sans) !important;
    font-size:0.88rem !important;
    font-weight:600 !important;
    color:var(--text-primary) !important;
    padding:0.85rem 1.1rem !important;
    transition:var(--transition) !important;
}
.streamlit-expanderHeader:hover {
    background:var(--surface-2) !important;
    border-color:var(--border-hover) !important;
}
.streamlit-expanderContent {
    background:var(--surface) !important;
    border:1px solid var(--border) !important;
    border-top:none !important;
    border-radius:0 0 var(--radius-sm) var(--radius-sm) !important;
    padding:1.2rem 1.4rem !important;
}

/* ── HISTORY ITEM ── */
.history-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    border-left: 3px solid var(--accent);
    transition: var(--transition);
}
.history-item:hover {
    box-shadow: var(--shadow-sm);
    transform: translateX(2px);
}
.history-name { font-size:0.9rem; font-weight:700; color:var(--text-primary); margin-bottom:0.25rem; }
.history-meta { font-size:0.78rem; color:var(--text-third); }
.pct-pill {
    display:inline-block;
    background: var(--accent-soft);
    color:var(--accent);
    font-size:0.72rem; font-weight:700;
    border-radius:100px;
    padding:2px 10px;
    margin-left:6px;
}

/* ── DIVIDER ── */
hr { border-color:var(--border) !important; margin:1.5rem 0 !important; }

/* ── RADIO ── */
.stRadio > div { flex-direction:row !important; gap:0.5rem !important; }
.stRadio > div > label {
    background:var(--surface-2) !important;
    border:1px solid var(--border) !important;
    border-radius:8px !important;
    padding:0.5rem 1rem !important;
    font-size:0.85rem !important;
    font-weight:500 !important;
    color:var(--text-second) !important;
    cursor:pointer !important;
    transition:var(--transition) !important;
}
.stRadio > div > label:hover {
    border-color:var(--accent) !important;
    color:var(--accent) !important;
    background:var(--accent-soft) !important;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align:center;
    padding:4rem 2rem;
}
.empty-icon { font-size:2.5rem; margin-bottom:1rem; opacity:0.2; }
.empty-title { font-size:1rem; font-weight:600; color:var(--text-second); margin-bottom:0.4rem; }
.empty-sub { font-size:0.84rem; color:var(--text-third); }

/* ── FOOTER ── */
.footer {
    text-align:center;
    padding:2.5rem 0 1rem;
    font-size:0.76rem;
    color:var(--text-third);
    letter-spacing:0.02em;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:var(--border-hover); border-radius:100px; }
</style>
""", unsafe_allow_html=True)

# ─── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by Gemini AI</div>
    <h1 class="hero-title">Test knowledge.<br>Track mastery.</h1>
    <p class="hero-subtitle">
        Generate full exams, attempt them live, and review results — all from one clean interface.
    </p>
</div>
""", unsafe_allow_html=True)


# ─── STRUCTURED OUTPUT CLASSES ──────────────────────────────────────────────────
class Options(BaseModel):
    question: str = Field(description="MCQ question on given topic")
    Option1: str = Field(description="1st Option for MCQ")
    Option2: str = Field(description="2nd Option for MCQ")
    Option3: str = Field(description="3rd Option for MCQ")
    Option4: str = Field(description="4th Option for MCQ")
    correct: int = Field(description="Correct option number (1-4)")

class MCQs(BaseModel):
    MCQ1:  List[Options] = Field(description="1st MCQ and its options from Given Topic")
    MCQ2:  List[Options] = Field(description="2nd MCQ and its options from Given Topic")
    MCQ3:  List[Options] = Field(description="3rd MCQ and its options from Given Topic")
    MCQ4:  List[Options] = Field(description="4th MCQ and its options from Given Topic")
    MCQ5:  List[Options] = Field(description="5th MCQ and its options from Given Topic")
    MCQ6:  List[Options] = Field(description="6th MCQ and its options from Given Topic")
    MCQ7:  List[Options] = Field(description="7th MCQ and its options from Given Topic")
    MCQ8:  List[Options] = Field(description="8th MCQ and its options from Given Topic")
    MCQ9:  List[Options] = Field(description="9th MCQ and its options from Given Topic")
    MCQ10: List[Options] = Field(description="10th MCQ and its options from Given Topic")
    MCQ11: List[Options] = Field(description="11th MCQ and its options from Given Topic")
    MCQ12: List[Options] = Field(description="12th MCQ and its options from Given Topic")

class Answers(BaseModel):
    Answer1: str = Field(description="A brief and short Answer of question1")
    Answer2: str = Field(description="A brief and short Answer of question2")
    Answer3: str = Field(description="A brief and short Answer of question3")
    Answer4: str = Field(description="A brief and short Answer of question4")
    Answer5: str = Field(description="A brief and short Answer of question5")
    Answer6: str = Field(description="A brief and short Answer of question6")
    Answer7: str = Field(description="A brief and short Answer of question7")
    Answer8: str = Field(description="A brief and short Answer of question8")
    LongAnswer1: str = Field(description="Answer of Longquestion1")
    LongAnswer2: str = Field(description="Answer of Longquestion2")

class Questions(BaseModel):
    question1: str = Field(description="1st short question of the given topic")
    question2: str = Field(description="2nd short question of the given topic")
    question3: str = Field(description="3rd short question of the given topic")
    question4: str = Field(description="4th short question of the given topic")
    question5: str = Field(description="5th short question of the given topic")
    question6: str = Field(description="6th short question of the given topic")
    question7: str = Field(description="7th short question of the given topic")
    question8: str = Field(description="8th short question of the given topic")
    LongQuestion1: str = Field(description="1st Long question of the given topic")
    LongQuestion2: str = Field(description="2nd Long question of the given topic")
    Responses: List[Answers] = Field(description="Answers these questions one by one")


# ─── SESSION STATE ───────────────────────────────────────────────────────────────
defaults = {
    'subject': "", 'topic': "", 'mcqs': None, 'short_questions': None,
    'active_tab': "generate", 'current_exam_id': None,
    'student_name': "", 'student_answers': {}, 'grading_complete': False,
    'show_exam': False, 'chat_history': [],
    'attempt_score': 0, 'attempt_total': 12
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── NAV BAR ────────────────────────────────────────────────────────────────────
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("✦  Generate Exam", use_container_width=True):
        st.session_state.active_tab = "generate"
        st.rerun()
with nav2:
    if st.button("◎  Attempt Exam", use_container_width=True):
        st.session_state.active_tab = "attempt"
        st.rerun()
with nav3:
    if st.button("⊞  View History", use_container_width=True):
        st.session_state.active_tab = "history"
        st.rerun()

# Active tab indicator
tab_labels = {"generate": "Generate Exam", "attempt": "Attempt Exam", "history": "View History"}
st.markdown(f"""
<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
color:var(--accent);margin-bottom:1.8rem;padding-left:2px;">
    ◆ &nbsp;{tab_labels.get(st.session_state.active_tab, '')}
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE EXAM
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "generate":

    st.markdown('<div class="section-label">Exam Setup</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.subject = st.text_input("Subject", st.session_state.subject,
                                                   placeholder="e.g. Physics, History")
    with col2:
        st.session_state.topic = st.text_input("Topic", st.session_state.topic,
                                                placeholder="e.g. Newton's Laws, WWI")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if st.button("Generate Exam →", use_container_width=True):
        with st.spinner("Generating exam questions…"):
            try:
                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

                mcq_prompt = f"Create 12 MCQs on {st.session_state.topic} for {st.session_state.subject}. For each question, include the correct answer option number (1-4)."
                mcq_LLM = llm.with_structured_output(MCQs)
                st.session_state.mcqs = mcq_LLM.invoke(mcq_prompt)

                sq_prompt = f"Generate 8 short questions and 2 long questions each with short and concise Answers on {st.session_state.topic} for {st.session_state.subject}"
                sq_llm = llm.with_structured_output(Questions)
                st.session_state.short_questions = sq_llm.invoke(sq_prompt)

                exam_data = {
                    "subject": st.session_state.subject,
                    "topic": st.session_state.topic,
                    "mcqs": st.session_state.mcqs.model_dump_json(),
                    "short_questions": st.session_state.short_questions.model_dump_json(),
                    "long_questions": json.dumps({
                        "LongQuestion1": st.session_state.short_questions.LongQuestion1,
                        "LongQuestion2": st.session_state.short_questions.LongQuestion2
                    })
                }

                c.execute('''INSERT INTO exams (subject, topic, mcqs, short_questions, long_questions)
                             VALUES (?, ?, ?, ?, ?)''',
                          (exam_data["subject"], exam_data["topic"],
                           exam_data["mcqs"], exam_data["short_questions"],
                           exam_data["long_questions"]))
                conn.commit()
                st.session_state.current_exam_id = c.lastrowid
                st.session_state.show_exam = True
                st.success(f"Exam ready — ID {st.session_state.current_exam_id}")

            except Exception as e:
                st.error(f"Error generating exam: {str(e)}")
                st.session_state.mcqs = None
                st.session_state.short_questions = None

    # ── Display generated exam ──
    if st.session_state.mcqs and st.session_state.short_questions and st.session_state.show_exam:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
            color:var(--text-third);margin-bottom:0.4rem;">Generated Exam</div>
            <div style="font-size:1.45rem;font-weight:700;color:var(--text-primary);letter-spacing:-0.03em;">
                {st.session_state.subject}
                <span style="color:var(--text-third);font-weight:400;"> · {st.session_state.topic}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Multiple Choice Questions</div>', unsafe_allow_html=True)
        for i in range(1, 13):
            mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
            opts_html = "".join([
                f'<div class="opt"><span class="opt-num">{j}</span> {getattr(mcq, f"Option{j}")}'
                + (' <span class="correct-badge">✓ Correct</span>' if j == mcq.correct else '')
                + '</div>'
                for j in range(1, 5)
            ])
            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">Question {i}</div>
                <div class="q-text">{mcq.question}</div>
                {opts_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1.5rem;">Short Answer Questions</div>',
                    unsafe_allow_html=True)
        for i in range(1, 9):
            q = getattr(st.session_state.short_questions, f"question{i}")
            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">Short Q{i}</div>
                <div class="q-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:1.5rem;">Long Answer Questions</div>',
                    unsafe_allow_html=True)
        for i, attr in enumerate(["LongQuestion1", "LongQuestion2"], 1):
            q = getattr(st.session_state.short_questions, attr)
            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">Long Q{i}</div>
                <div class="q-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        if st.button("Attempt This Exam →", use_container_width=True):
            st.session_state.active_tab = "attempt"
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# ATTEMPT EXAM
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "attempt":

    st.markdown('<div class="section-label">Select & Attempt</div>', unsafe_allow_html=True)

    c.execute("SELECT id, subject, topic FROM exams ORDER BY id DESC")
    exams = c.fetchall()

    if not exams:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◎</div>
            <div class="empty-title">No exams available</div>
            <div class="empty-sub">Generate an exam first to attempt it here.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Generate →", use_container_width=True):
            st.session_state.active_tab = "generate"
            st.rerun()
        st.stop()

    exam_options = [f"{exam[1]} — {exam[2]}  (ID {exam[0]})" for exam in exams]
    selected_exam = st.selectbox("Choose an Exam", exam_options)
    exam_id = int(selected_exam.split("(ID ")[1].replace(")", ""))

    c.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    exam_data = c.fetchone()

    if exam_data:
        exam_id, subject, topic, created_at, mcqs_json, short_questions_json, long_questions_json = exam_data
        st.session_state.mcqs = MCQs.model_validate_json(mcqs_json)
        st.session_state.short_questions = Questions.model_validate_json(short_questions_json)
        st.session_state.current_exam_id = exam_id

        st.markdown(f"""
        <div style="background:var(--accent-soft);border:1px solid rgba(0,113,227,0.18);
        border-radius:var(--radius-sm);padding:0.85rem 1.1rem;margin-bottom:1.4rem;
        font-size:0.86rem;color:var(--accent);font-weight:500;">
            {subject} · {topic}
            <span style="color:var(--text-third);margin-left:0.8rem;font-weight:400;font-size:0.78rem;">
                Created {created_at[:10]}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.student_name = st.text_input(
            "Your Name", st.session_state.student_name, placeholder="Enter your full name"
        )

        if not st.session_state.student_name:
            st.warning("Please enter your name to begin.")
            st.stop()

        st.markdown('<div class="section-label" style="margin-top:1rem;">Multiple Choice Questions</div>',
                    unsafe_allow_html=True)

        for i in range(1, 13):
            mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
            if f"mcq_{i}" not in st.session_state.student_answers:
                st.session_state.student_answers[f"mcq_{i}"] = None

            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">Question {i} of 12</div>
                <div class="q-text">{mcq.question}</div>
            </div>
            """, unsafe_allow_html=True)

            options = [mcq.Option1, mcq.Option2, mcq.Option3, mcq.Option4]
            selected = st.radio(
                f"Answer for Q{i}",
                options,
                index=None,
                key=f"mcq_{i}",
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.student_answers[f"mcq_{i}"] = options.index(selected) + 1 if selected else None
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        if st.button("Submit Exam →", use_container_width=True):
            score = sum(
                1 for i in range(1, 13)
                if (ans := st.session_state.student_answers.get(f"mcq_{i}")) and
                   ans == getattr(st.session_state.mcqs, f"MCQ{i}")[0].correct
            )
            total_mcqs = 12

            c.execute('''INSERT INTO attempts (exam_id, student_name, answers, score, total)
                         VALUES (?, ?, ?, ?, ?)''',
                      (exam_id, st.session_state.student_name,
                       json.dumps(st.session_state.student_answers), score, total_mcqs))
            conn.commit()
            st.session_state.grading_complete = True
            st.session_state.attempt_score = score
            st.session_state.attempt_total = total_mcqs
            st.success("Exam submitted. Here are your results.")

        # ── Results ──
        if st.session_state.grading_complete:
            score = st.session_state.attempt_score
            total = st.session_state.attempt_total
            pct = round((score / total) * 100, 1)

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="score-card">
                <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                color:var(--text-third);margin-bottom:0.8rem;">Your Score</div>
                <div class="score-big">{score}<span style="font-size:2rem;color:var(--text-third);">/{total}</span></div>
                <div class="score-sub">Multiple Choice Questions</div>
                <div class="score-pct">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-label">Question Review</div>', unsafe_allow_html=True)

            for i in range(1, 13):
                mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
                student_answer = st.session_state.student_answers.get(f"mcq_{i}")
                is_correct = student_answer == mcq.correct

                opts_html = ""
                for j in range(1, 5):
                    opt_text = getattr(mcq, f'Option{j}')
                    css_class = ""
                    label = ""
                    if j == student_answer and is_correct:
                        css_class = "correct"
                        label = " ✓ Your answer"
                    elif j == student_answer and not is_correct:
                        css_class = "wrong"
                        label = " ✗ Your answer"
                    elif j == mcq.correct:
                        css_class = "correct"
                        label = " ✓ Correct answer"
                    opts_html += f'<div class="opt {css_class}"><span class="opt-num">{j}</span>{opt_text}<span style="margin-left:auto;font-size:0.75rem;font-weight:600;">{label}</span></div>'

                status_icon = "✓" if is_correct else "✗"
                status_color = "var(--success)" if is_correct else "var(--danger)"
                st.markdown(f"""
                <div class="q-card">
                    <div class="q-num" style="color:{status_color};">{status_icon} &nbsp;Question {i}</div>
                    <div class="q-text">{mcq.question}</div>
                    {opts_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            if st.button("View History →", use_container_width=True):
                st.session_state.active_tab = "history"
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAM HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "history":

    st.markdown('<div class="section-label">All Exams</div>', unsafe_allow_html=True)

    c.execute("SELECT * FROM exams ORDER BY id DESC")
    exams = c.fetchall()

    if not exams:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">⊞</div>
            <div class="empty-title">No history yet</div>
            <div class="empty-sub">Generate and attempt exams to see records here.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    for exam in exams:
        exam_id, subject, topic, created_at, mcqs, short_questions, long_questions = exam
        c.execute("SELECT * FROM attempts WHERE exam_id = ? ORDER BY submitted_at DESC", (exam_id,))
        attempts = c.fetchall()

        with st.expander(f"{subject}  ·  {topic}  —  {created_at[:10]}  ({len(attempts)} attempt{'s' if len(attempts)!=1 else ''})"):
            st.markdown(f"""
            <div style="font-size:0.78rem;color:var(--text-third);margin-bottom:1rem;">
                Exam ID: <strong style="color:var(--text-second)">{exam_id}</strong>
                &nbsp;·&nbsp; Created: {created_at}
            </div>
            """, unsafe_allow_html=True)

            if attempts:
                st.markdown('<div class="section-label">Student Attempts</div>', unsafe_allow_html=True)
                for attempt in attempts:
                    attempt_id, _, student_name, answers, score, total, submitted_at = attempt
                    pct = round((score / total) * 100, 1) if total else 0
                    st.markdown(f"""
                    <div class="history-item">
                        <div class="history-name">{student_name}</div>
                        <div class="history-meta">
                            {submitted_at[:16]} &nbsp;·&nbsp;
                            Score: <strong>{score}/{total}</strong>
                            <span class="pct-pill">{pct}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size:0.84rem;color:var(--text-third);">No attempts yet.</div>',
                            unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    with st.expander("⚠️  Delete an Exam"):
        exam_options = [f"{exam[1]} — {exam[2]} (ID {exam[0]})" for exam in exams]
        selected_del = st.selectbox("Select exam to delete", exam_options, key="del_select")
        del_id = int(selected_del.split("(ID ")[1].replace(")", ""))
        if st.button(f"Permanently Delete Selected Exam", use_container_width=True):
            c.execute("DELETE FROM exams WHERE id = ?", (del_id,))
            conn.commit()
            st.success("Exam deleted.")
            st.rerun()


# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ExamOS &nbsp;·&nbsp; Generate · Attempt · Grade &nbsp;·&nbsp; Powered by Gemini AI
</div>
""", unsafe_allow_html=True)

conn.close()