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

# Create tables
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


# Custom CSS for styling
st.markdown("""
    <style>
    :root {
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #0f3460;
        --highlight: #e94560;
        --text: #f1f1f1;
        --light-bg: rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: var(--text);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stButton>button {
        background: var(--highlight) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        transition: all 0.3s;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--highlight);
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, var(--accent), var(--highlight));
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .card {
        background: var(--light-bg);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .question-card {
        background: rgba(15, 52, 96, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateY(-3px);
        background: rgba(15, 52, 96, 0.5);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .option {
        padding: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin: 5px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .correct-answer {
        background: rgba(46, 196, 182, 0.2) !important;
        border: 1px solid rgba(46, 196, 182, 0.5) !important;
    }
    
    .incorrect-answer {
        background: rgba(231, 29, 54, 0.2) !important;
        border: 1px solid rgba(231, 29, 54, 0.5) !important;
    }
    
    .tab-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .tab {
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        text-align: center;
        flex: 1;
        margin: 0 5px;
    }
    
    .tab:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .tab.active {
        background: var(--highlight);
        color: white;
        box-shadow: 0 4px 10px rgba(233, 69, 96, 0.3);
    }
    
    .score-badge {
        display: inline-block;
        background: var(--highlight);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .history-item {
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
        border-left: 4px solid var(--highlight);
    }
    
    .section-title {
        border-left: 4px solid var(--highlight);
        padding-left: 15px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header">
        <h1>📝 AI Exam Generator</h1>
        <p>Create, attempt, and grade exams - All in one platform</p>
    </div>
""", unsafe_allow_html=True)

# Structured Output Classes
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
    MCQ10:  List[Options] = Field(description="10th MCQ and its options from Given Topic")
    MCQ11:  List[Options] = Field(description="11th MCQ and its options from Given Topic")
    MCQ12:  List[Options] = Field(description="12th MCQ and its options from Given Topic")

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

# Initialize session state
if 'subject' not in st.session_state:
    st.session_state.subject = ""
if 'topic' not in st.session_state:
    st.session_state.topic = ""
if 'mcqs' not in st.session_state:
    st.session_state.mcqs = None
if 'short_questions' not in st.session_state:
    st.session_state.short_questions = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "generate"
if 'current_exam_id' not in st.session_state:
    st.session_state.current_exam_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_answers' not in st.session_state:
    st.session_state.student_answers = {}
if 'grading_complete' not in st.session_state:
    st.session_state.grading_complete = False
if 'show_exam' not in st.session_state:
    st.session_state.show_exam = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


if st.query_params.get("generate") == "one":
    st.session_state.active_tab = "generate"
if st.query_params.get("attempt") == "two":
    st.session_state.active_tab = "attempt"
if st.query_params.get("history") == 3:
    st.session_state.active_tab = "history"
if st.query_params.get("Recommender") == 4:
    st.session_state.active_tab = "Recommender"
    


col1,col2,col3,col4 = st.columns([2,2,2,2])
with col1:
    if st.button("Generate Exam"):
        st.session_state.active_tab = "generate"
        st.rerun()
with col2:
    if st.button("Attempt exam"):
        st.session_state.active_tab = "attempt"
        st.rerun()
with col3:
    if st.button("View History"):
        st.session_state.active_tab = "history"
        st.rerun()
with col4:
    if st.button("Recommender"):
        st.session_state.active_tab = "Recommender"
        st.rerun()

