import streamlit as st
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.tools import YouTubeSearchTool

tool = YouTubeSearchTool()

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = str(os.getenv("GOOGLE_API_KEY"))
os.environ["GROQ_API_KEY"] = str(os.getenv("GROQ_API_KEY"))


# --- Structured Output Classes ---
class Study_plan_for_week(BaseModel):
    day1: str = Field(description="Plan for day one and also adding some details to start learning")
    day2: str = Field(description="Plan for day two and also adding some details to start learning")
    day3: str = Field(description="Plan for day three and also adding some details to start learning")
    day4: str = Field(description="Plan for day four and also adding some details to start learning")
    day5: str = Field(description="Plan for day five and also adding some details to start learning")
    day6: str = Field(description="Plan for day six and also adding some details to start learning")
    day7: str = Field(description="Plan for day seven and also adding some details to start learning")


class Study_plan(BaseModel):
    day1: str = Field(description="Plan for day one and also adding some details to start learning")
    day2: str = Field(description="Plan for day two and also adding some details to start learning")
    day3: str = Field(description="Plan for day three and also adding some details to start learning")
    day4: str = Field(description="Plan for day four and also adding some details to start learning")
    day5: str = Field(description="Plan for day five and also adding some details to start learning")
    day6: str = Field(description="Plan for day six and also adding some details to start learning")
    day7: str = Field(description="Plan for day seven and also adding some details to start learning")
    day8: str = Field(description="Plan for day eight and also adding some details to start learning")
    day9: str = Field(description="Plan for day nine and also adding some details to start learning")
    day10: str = Field(description="Plan for day ten and also adding some details to start learning")
    day11: str = Field(description="Plan for day eleven and also adding some details to start learning")
    day12: str = Field(description="Plan for day twelve and also adding some details to start learning")
    day13: str = Field(description="Plan for day thirteen and also adding some details to start learning")
    day14: str = Field(description="Plan for day fourteen and also adding some details to start learning")
    day15: str = Field(description="Plan for day fifteen and also adding some details to start learning")
    day16: str = Field(description="Plan for day sixteen and also adding some details to start learning")
    day17: str = Field(description="Plan for day seventeen and also adding some details to start learning")
    day18: str = Field(description="Plan for day eighteen and also adding some details to start learning")
    day19: str = Field(description="Plan for day nineteen and also adding some details to start learning")
    day20: str = Field(description="Plan for day twenty and also adding some details to start learning")
    day21: str = Field(description="Plan for day twenty one and also adding some details to start learning")
    day22: str = Field(description="Plan for day twenty two and also adding some details to start learning")
    day23: str = Field(description="Plan for day twenty three and also adding some details to start learning")
    day24: str = Field(description="Plan for day twenty four and also adding some details to start learning")
    day25: str = Field(description="Plan for day twenty five and also adding some details to start learning")
    day26: str = Field(description="Plan for day twenty six and also adding some details to start learning")
    day27: str = Field(description="Plan for day twenty seven and also adding some details to start learning")
    day28: str = Field(description="Plan for day twenty eight and also adding some details to start learning")


# --- UI Configuration ---
st.set_page_config(
    page_title="StudyOS · AI Lesson Planner",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── APPLE-STYLE PREMIUM CSS ───────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600&display=swap" rel="stylesheet">

<style>
/* ── RESET & BASE ── */
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
    --accent-soft:  rgba(0, 113, 227, 0.08);
    --success:      #34c759;
    --danger:       #ff3b30;
    --warning:      #ff9f0a;
    --radius-sm:    10px;
    --radius:       16px;
    --radius-lg:    24px;
    --shadow-xs:    0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-sm:    0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.04);
    --shadow:       0 8px 32px rgba(0,0,0,0.09), 0 2px 8px rgba(0,0,0,0.05);
    --shadow-lg:    0 20px 60px rgba(0,0,0,0.12), 0 4px 16px rgba(0,0,0,0.06);
    --font-sans:    'Figtree', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-display: 'Playfair Display', Georgia, serif;
    --transition:   all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── APP BACKGROUND ── */
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--font-sans) !important;
}

[data-testid="stHeader"] { display: none !important; }

[data-testid="block-container"] {
    padding: 2.5rem 3rem 4rem 3rem !important;
    max-width: 900px;
    margin: 0 auto;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.4rem !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-sans) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-third) !important;
    border: none !important;
    margin-bottom: 1rem !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
}

