import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def build_context(results: list) -> str:
    lines = []
    for r in results:
        lines.append(
            f"- {r['filename']}: score={r['score']}%, "
            f"matched={r['matched_skills']}, missing={r['missing_skills']}, "
            f"explanation={r['explanation']}"
        )
    return "\n".join(lines)

def ask_llm(question: str, results: list) -> str:
    context = build_context(results)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a resume screening assistant. Answer questions clearly and concisely based only on the screening results provided."
            },
            {
                "role": "user",
                "content": f"Screening results:\n{context}\n\nQuestion: {question}"
            }
        ],
        max_tokens=512,
    )
    return response.choices[0].message.content
