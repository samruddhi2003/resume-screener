import os

from dotenv import load_dotenv
from groq import Groq

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from resume_parser import parse_resume
from matcher import match_resume
from chat import ask_llm

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# ---------------- TOOLS ---------------- #

@tool
def parse_resume_tool(file_path: str):
    """Parse a resume and extract text, skills and experience."""
    return parse_resume(file_path)


@tool
def match_resume_tool(job_description: str, resume: dict):
    """Compare resume against job description."""
    return match_resume(job_description, resume)


@tool
def explain_tool(question: str, results: list):
    """Answer questions about resume screening."""
    return ask_llm(question, results)


tools = [
    parse_resume_tool,
    match_resume_tool,
    explain_tool
]

agent_executor = create_react_agent(
    llm,
    tools,
    prompt="You are an AI Resume Screening Agent. You have access to three tools: Parse Resume, Match Resume, and Explain Screening Results. Always use the appropriate tool before answering."
)


class ResumeScreeningAgent:

    def screen_resume(self, file_path, jd):

        parsed = parse_resume_tool.invoke(
            {"file_path": file_path}
        )

        result = match_resume_tool.invoke(
            {
                "job_description": jd,
                "resume": parsed
            }
        )

        return result

    def explain(self, question, results):

        return explain_tool.invoke(
            {
                "question": question,
                "results": results
            }
        )