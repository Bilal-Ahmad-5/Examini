# 📚 Examini - AI-Powered Learning Platform

Examini is an innovative AI-powered educational platform that revolutionizes learning through personalized study plans, intelligent exam generation, and adaptive recommendations. Built with cutting-edge AI technologies, Examini helps students optimize their study process while providing educators with powerful tools for content creation.

## ✨ Key Features

### 📅 AI Lesson Planner
- **Personalized Study Plans**: Generate weekly or monthly study schedules tailored to your learning goals
- **Adaptive Difficulty**: Beginner, Intermediate, and Advanced levels
- **Progress Tracking**: Visualize your learning journey with intuitive interfaces
- **Resource Integration**: Includes practical exercises and learning resources

### 📝 AI Exam Generator
- **Smart Question Creation**: Automatically generate MCQs, short answer, and essay questions
- **Auto-Grading System**: Instant scoring and feedback on exam attempts
- **Performance Analytics**: Detailed breakdown of strengths and weaknesses
- **Exam History**: Track progress across multiple attempts

### 🎯 Personalized Recommendations
- **AI Tutor Assistant**: Get customized learning recommendations
- **Performance Analysis**: Insights based on exam history
- **Chat History**: Save and review past learning interactions
- **Adaptive Learning Paths**: Content adjusts to your progress

## 🚀 Technology Stack

- **AI Models**:
  - Google Gemini Flash 1.5
  - Groq API (Llama 3)
  
- **Frameworks**:
  - Streamlit (Frontend)
  - LangChain (AI Orchestration)
  - Pydantic (Structured Outputs)
  
- **Database**:
  - SQLite (Data Storage)
  
- **APIs & Tools**:
  - Google Gemino Api (LLM Integration)
  - Tavily Search Api (Resource Integration)
  - Dotenv (Environment Management)

## 🛠️ Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Bilal-Ahmad-5/Examini.git
cd examini
Install dependencies:

bash
pip install -r requirements.txt
Set up environment variables:

bash
cp .env.example .env
Add your API keys to the .env file:

env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
Run the application:

bash
streamlit run Home.py


📋 Usage Guide
Lesson Planning:

Select subject and topic

Choose duration (1 week/1 month)

Set daily study hours

Generate personalized study plan

Exam Generation:

Create exams by subject/topic

Attempt generated exams

Get instant grading and feedback

Review exam history

Recommendations:

Enter student name to view performance history

Chat with AI tutor for personalized advice

Save and review learning conversations

📂 Project Structure
text
examini/
├── Home.py                 # Main application entry point
├── Plan_Lesson.py          # Lesson planning module
├── Generate_Exam.py        # Exam generation module
├── Recomandation.py        # Recommendation system
├── requirements.txt        # Dependencies
├── .env.example         # Environment template
├── study_plans.db          # Database for study plans
├── exam_history.db         # Database for exam history
└── README.md

📜 License
Distributed under the MIT License. See LICENSE for more information.

✉️ Contact
