from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_skills

def match_resume(jd_text: str, resume: dict) -> dict:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([jd_text, resume["text"]])
    tfidf_score = float(cosine_similarity(tfidf[0], tfidf[1])[0][0])

    jd_skills = set(extract_skills(jd_text))
    resume_skills = set(resume["skills"])
    matched = sorted(jd_skills & resume_skills)
    missing = sorted(jd_skills - resume_skills)

    skill_score = (len(matched) / len(jd_skills)) if jd_skills else 0

    # 40% TF-IDF + 60% skill match for a more realistic score
    score = round((0.4 * tfidf_score + 0.6 * skill_score) * 100, 2)
    exp_note = f"Candidate has {resume['experience']} of experience." if resume["experience"] and resume["experience"] != "fresher" else ("Candidate is a fresher." if resume["experience"] == "fresher" else "Experience not mentioned.")
    match_note = f"Matched {len(matched)}/{len(jd_skills)} required skills." if jd_skills else "No specific skills detected in JD."
    missing_note = f"Missing: {', '.join(missing)}." if missing else "No key skills missing."

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": f"{exp_note} {match_note} {missing_note}",
    }
