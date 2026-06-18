from langchain.tools import tool

from resume_parser import parse_resume
from matcher import match_resume
from chat import ask_llm


@tool
def parse_resume_tool(file_path: str):
    """Parse a resume and extract text, skills, and experience."""
    return parse_resume(file_path)


@tool
def match_resume_tool(job_description: str, resume: dict):
    """Match a parsed resume with the job description."""
    return match_resume(job_description, resume)


@tool
def explain_results_tool(question: str, results: list):
    """Generate AI explanation using Groq."""
    return ask_llm(question, results)