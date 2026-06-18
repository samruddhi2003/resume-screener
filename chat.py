import os
from groq import Groq
from agent_memory import add_interaction, get_history
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def build_context(results: list) -> str:
    lines = []

    for r in results:
        lines.append(
            f"""
Candidate: {r['filename']}

Score: {r['score']}

Matched Skills:
{", ".join(r["matched_skills"])}

Missing Skills:
{", ".join(r["missing_skills"])}

Explanation:
{r["explanation"]}
"""
        )

    return "\n".join(lines)


def ask_llm(question: str, results: list):

    context = build_context(results)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                """
You are an AI Resume Screening Agent.

You help HR teams evaluate candidates.

When answering:

- Compare candidates
- Explain scores
- Mention strengths
- Mention weaknesses
- Recommend Interview / Reject
- Keep answers professional.
"""
            },
            {
                "role": "user",
                "content":
                f"""
Conversation History

{get_history()}

Resume Results

{context}

Question:

{question}
"""
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    answer = response.choices[0].message.content

    add_interaction(question, answer)

    return answer


def summarize_candidate(result):

    prompt = f"""
You are an HR Resume Screening AI.

Analyze this candidate.

Score:
{result['score']}

Matched Skills:
{result['matched_skills']}

Missing Skills:
{result['missing_skills']}

Explanation:
{result['explanation']}

Return ONLY in this format.

Candidate Summary:
...

Strengths:
- ...

Weaknesses:
- ...

Recommendation:
Interview / Maybe / Reject
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content