# 📚 Examini — AI-Powered Learning Platform

> *Study smarter. Learn faster. Perform better.*

Examini is an AI-powered educational platform that generates personalized study plans, creates intelligent exams, and adapts recommendations to every student's progress — all in one place.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Bilal-Ahmad-5/Examini.git
cd examini

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

Add your API keys to `.env`:

```
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

> Get your keys: [Google Gemini](https://makersuite.google.com/app/apikey) · [Groq](https://console.groq.com)

Then launch the app:

```bash
streamlit run main.py
```

---

## ✨ What It Does

### 📅 AI Lesson Planner
*Build a study schedule that fits your life*

- Generate weekly or monthly study plans tailored to your goals
- Choose your level — Beginner, Intermediate, or Advanced
- Set your subject, topic, and daily study hours
- Track your progress visually as you go

### 📝 AI Exam Generator
*Practice smarter with AI-crafted questions*

- Auto-generate MCQs, short answer, and essay questions on any topic
- Get instant grading and detailed feedback after each attempt
- Review your exam history to spot strengths and weaknesses
- Track improvement across multiple attempts

### ✅ AI Exam Checker & Grading
*Instant, intelligent evaluation of every answer*

- Submit completed exams and get **automated grading in seconds**
- AI evaluates MCQs, short answers, and essays with context-aware scoring
- Receive **detailed feedback per question** — not just a score, but why
- Get a **performance breakdown** showing strong topics vs areas to revisit
- All results saved to exam history for progress tracking over time

### 🎯 Personalized Recommendations
*An AI tutor that knows your progress*

- Chat with an AI tutor for customized learning advice
- Get recommendations based on your actual exam performance
- Save and revisit past learning conversations
- Adaptive learning paths that evolve as you improve

---

## 💡 How to Use

| Module | Steps |
|--------|-------|
| 📅 **Lesson Planner** | Select subject → Set duration → Set daily hours → Generate plan |
| 📝 **Exam Generator** | Choose topic → Generate exam → Attempt it → Submit answers |
| ✅ **Exam Checker** | AI grades your answers → Feedback per question → Saved to history |
| 🎯 **Recommendations** | Enter your name → View history → Chat with AI tutor |

---

## 🧰 Tech Stack

| Layer | Tools |
|-------|-------|
| **LLMs** | Google Gemini Flash 1.5 · Groq (Llama 3) |
| **Framework** | Streamlit · LangChain · Pydantic |
| **Database** | SQLite |
| **APIs** | Google Gemini · Tavily Search |

---

## 📂 Project Structure

```
examini/
├── main.py               # App entry point
├── Plan_Lesson.py         # Lesson planning module
├── Generate_Exam.py       # Exam generation module
├── Recomandation.py       # Recommendation system
├── study_plans.db         # Study plan storage
├── exam_history.db        # Exam history storage
├── requirements.txt
└── .env.example
```

---

## 🤝 Contributing

Fork it, improve it, open a pull request. Ideas for new subjects, question types, or UI improvements are all welcome.

---

## 📄 License

MIT — free to use and build upon.

---

*Every student deserves a personalized path to success. Examini helps build it.*