.stMarkdown p, .stMarkdown li {
    font-family: var(--font-sans) !important;
    color: var(--text-second) !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
}

/* ── HERO HEADER ── */
.hero {
    text-align: center;
    padding: 4rem 2rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}

.hero-eyebrow::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(2.4rem, 5vw, 3.6rem) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    line-height: 1.15 !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 1rem !important;
    border: none !important;
}

.hero-subtitle {
    font-size: 1.05rem !important;
    color: var(--text-second) !important;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── CARD SURFACE ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem 2.2rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.5rem;
    transition: var(--transition);
}

.card:hover {
    box-shadow: var(--shadow);
    border-color: var(--border-hover);
}

.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-third);
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── FORM INPUTS ── */
.stTextInput input,
.stSelectSlider > div > div,
.stRadio > div {
    font-family: var(--font-sans) !important;
}

.stTextInput label,
.stSelectSlider label,
.stRadio label,
.stSlider label {
    font-family: var(--font-sans) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 0.3rem !important;
}

.stTextInput input {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-xs) !important;
}

.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft), var(--shadow-xs) !important;
    background: var(--surface) !important;
    outline: none !important;
}

.stTextInput input::placeholder { color: var(--text-third) !important; }

/* ── RADIO ── */
.stRadio > div {
    display: flex;
    gap: 0.75rem;
    flex-direction: row !important;
}

.stRadio > div > label {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.2rem !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
    font-size: 0.88rem !important;
    color: var(--text-second) !important;
    font-weight: 500 !important;
}

.stRadio > div > label:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-soft) !important;
}

/* ── SELECT SLIDER ── */
.stSelectSlider > div {
    padding: 0 !important;
}

/* ── DIVIDER ── */
.stDivider { margin: 1.6rem 0 !important; opacity: 0.5 !important; }
hr { border-color: var(--border) !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 0.65rem 1.6rem !important;
    transition: var(--transition) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}

/* Primary (form submit) button */
[data-testid="stFormSubmitButton"] > button {
    background: var(--text-primary) !important;
    color: #fff !important;
    width: 100% !important;
    padding: 0.85rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18) !important;
}

[data-testid="stFormSubmitButton"] > button:hover {
    background: #000 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
}

/* Sidebar plan buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 0.8rem !important;
    text-align: left !important;
    padding: 0.65rem 0.9rem !important;
    width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition: var(--transition) !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--surface-2) !important;
    border-color: var(--border-hover) !important;
}

/* Delete button */
[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button {
    color: var(--danger) !important;
    border-color: transparent !important;
    padding: 0.65rem 0.5rem !important;
    background: transparent !important;
    font-size: 0.9rem !important;
}

[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button:hover {
    background: rgba(255,59,48,0.08) !important;
    border-color: rgba(255,59,48,0.2) !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-color: var(--accent) transparent transparent transparent !important;
}

/* ── ALERTS ── */
.stSuccess {
    background: rgba(52,199,89,0.08) !important;
    border: 1px solid rgba(52,199,89,0.25) !important;
    border-radius: var(--radius-sm) !important;
    color: #1a7a35 !important;
}

.stError {
    background: rgba(255,59,48,0.08) !important;
    border: 1px solid rgba(255,59,48,0.25) !important;
    border-radius: var(--radius-sm) !important;
}

.stInfo {
    background: var(--accent-soft) !important;
    border: 1px solid rgba(0,113,227,0.2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--accent) !important;
}

/* ── TABS ── */
[data-testid="stTabs"] {
    border: none !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface-2) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
    display: inline-flex !important;
    margin-bottom: 1.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: var(--font-sans) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text-second) !important;
    background: transparent !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 6px 20px !important;
    transition: var(--transition) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-xs) !important;
}

.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── EXPANDERS (day cards) ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    padding: 0.85rem 1.1rem !important;
    transition: var(--transition) !important;
}

.streamlit-expanderHeader:hover {
    background: var(--surface-2) !important;
    border-color: var(--border-hover) !important;
}

.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
    padding: 1rem 1.2rem !important;
}

/* ── DAY PLAN CARD ── */
.day-plan {
    background: var(--surface-2);
    border-radius: var(--radius-sm);
    padding: 1rem 1.2rem;
    font-size: 0.91rem;
    color: var(--text-second);
    line-height: 1.7;
    border-left: 3px solid var(--accent);
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1.2rem;
    opacity: 0.25;
}

.empty-state-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-second);
    margin-bottom: 0.5rem;
}

