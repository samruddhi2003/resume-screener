# Smart Resume Screening System (AI-Powered)

Screens multiple resumes against a job description and returns a relevance score, matched/missing skills, and a short explanation for each candidate. Includes an LLM-powered chat to answer questions about the results.

---

## Tech Stack

### 1. FastAPI — Web Framework
**Why:** FastAPI builds the REST API endpoints. Chosen because:
- Natively supports file uploads (`UploadFile`) and form fields in the same request
- Async-ready for handling multiple resume uploads without blocking
- Auto-generates interactive API docs at `/docs` with zero config
- Serves the static frontend UI directly via `StaticFiles`

### 2. pdfplumber — PDF Text Extraction
**Why:** Resumes are commonly submitted as PDFs. `pdfplumber` extracts raw text from each page. Chosen over `PyPDF2` because it handles complex layouts (tables, columns) more reliably — important since resumes vary wildly in formatting.

### 3. scikit-learn (TF-IDF + Cosine Similarity) — Scoring Engine
**Why:** Core of the text-based matching. Two steps:
- **TF-IDF:** Converts JD and resume text into numerical vectors. Domain-specific terms like "Kubernetes" or "FastAPI" get higher weight than common words.
- **Cosine Similarity:** Measures angle between the two vectors. Contributes 40% of the final score.

### 4. Hybrid Scoring — Skill Match Ratio
**Why:** Pure TF-IDF gives low scores because resumes and JDs use different vocabulary even when skills match. The final score is a weighted blend:
- **60% skill match ratio** — `matched_skills / jd_skills`
- **40% TF-IDF cosine similarity** — overall text overlap

This produces fair, realistic scores instead of always showing 15–30%.

### 5. Regex — Skill Extraction & Experience Parsing
**Why:** Two regex-based extractors run on every resume:
- **Skill extraction:** Scans for whole-word matches against a curated list of ~50 tech keywords using `\b` word boundaries.
- **Experience extraction:** Handles multiple formats:
  - `"3 years of experience"` / `"5+ years exp"`
  - `"experience of 2 years"`
  - `"6 months experience"`
  - `"2019 - 2023"` or `"2021 - present"` (calculates years automatically)
  - `"fresher"` / `"entry level"`

### 6. Groq (LLaMA 3.3 70B) — LLM Chat
**Why:** After screening, a chat interface lets users ask natural language questions about the results — e.g. "Why is resume1.pdf score low?" or "Who is the best candidate?". Groq was chosen because:
- Free tier with fast inference
- No GPU or local model required
- `llama-3.3-70b-versatile` is capable, up-to-date, and supported

The LLM receives the screening results as context and answers only based on that data.

### 7. python-dotenv — Environment Variables
**Why:** Loads the `GROQ_API_KEY` from a `.env` file so secrets are never hardcoded in source code or pushed to GitHub.

### 8. python-multipart — Form Data Parsing
**Why:** FastAPI requires this to parse `multipart/form-data` requests — the format used when submitting text fields and file uploads together in the same HTTP request.

### 9. HTML/CSS/Vanilla JS — Frontend UI
**Why:** A single static `index.html` served directly by FastAPI — no React, no build step. Features:
- Drag & drop or browse file upload with removable file tags
- Color-coded score bar per candidate (🟢 ≥60% / 🟡 ≥35% / 🔴 <35%)
- Matched and missing skill badges
- LLM chat panel that appears after screening
- Enter key support for chat input

### 10. uvicorn — ASGI Server
**Why:** FastAPI is an ASGI framework and needs an ASGI-compatible server. `uvicorn` is the standard lightweight choice — `--reload` enables hot-reloading during development.

---

## Project Structure

```
resume screening/
├── main.py            # FastAPI app, /screen and /chat endpoints, static file serving
├── resume_parser.py   # PDF/TXT text extraction, skill & experience parsing
├── matcher.py         # Hybrid TF-IDF + skill ratio scoring, explanation generation
├── chat.py            # Groq LLM integration for Q&A on screening results
├── requirements.txt   # All dependencies
├── .env               # GROQ_API_KEY (never commit this)
├── .gitignore
├── README.md
└── static/
    └── index.html     # Frontend UI
```

---

## Setup

```bash
pip install -r requirements.txt
```

Add your Groq API key to `.env` (get one free at https://console.groq.com):
```
GROQ_API_KEY=your_groq_api_key_here
```

## Run

```bash
uvicorn main:app --reload
```

- UI: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### `GET /`
Serves the frontend UI.

### `POST /screen`

| Field | Type | Description |
|---|---|---|
| `job_description` | `string` | Full text of the job description |
| `resumes` | `file(s)` | One or more resume files (`.pdf` or `.txt`) |

**Example Response:**
```json
{
  "results": [
    {
      "filename": "resume1.pdf",
      "score": 72.45,
      "matched_skills": ["aws", "docker", "fastapi", "python"],
      "missing_skills": [],
      "explanation": "Candidate has 3 years of experience. Matched 4/4 required skills. No key skills missing."
    },
    {
      "filename": "resume2.txt",
      "score": 31.10,
      "matched_skills": ["python"],
      "missing_skills": ["aws", "docker", "fastapi"],
      "explanation": "Candidate is a fresher. Matched 1/4 required skills. Missing: aws, docker, fastapi."
    }
  ]
}
```

Results are sorted by score descending.

### `POST /chat`

| Field | Type | Description |
|---|---|---|
| `question` | `string` | Natural language question about the results |
| `results` | `array` | The results array returned by `/screen` |

**Example Response:**
```json
{
  "answer": "resume2.txt has a low score because it only matched 1 out of 4 required skills. The candidate is missing aws, docker, and fastapi which are core requirements in the job description."
}
```

---

## Known Limitations

- **Not fully semantic:** TF-IDF is keyword-based. "Software Engineer" and "Developer" won't match even if they mean the same thing.
- **Fixed skill list:** Only skills in the hardcoded keyword list in `resume_parser.py` are detected. "ReactJS" won't match "react".
- **Simple experience parsing:** Infers experience from common patterns and date ranges but won't catch all resume formats.
