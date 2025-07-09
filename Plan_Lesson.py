import streamlit as st
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field 
import os
import sqlite3  # Added for database storage
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
    day13: str = Field(description="Plan for day therteen and also adding some details to start learning")
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


# class Study_plan2(BaseModel):
#     # Next 14 days

# --- UI Configuration ---
st.set_page_config(
    page_title="AI Lesson Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling
st.markdown("""
    <style>
    :root {
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #0f3460;
        --highlight: #e94560;
        --text: #f1f1f1;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: var(--text);
    }
    
    .stChatInput {
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: var(--highlight) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--highlight);
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--highlight) !important;
        border-bottom: 2px solid var(--highlight);
        padding-bottom: 10px;
    }
    
    .stAudio {
        width: 100%;
        margin-top: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
    }
    
    .message-user {
        background: rgba(15, 52, 96, 0.5) !important;
        border-radius: 15px 15px 0 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .message-assistant {
        background: rgba(233, 69, 96, 0.2) !important;
        border-radius: 15px 15px 15px 0;
        padding: 15px;
        margin: 10px 0;
    }
    
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, var(--accent), var(--highlight));
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: var(--secondary) !important;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)



# --- Header Section ---
st.markdown("""
    <div class="header">
        <h1>📚 AI Lesson Planner</h1>
        <p>Generate personalized study plans for any topic with AI-powered scheduling</p>
    </div>
""", unsafe_allow_html=True)

# --- Main Content ---
with st.container():
        st.markdown("""
            <div class="card">
                <h2>⚙️ Configuration</h2>
                <p>Customize your learning plan</p>
            </div>
        """, unsafe_allow_html=True)
        
        # User Inputs
        with st.form("config_form"):
            topic = st.text_input("📖 Enter Learning Topic")
            subject = st.text_input("📖 Enter Subject")
            daily_hours = st.text_input("📖 Enter Daily Hours ")
            st.divider()
            plan_type = st.radio("⏱️ Plan Duration", ["One Week", "One Month"])
            st.divider()
            difficulty = st.select_slider("📈 Difficulty Level", 
                                         options=["Beginner", "Intermediate", "Advanced"])
            submit_button = st.form_submit_button("✨ Generate Study Plan")
           
        if submit_button:
            with st.spinner("🧠 Creating your personalized study plan..."):
                try:
                    # Generate plan based on selection
                    if plan_type == "One Week":
                        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
                        structured_llm = llm.with_structured_output(Study_plan_for_week)
                        prompt = f"""
                        Create a {difficulty.lower()} study plan for one week(7 days) on TOPIC: {topic} OF SUBJECT:{subject}
                        - Each day should have: title, topics, resources, exercises
                        - Daily study time: {daily_hours} hours
                        - Include practical exercises.
                        """
                        response = structured_llm.invoke(prompt)
                        
                    else:  # One Month plan
                        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
                        structured_llm1 = llm.with_structured_output(Study_plan)
                        prompt1= f"""
                        Create a {difficulty.lower()} study plan for one month on Topic: {topic} of Subject:{subject}.\n
                        - Each day should have: title, topics, resources, exercises
                        - Daily study time: {daily_hours} hours
                        - Include practical exercises
                        """
                        response = structured_llm1.invoke(prompt1)
                    
                except Exception as e:
                    st.error(f"⚠️ Error generating plan: {str(e)}")
        
        else:
            st.markdown("""
                <div style="text-align: center; padding: 4rem 0;">
                    <h3>No Plan</h3>
                    <p>Select options and click "Generate Study Plan" to get started</p>
                </div>
            """, unsafe_allow_html=True)
        st.divider()

# Database Setup
def init_db():
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 topic TEXT,
                 subject TEXT,
                 daily_hours TEXT,
                 plan_type TEXT,
                 difficulty TEXT,
                 plan_data TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_plan(topic, subject, daily_hours, plan_type, difficulty, plan_data):
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''INSERT INTO plans 
                 (topic, subject, daily_hours, plan_type, difficulty, plan_data) 
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (topic, subject, daily_hours, plan_type, difficulty, json.dumps(plan_data)))
    conn.commit()
    conn.close()

def get_plan_history():
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''SELECT id, topic, subject, plan_type, created_at 
                 FROM plans ORDER BY created_at DESC''')
    history = c.fetchall()
    conn.close()
    return history

def get_plan_by_id(plan_id):
    conn = sqlite3.connect('study_plans.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM plans WHERE id = ?''', (plan_id,))
    plan = c.fetchone()
    conn.close()
    return plan

# Initialize database
init_db()


# Inside your col2 where you generate plans:
if submit_button:
    with st.spinner("Saving your personalized study plan..."):
        try:
            if plan_type == "One Week":
                plan_data = {
                    'day1': response.day1,
                    'day2': response.day2,
                    'day3': response.day3,
                    'day4': response.day4,
                    'day5': response.day5,
                    'day6': response.day6,
                    'day7': response.day7
                }
            else:  # One Month
                plan_data = {f'day{i}': getattr(response, f'day{i}') for i in range(1, 29)}
            
            save_plan(topic, subject, daily_hours, plan_type, difficulty, plan_data)
            
            # Store in session state for immediate display
            st.session_state.current_plan = {
                'topic': topic,
                'subject': subject,
                'daily_hours': daily_hours,
                'plan_type': plan_type,
                'difficulty': difficulty,
                'plan_data': plan_data
            }
            
            st.success("🎉 Your study plan is ready! Time to start learning!")
            
        except Exception as e:
            st.error(f"⚠️ Error generating plan: {str(e)}")
            

# Define callback functions outside the loop
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
    
    # Empty the container to remove the plan UI immediately
    container.empty()

with st.sidebar:
    st.header("📚 Study Plans ")
    history = get_plan_history()
    if not history:
        st.info("No saved plans yet. Generate a plan to see history.")
    else:
        for plan in history:
            # UNPACK VALUES IMMEDIATELY
            plan_id, topic, subject, plan_type, created_at = plan
            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%b %d, %Y %H:%M")
            
            # Create unique container for each plan
            plan_container = st.container()
            with plan_container:
                cols = st.columns([4, 1])
                
                with cols[0]:
                    # Use a lambda with captured values to handle clicks
                    st.button(
                        f"{topic} - {subject} ({dt.strftime('%b %d, %Y %H:%M')})",
                        key=f"load_{plan_id}",
                        on_click=load_plan_callback,  # Use callback function
                        args=(plan_id,)  # Pass plan_id as argument
                    )
                
                with cols[1]:
                    st.button(
                        "⛔", 
                        key=f"del_{plan_id}",
                        on_click=delete_plan_callback,  # Use callback function
                        args=(plan_id, plan_container)  # Pass plan_id and container
                    )


# Display current plan from session state
if 'current_plan' in st.session_state:
    plan = st.session_state.current_plan
    plan_type = plan['plan_type']
    plan_data = plan['plan_data']
    
    # Display week plan
    if plan_type == "One Week":
        days = {
            "Monday": plan_data['day1'],
            "Tuesday": plan_data['day2'],
            "Wednesday": plan_data['day3'],
            "Thursday": plan_data['day4'],
            "Friday": plan_data['day5'],
            "Saturday": plan_data['day6'],
            "Sunday": plan_data['day7']
        }
        
        for day, plan_text in days.items():
            with st.expander(f"📅 {day}", expanded=True):
                st.markdown(f"""
                    <div class="plan-card">
                        <h4>{day}'s Plan</h4>
                        <p>{plan_text}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Display month plan
    elif plan_type == "One Month":
        tab1, tab2, tab3, tab4 = st.tabs(["Week 1", "Week 2", "Week 3", "Week 4"])
        
        with tab1:
            days = {
                "Monday": plan_data['day1'],
                "Tuesday": plan_data['day2'],
                "Wednesday": plan_data['day3'],
                "Thursday": plan_data['day4'],
                "Friday": plan_data['day5'],
                "Saturday": plan_data['day6'],
                "Sunday": plan_data['day7']
            }
            for day, plan_text in days.items():
                with st.expander(f"📅 {day}", expanded=True):
                    st.markdown(f"""
                        <div class="plan-card">
                            <h4>{day}'s Plan</h4>
                            <p>{plan_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            days = {
                "Monday": plan_data['day8'],
                "Tuesday": plan_data['day9'],
                "Wednesday": plan_data['day10'],
                "Thursday": plan_data['day11'],
                "Friday": plan_data['day12'],
                "Saturday": plan_data['day13'],
                "Sunday": plan_data['day14']
            }
            for day, plan_text in days.items():
                with st.expander(f"📅 {day}", expanded=True):
                    st.markdown(f"""
                        <div class="plan-card">
                            <h4>{day}'s Plan</h4>
                            <p>{plan_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            days = {
                "Monday": plan_data['day15'],
                "Tuesday": plan_data['day16'],
                "Wednesday": plan_data['day17'],
                "Thursday": plan_data['day18'],
                "Friday": plan_data['day19'],
                "Saturday": plan_data['day20'],
                "Sunday": plan_data['day21']
            }
            for day, plan_text in days.items():
                with st.expander(f"📅 {day}", expanded=True):
                    st.markdown(f"""
                        <div class="plan-card">
                            <h4>{day}'s Plan</h4>
                            <p>{plan_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            days = {
                "Monday": plan_data['day22'],
                "Tuesday": plan_data['day23'],
                "Wednesday": plan_data['day24'],
                "Thursday": plan_data['day25'],
                "Friday": plan_data['day26'],
                "Saturday": plan_data['day27'],
                "Sunday": plan_data['day28']
            }
            for day, plan_text in days.items():
                with st.expander(f"📅 {day}", expanded=True):
                    st.markdown(f"""
                        <div class="plan-card">
                            <h4>{day}'s Plan</h4>
                            <p>{plan_text}</p>
                        </div>
                    """, unsafe_allow_html=True)

st.divider()
# Features Section
st.markdown("""
    <div class="card">
        <h3>🚀 Features</h3>
        <div class="st-columns" style="display: flex; gap: 1.5rem;">
            <div style="flex: 1;">
                <h4>🎯 Personalized Plans</h4>
                <p>AI creates customized learning paths based on your topic and skill level</p>
            </div>
            <div style="flex: 1;">
                <h4>⏱️ Flexible Duration</h4>
                <p>Choose between 1-week intensive or 1-month comprehensive plans</p>
            </div>
            <div style="flex: 1;">
                <h4>📈 Progress Tracking</h4>
                <p>Visualize your learning journey with our intuitive interface</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class="footer">
        <p>AI Lesson Planner • Built with Streamlit and Google Gemini • Your smart learning companion</p>
    </div>
""", unsafe_allow_html=True)
