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


st.markdown("""
        <div class="header">
        <h1>📝 Recommendation System</h1>
        <p>Create, attempt, and grade exams - All in one platform</p>
    </div>
    """, unsafe_allow_html=True)

if 'Response' not in st.session_state:
    st.session_state.Response = ""


def get_data_by_name(student):
    conn = sqlite3.connect('exam_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''SELECT * FROM attempts WHERE student_name = ?''', (student,))
    data = c.fetchall()
    conn.close()
    return data


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
            st.session_state.Response = response.content
            st.markdown(st.session_state.Response)
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
                        st.session_state.Response = f"User:{user} \n Output:{bilalgpt}"
                        st.markdown(st.session_state.Response)
                        
            
               