# Generate Exam
if st.session_state.active_tab == "generate":
    with st.container():
        st.markdown("## Create New Exam")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.subject = st.text_input("📚 Subject", st.session_state.subject)
        with col2:
            st.session_state.topic = st.text_input("📖 Topic", st.session_state.topic)
        
        if st.button("✨ Generate Exam", use_container_width=True):
            with st.spinner("Generating exam questions..."):
                try:
                    # Initialize LLM
                    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
                    
                    # Generate MCQs
                    mcq_prompt = f"Create 12 MCQs on {st.session_state.topic} for {st.session_state.subject}. For each question, include the correct answer option number (1-4)."
                    mcq_LLM = llm.with_structured_output(MCQs)
                    st.session_state.mcqs = mcq_LLM.invoke(mcq_prompt)
                    
                    # Generate Short Questions
                    sq_prompt = f"Generate 8 short questions and 2 long questions each with his short and concise Answers on {st.session_state.topic} for {st.session_state.subject}"
                    sq_llm = llm.with_structured_output(Questions)
                    st.session_state.short_questions = sq_llm.invoke(sq_prompt)
                    
                    # Store exam in database
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
                             (exam_data["subject"], 
                              exam_data["topic"], 
                              exam_data["mcqs"], 
                              exam_data["short_questions"], 
                              exam_data["long_questions"]))
                    conn.commit()
                    st.session_state.current_exam_id = c.lastrowid
                    
                    st.success(f"Exam generated and saved! ID: {st.session_state.current_exam_id}")
                    st.session_state.show_exam = True
                    
                except Exception as e:
                    st.error(f"Error generating exam: {str(e)}")
                    st.session_state.mcqs = None
                    st.session_state.short_questions = None
        
        # Generated exam in the same tab
        if st.session_state.mcqs and st.session_state.short_questions and st.session_state.show_exam:
            st.markdown("---")
            st.markdown(f"## Generated Exam: {st.session_state.subject} - {st.session_state.topic}")
            
            # MCQs Display
            st.markdown("### Multiple Choice Questions")
            for i in range(1, 13):
                mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
                st.markdown(f"""
                    <div class="question-card">
                        <b>Q{i}:</b> {mcq.question}
                        <div class="option">1. {mcq.Option1}</div>
                        <div class="option">2. {mcq.Option2}</div>
                        <div class="option">3. {mcq.Option3}</div>
                        <div class="option">4. {mcq.Option4}</div>
                        <div style="margin-top: 10px; color: #e94560;"><b>Correct Answer: {mcq.correct}</b></div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Display Short Questions
            st.markdown("### Short Answer Questions")
            for i in range(1, 9):
                question = getattr(st.session_state.short_questions, f"question{i}")
    
                st.markdown(f"""
                    <div class="question-card">
                        <b>Q{i}:</b> {question}
                    </div>
                """, unsafe_allow_html=True)
                
            # Long Questions
            st.markdown("### Long Answer Questions")
            st.markdown(f"""
                <div class="question-card">
                    <b>A1:</b> {st.session_state.short_questions.LongQuestion1}
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="question-card">
                    <b>Q2:</b> {st.session_state.short_questions.LongQuestion2}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Attempt This Exam", use_container_width=True):
                st.session_state.active_tab = "attempt"
                st.rerun()

# Attempt Exam
if st.session_state.active_tab == "attempt":
    with st.container():
        st.markdown("## Attempt Exam")
        
        # Exams from database
        c.execute("SELECT id, subject, topic FROM exams ORDER BY id DESC")
        exams = c.fetchall()
        
        if not exams:
            st.warning("No exams available. Please generate an exam first.")
            if st.button("Go to Generate Exam"):
                st.session_state.active_tab = "generate"
                st.experimental_rerun()
            st.stop()
        
        # Exam selector
        exam_options = [f"{exam[1]} - {exam[2]} (ID: {exam[0]})" for exam in exams]
        selected_exam = st.selectbox("Select Exam to Attempt", exam_options)
        
        # Exam ID from selection
        exam_id = int(selected_exam.split("(ID: ")[1].replace(")", ""))
        
        # Selected exam
        c.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
        exam_data = c.fetchone()
        
        if exam_data:
            exam_id, subject, topic, created_at, mcqs_json, short_questions_json, long_questions_json = exam_data
            st.session_state.mcqs = MCQs.model_validate_json(mcqs_json)
            st.session_state.short_questions = Questions.model_validate_json(short_questions_json)
            st.session_state.current_exam_id = exam_id
            
            st.info(f"Attempting Exam: {subject} - {topic} (Created: {created_at})")
            
            # Student information
            st.session_state.student_name = st.text_input("👤 Student Name", st.session_state.student_name)
            
            if not st.session_state.student_name:
                st.warning("Please enter your name to start the exam")
                st.stop()
            
            # Exam questions
            st.markdown("### Multiple Choice Questions")
            for i in range(1, 13):
                mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
                
                # Initialize answer if not exists
                if f"mcq_{i}" not in st.session_state.student_answers:
                    st.session_state.student_answers[f"mcq_{i}"] = None
                
                with st.container():
                    st.markdown(f"<div class='question-card'><b>Q{i}:</b> {mcq.question}</div>", unsafe_allow_html=True)
                    
                    # MCQs options
                    options = [mcq.Option1, mcq.Option2, mcq.Option3, mcq.Option4]
                    selected = st.radio(
                        f"Select answer for Q{i}:",
                        options,
                        index=None,
                        key=f"mcq_{i}",
                        horizontal=True
                    )
                    st.session_state.student_answers[f"mcq_{i}"] = options.index(selected) + 1 if selected else None
            
            # Submit button
            if st.button("📝 Submit Exam", use_container_width=True):
                # Calculate score
                score = 0
                total_mcqs = 12
                
                for i in range(1, 13):
                    mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
                    student_answer = st.session_state.student_answers.get(f"mcq_{i}")
                    
                    if student_answer and student_answer == mcq.correct:
                        score += 1
               
                # attempt in database
                attempt_data = {
                    "exam_id": exam_id,
                    "student_name": st.session_state.student_name,
                    "answers": json.dumps(st.session_state.student_answers),
                    "score": score,
                    "total": total_mcqs
                }
                
                c.execute('''INSERT INTO attempts (exam_id, student_name, answers, score, total)
                            VALUES (?, ?, ?, ?, ?)''',
                         (attempt_data["exam_id"], 
                          attempt_data["student_name"], 
                          attempt_data["answers"], 
                          attempt_data["score"], 
                          attempt_data["total"]))
                conn.commit()
                
                st.session_state.grading_complete = True
                st.session_state.attempt_score = score
                st.session_state.attempt_total = total_mcqs
                st.success("Exam submitted successfully! View your results below.")
            
            # results if grading complete
            if st.session_state.grading_complete:
                st.markdown("---")
                st.markdown(f"## Exam Results")
                st.markdown(f"### Score: {st.session_state.attempt_score}/{st.session_state.attempt_total} <span class='score-badge'>{round((st.session_state.attempt_score/st.session_state.attempt_total)*100, 1)}%</span>", 
                            unsafe_allow_html=True)
                
                # correct answers
                st.markdown("### Question Review")
                for i in range(1, 13):
                    mcq = getattr(st.session_state.mcqs, f"MCQ{i}")[0]
                    student_answer = st.session_state.student_answers.get(f"mcq_{i}")
                    is_correct = student_answer == mcq.correct
                    option_class = "correct-answer" if is_correct else "incorrect-answer"
                    
                    st.markdown(f"**Q{i}:** {mcq.question}")
                    
                    # options with highlighting
                    for j in range(1, 5):
                        option_text = mcq.__getattribute__(f'Option{j}')
                        if j == student_answer:
                            st.markdown(f"<div class='option {option_class}'>Your Answer: {j}. {option_text}</div>", 
                                        unsafe_allow_html=True)
                        elif j == mcq.correct:
                            st.markdown(f"<div class='option correct-answer'>Correct Answer: {j}. {option_text}</div>", 
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='option'>{j}. {option_text}</div>", 
                                        unsafe_allow_html=True)
                    
                        st.markdown("---")
                if st.button("View History", use_container_width=True):
                    st.session_state.active_tab = "history"
                    st.rerun()
          

# Exam History 
if st.session_state.active_tab == "history":
    with st.container():
        st.markdown("## Exam History")
        
        # all exams
        c.execute("SELECT * FROM exams ORDER BY id DESC")
        exams = c.fetchall()
        
        if not exams:
            st.info("No exams found in history. Generate an exam to get started.")
            st.stop()
        
        for exam in exams:
            exam_id, subject, topic, created_at, mcqs, short_questions, long_questions = exam
            
            # attempts for this exam
            c.execute("SELECT * FROM attempts WHERE exam_id = ? ORDER BY submitted_at DESC", (exam_id,))
            attempts = c.fetchall()
            
            with st.expander(f"{subject} - {topic} (Created: {created_at})"):
                st.markdown(f"**Exam ID:** {exam_id}")
                st.markdown(f"**Created:** {created_at}")
                st.markdown(f"**Attempts:** {len(attempts)}")
                
                if attempts:
                    st.markdown("### Student Attempts")
                    for attempt in attempts:
                        attempt_id, _, student_name, answers, score, total, submitted_at = attempt
                        
                        st.markdown(f"""
                            <div class="history-item">
                                <h4>{student_name}</h4>
                                <p>Submitted: {submitted_at}</p>
                                <p>Score: {score}/{total} <span class='score-badge'>{round((score/total)*100, 1)}%</span></p>
                            </div>
                        """, unsafe_allow_html=True)
        with st.expander("Clear History"):
                    # Create exam selector
            exam_options = [f"{exam[1]} - {exam[2]} (ID: {exam[0]})" for exam in exams]
            selected_exam = st.selectbox("SELECT EXAM TO DELETE", exam_options)
            
            # Extract exam ID from selection
            exam_id = int(selected_exam.split("(ID: ")[1].replace(")", ""))
            if st.button(f"Delete {selected_exam}"):
                # DELETE selected exam
                c.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
                conn.commit()

# Footer
st.markdown("""
    <div style="text-align: center; padding: 1.5rem; color: #a0a0a0; font-size: 0.9rem; margin-top: 3rem;">
        <p>AI Exam Generator • Create, Attempt, Grade • Powered by Bilal GPT</p>
    </div>
""", unsafe_allow_html=True)

# Close database connection at end
conn.close()

if st.session_state.active_tab == "Recommender":
    st.markdown("""
    <div class="header">
        <h1>📝 Recommendation System</h1>
        <p>Create, attempt, and grade exams - All in one platform</p>
    </div>
    """, unsafe_allow_html=True)
    with st.container():
        st.subheader("⚡Enter Student for Personalized Recomandations")
        col1, col2 = st.columns([3,1], border=True)
        with col1:
            # Database to store Chat
            conn = sqlite3.connect('Chat_history.db', check_same_thread=False)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS chats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT
                        bilalgpt TEXT
                    )''')
            c.execute("PRAGMA table_info(chats);")
            columns = [column[1] for column in c.fetchall()]

            if 'bilalgpt' not in columns:
                c.execute('''ALTER TABLE chats ADD COLUMN bilalgpt TEXT;''')
            conn.commit()

            student = st.text_input("Student name")
            student_data = get_data_by_name(student)
            # Initialize LLM
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")    
            query = st.text_input("Ask me Anything...")

            if st.button("Submit"):
                prompt = f"""You are Recommantion System. These are the stats of the Student:{student_data}
                        According to this student data and stats , provide personalized recomendations to the student.\n
                        also respond to the user query:{query}"""
                response = llm.invoke(prompt)
                c.execute('''INSERT INTO chats (user, bilalgpt)  VALUES (?, ?)''',(query, str(response.content),))
                conn.commit()
                st.markdown(response.content)
        with col2:
            st.subheader("Chat history")
            conn = sqlite3.connect('Chat_history.db', check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM chats")
            chats = c.fetchall()
            colm,colt = st.columns([2,2])
            with colt:
                if st.button("Clear"):
                    c.execute("DELETE FROM chats")
                    conn.commit()

            if chats == None:
                st.warning("Start Conservation!") 
            else:
                for chat in chats:
                    id, user, bilalgpt = chat
                    plan_container = st.container()
                    with plan_container:
                        if st.button(f"Chat {id}", key=f"load_{id}"):
                            st.markdown(f"User:{user}")
                            st.markdown(f"Bilal GPT: {bilalgpt}")
            
               