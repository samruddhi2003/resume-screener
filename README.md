# Smart Resume Screening AI Agent

A web app that screens resumes against a job description using an AI agent — giving each candidate a match score, skill analysis, AI summary, and a chat interface with conversation memory.

---

## What It Does

1. You paste a job description
2. You upload one or more resumes (PDF or TXT)
3. An AI agent screens each resume and returns:
   - A **match score out of 100**
   - **Matched** and **missing** skills
   - An AI-generated **candidate summary** with strengths, weaknesses, and a recommendation (Interview / Maybe / Reject)
4. You can **chat** with the AI to ask follow-up questions — it remembers the conversation history

---

## How the Score Works

| What | Weight | How |
|---|---|---|
| Skill match | 60% | How many skills from the JD appear in the resume |
| Text similarity | 40% | TF-IDF cosine similarity between JD and resume text |

**Score colors:**
- 🟢 Green — 60% and above (strong match)
- 🟡 Amber — 35% to 59% (partial match)
- 🔴 Red — below 35% (weak match)

---

## Tools Used

| Tool | What it does |
|---|---|
| **FastAPI** | Backend server and API endpoints |
| **pdfplumber** | Extracts text from PDF resumes |
| **scikit-learn** | TF-IDF text similarity scoring |
| **Regex** | Skill and experience extraction |
| **LangChain + LangGraph** | AI agent with tool calling (`create_react_agent`) |
| **langchain-groq** | Connects LangChain to Groq's LLaMA model |
| **Groq (LLaMA 3.3 70B)** | Powers chat, candidate summary, and explanations |
| **python-dotenv** | Loads API key from `.env` |
| **HTML/CSS/JS** | Frontend UI (no framework, mobile-friendly) |
| **uvicorn** | Runs the FastAPI app locally |

---

## Project Files

```
resume screening/
├── main.py            → FastAPI server, defines /screen and /chat endpoints
├── agent.py           → LangGraph AI agent with 3 tools (parse, match, explain)
├── agent_memory.py    → Stores conversation history for chat context
├── resume_parser.py   → Reads PDFs/TXTs, extracts skills and experience
├── matcher.py         → Calculates match score (TF-IDF + skill match)
├── chat.py            → AI chat with memory + candidate summary generation
├── requirements.txt   → Python dependencies
├── render.yaml        → Render deployment config
├── .env               → Your Groq API key (never share this)
├── .gitignore         → Files excluded from GitHub
├── README.md
└── static/
    └── index.html     → Frontend UI
```

---

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Add your Groq API key**

Get a free key at https://console.groq.com, then open `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

**3. Run the app**
```bash
uvicorn main:app --reload
```

**4. Open in browser**
```
http://127.0.0.1:8000
```

---

## API Endpoints

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/` | Opens the UI |
| POST | `/screen` | Screens resumes against a job description |
| POST | `/chat` | Asks the AI a question with conversation memory |

---

## Deployment

Deployed on **Render**: https://resume-screener-9fg9.onrender.com

> Note: Free tier spins down after inactivity — first request may take ~30 seconds.

---

## Limitations

- Detects skills from a fixed list of ~50 keywords — variations like "ReactJS" won't match "react"
- Experience extracted from patterns like "3 years of experience" — unusual formats may be missed
- Not fully semantic — "Developer" and "Engineer" won't match even if they mean the same thing
- Conversation memory is in-memory only — resets when the server restarts
