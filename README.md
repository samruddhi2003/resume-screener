# Smart Resume Screening System

A web app that compares resumes against a job description and tells you how well each candidate matches — with a score, matched skills, missing skills, and an AI chat to answer your questions.

---

## What It Does

1. You paste a job description
2. You upload one or more resumes (PDF or TXT)
3. It gives each resume a **match score out of 100**
4. It shows which skills matched and which are missing
5. You can chat with an AI to ask things like *"Why is this score low?"* or *"Who is the best candidate?"*

---

## How the Score Works

The score is a mix of two things:

| What | Weight | How |
|---|---|---|
| Skill match | 60% | How many skills from the JD appear in the resume |
| Text similarity | 40% | How similar the overall text is (using TF-IDF) |

So if a resume matches 4 out of 5 required skills, it starts with a strong base score.

**Score colors:**
- 🟢 Green — 60% and above (strong match)
- 🟡 Amber — 35% to 59% (partial match)
- 🔴 Red — below 35% (weak match)

---

## Tools Used

| Tool | What it does |
|---|---|
| **FastAPI** | Runs the backend server and API |
| **pdfplumber** | Reads text out of PDF resumes |
| **scikit-learn** | Calculates text similarity score (TF-IDF) |
| **Regex** | Finds skills and experience in resume text |
| **Groq (LLaMA 3.3 70B)** | Powers the AI chat feature |
| **python-dotenv** | Loads the API key from the `.env` file |
| **HTML/CSS/JS** | The frontend UI (no React, no build step needed) |
| **uvicorn** | Runs the FastAPI app locally |

---

## Project Files

```
resume screening/
├── main.py            → starts the server, defines all endpoints
├── resume_parser.py   → reads PDFs/TXTs, finds skills and experience
├── matcher.py         → calculates the match score and explanation
├── chat.py            → sends questions to the Groq AI and returns answers
├── requirements.txt   → list of packages to install
├── .env               → your Groq API key (never share this)
├── .gitignore         → files to exclude from GitHub
├── README.md
└── static/
    └── index.html     → the frontend UI
```

---

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Add your Groq API key**

Get a free key at https://console.groq.com, then open `.env` and replace the placeholder:
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
| POST | `/chat` | Asks the AI a question about the results |

---

## Limitations

- Only detects skills from a fixed list of ~50 keywords — "ReactJS" won't match "react"
- Experience is guessed from patterns like "3 years of experience" — unusual formats may be missed
- Not fully semantic — "Developer" and "Engineer" won't match even if they mean the same thing
