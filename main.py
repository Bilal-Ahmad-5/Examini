import streamlit as st
import datetime

# set home

# Page configuration
st.set_page_config(
    page_title="AI Tuitor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Examini",)

pg = st.navigation({"🤖 Examini":
                    [st.Page("Plan_Lesson.py"),
                    st.Page("Generate_Exam.py")]
                })
pg.run()
