import re
import pdfplumber

SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "redis",
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "git", "ci/cd", "linux", "rest", "graphql", "kafka", "spark",
    "html", "css", "bash", "scala", "r", "matlab",
]

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    return [skill for skill in SKILL_KEYWORDS if re.search(rf"\b{re.escape(skill)}\b", text_lower)]

def extract_experience(text: str) -> str | None:
    patterns = [
        r"(\d+)\+?\s*years?\s*(of\s*)?(experience|exp|work)",   # 3 years of experience
        r"experience\s*(of\s*)?(\d+)\+?\s*years?",              # experience of 2 years
        r"(\d+)\+?\s*months?\s*(of\s*)?(experience|exp)",       # 6 months experience
        r"(\d{4})\s*[-–]\s*(\d{4}|present|current)",            # 2019 - 2023 / present
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if "months" in pattern:
                return f"{match.group(1)} months"
            if r"\d{4}" in pattern:
                start, end = match.group(1), match.group(2)
                if end.lower() in ("present", "current"):
                    years = 2025 - int(start)
                else:
                    years = int(end) - int(start)
                if years > 0:
                    return f"{years} years"
            return f"{match.group(1)} years"
    if re.search(r"\b(fresher|entry.?level|no experience)\b", text, re.IGNORECASE):
        return "fresher"
    return None

def parse_resume(file_path: str) -> dict:
    text = extract_text(file_path)
    return {
        "text": text,
        "skills": extract_skills(text),
        "experience": extract_experience(text),
    }