.empty-state-sub {
    font-size: 0.88rem;
    color: var(--text-third);
}

/* ── FEATURES GRID ── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}

.feature-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.2rem;
    transition: var(--transition);
}

.feature-item:hover {
    background: var(--surface);
    box-shadow: var(--shadow-sm);
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 1.4rem;
    margin-bottom: 0.7rem;
}

.feature-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.35rem;
}

.feature-desc {
    font-size: 0.8rem;
    color: var(--text-third);
    line-height: 1.5;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    font-size: 0.78rem;
    color: var(--text-third);
    letter-spacing: 0.01em;
}

/* ── SIDEBAR PLAN ITEM ── */
.sidebar-plan-meta {
    font-size: 0.7rem;
    color: var(--text-third);
    margin-bottom: 0.3rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.sidebar-empty {
    font-size: 0.82rem;
    color: var(--text-third);
    text-align: center;
    padding: 2rem 0.5rem;
    line-height: 1.5;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 100px; }

/* ── FORM CONTAINER ── */
[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem 2.2rem 2rem !important;
    box-shadow: var(--shadow-sm) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HERO HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by Gemini AI</div>
    <h1 class="hero-title">Learn anything.<br>One day at a time.</h1>
    <p class="hero-subtitle">
        Generate a beautifully structured study plan tailored to your topic,
        pace, and ambition — in seconds.
    </p>
</div>
""", unsafe_allow_html=True)


# ─── CONFIGURATION FORM ─────────────────────────────────────────────────────────
with st.form("config_form"):
    st.markdown('<div class="section-label">Your Learning Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic", placeholder="e.g. Machine Learning, Piano, Spanish")
    with col2:
        subject = st.text_input("Subject", placeholder="e.g. Computer Science, Music, Language")

    daily_hours = st.text_input("Daily Study Hours", placeholder="e.g. 2")

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        plan_type = st.radio("Plan Duration", ["One Week", "One Month"])
    with col4:
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner"
        )

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    submit_button = st.form_submit_button("Generate Study Plan →")


# ─── PLAN GENERATION ────────────────────────────────────────────────────────────
if submit_button:
    with st.spinner("Crafting your personalized plan…"):
        try:
            if plan_type == "One Week":
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
                structured_llm = llm.with_structured_output(Study_plan_for_week)
                prompt = f"""
                Create a {difficulty.lower()} study plan for one week (7 days) on TOPIC: {topic} OF SUBJECT: {subject}
                - Each day should have: title, topics, resources, exercises
                - Daily study time: {daily_hours} hours
                - Include practical exercises.
                """
                response = structured_llm.invoke(prompt)
            else:
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
                structured_llm1 = llm.with_structured_output(Study_plan)
                prompt1 = f"""
                Create a {difficulty.lower()} study plan for one month on Topic: {topic} of Subject: {subject}.
                - Each day should have: title, topics, resources, exercises
                - Daily study time: {daily_hours} hours
                - Include practical exercises
                """
                response = structured_llm1.invoke(prompt1)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">◎</div>
        <div class="empty-state-title">No plan generated yet</div>
        <div class="empty-state-sub">Fill in your details above and click <strong>Generate Study Plan</strong></div>
    </div>
    """, unsafe_allow_html=True)


# ─── DATABASE ───────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 topic TEXT, subject TEXT, daily_hours TEXT,
                 plan_type TEXT, difficulty TEXT, plan_data TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def save_plan(topic, subject, daily_hours, plan_type, difficulty, plan_data):
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''INSERT INTO plans (topic, subject, daily_hours, plan_type, difficulty, plan_data)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (topic, subject, daily_hours, plan_type, difficulty, json.dumps(plan_data)))
    conn.commit()
    conn.close()


def get_plan_history():
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('SELECT id, topic, subject, plan_type, created_at FROM plans ORDER BY created_at DESC')
    history = c.fetchall()
    conn.close()
    return history


def get_plan_by_id(plan_id):
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('SELECT * FROM plans WHERE id = ?', (plan_id,))
    plan = c.fetchone()
    conn.close()
    return plan


init_db()


# ─── SAVE PLAN AFTER GENERATION ─────────────────────────────────────────────────
if submit_button:
    with st.spinner("Saving your plan…"):
        try:
            if plan_type == "One Week":
                plan_data = {f'day{i}': getattr(response, f'day{i}') for i in range(1, 8)}
            else:
                plan_data = {f'day{i}': getattr(response, f'day{i}') for i in range(1, 29)}

            save_plan(topic, subject, daily_hours, plan_type, difficulty, plan_data)

            st.session_state.current_plan = {
                'topic': topic,
                'subject': subject,
                'daily_hours': daily_hours,
                'plan_type': plan_type,
                'difficulty': difficulty,
                'plan_data': plan_data
            }

            st.success("Your study plan is ready — let's get started.")

        except Exception as e:
            st.error(f"Error saving plan: {str(e)}")


# ─── CALLBACKS ──────────────────────────────────────────────────────────────────
def load_plan_callback(plan_id):
    plan_data = get_plan_by_id(plan_id)
    st.session_state.current_plan = {
        'topic': plan_data[1],
        'subject': plan_data[2],
        'daily_hours': plan_data[3],
        'plan_type': plan_data[4],
        'difficulty': plan_data[5],
        'plan_data': json.loads(plan_data[6])
    }


def delete_plan_callback(plan_id, container):
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
    conn.commit()
    conn.close()
    container.empty()


# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">Saved Plans</div>', unsafe_allow_html=True)

    history = get_plan_history()

    if not history:
        st.markdown("""
        <div class="sidebar-empty">
            No plans saved yet.<br>Generate one to see it here.
        </div>
        """, unsafe_allow_html=True)
    else:
        for plan in history:
            plan_id, p_topic, p_subject, p_type, created_at = plan
            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            plan_container = st.container()
            with plan_container:
                cols = st.columns([5, 1])
                with cols[0]:
                    st.button(
                        f"{p_topic} · {p_subject}",
                        key=f"load_{plan_id}",
                        on_click=load_plan_callback,
                        args=(plan_id,)
                    )
                    st.markdown(
                        f'<div class="sidebar-plan-meta">{p_type} · {dt.strftime("%b %d, %Y")}</div>',
                        unsafe_allow_html=True
                    )
                with cols[1]:
                    st.button(
                        "✕",
                        key=f"del_{plan_id}",
                        on_click=delete_plan_callback,
                        args=(plan_id, plan_container)
                    )


# ─── DISPLAY CURRENT PLAN ────────────────────────────────────────────────────────
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

if 'current_plan' in st.session_state:
    plan      = st.session_state.current_plan
    plan_type = plan['plan_type']
    plan_data = plan['plan_data']

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--text-third);margin-bottom:0.5rem;">
            Your Plan
        </div>
        <div style="font-size:1.55rem;font-weight:700;color:var(--text-primary);letter-spacing:-0.03em;">
            {plan['topic']}
            <span style="color:var(--text-third);font-weight:400;"> · {plan['subject']}</span>
        </div>
        <div style="font-size:0.82rem;color:var(--text-third);margin-top:0.35rem;">
            {plan_type} &nbsp;·&nbsp; {plan['difficulty']} &nbsp;·&nbsp; {plan['daily_hours']}h/day
        </div>
    </div>
    """, unsafe_allow_html=True)

    def render_week(day_keys):
        for idx, key in enumerate(day_keys):
            day_name = WEEK_DAYS[idx % 7]
            text = plan_data.get(key, "")
            with st.expander(f"📅  {day_name}", expanded=False):
                st.markdown(f'<div class="day-plan">{text}</div>', unsafe_allow_html=True)

    if plan_type == "One Week":
        render_week([f'day{i}' for i in range(1, 8)])

    else:
        tab1, tab2, tab3, tab4 = st.tabs(["Week 1", "Week 2", "Week 3", "Week 4"])
        with tab1:
            render_week([f'day{i}' for i in range(1, 8)])
        with tab2:
            render_week([f'day{i}' for i in range(8, 15)])
        with tab3:
            render_week([f'day{i}' for i in range(15, 22)])
        with tab4:
            render_week([f'day{i}' for i in range(22, 29)])


# ─── FEATURES SECTION ───────────────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<div class="features-grid">
    <div class="feature-item">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Personalized Plans</div>
        <div class="feature-desc">AI creates custom learning paths tuned to your topic and skill level.</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">⏱</div>
        <div class="feature-title">Flexible Duration</div>
        <div class="feature-desc">Choose a focused 1-week sprint or a thorough 1-month deep dive.</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Progress Tracking</div>
        <div class="feature-desc">Visualize your journey day by day with a clean, structured view.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    StudyOS &nbsp;·&nbsp; Built with Streamlit &amp; Gemini &nbsp;·&nbsp; Your intelligent learning companion
</div>
""", unsafe_allow_html=True)