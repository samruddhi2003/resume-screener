import os
import shutil
import tempfile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import ResumeScreeningAgent
from resume_parser import parse_resume
from chat import ask_llm, summarize_candidate

app = FastAPI(title="Smart Resume Screening AI Agent")

agent = ResumeScreeningAgent()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/screen")
async def screen_resumes(
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
):

    results = []

    with tempfile.TemporaryDirectory() as tmpdir:

        for resume_file in resumes:

            dest = os.path.join(tmpdir, resume_file.filename)

            with open(dest, "wb") as f:
                shutil.copyfileobj(resume_file.file, f)

            # Parse resume
            parsed = parse_resume(dest)

            # Agent performs resume screening
            result = agent.screen_resume(dest, job_description)

            # AI Summary
            summary = summarize_candidate(result)

            results.append(
                {
                    "filename": resume_file.filename,
                    **result,
                    "summary": summary,
                }
            )

    results.sort(key=lambda x: x["score"], reverse=True)

    return {"results": results}


class ChatRequest(BaseModel):
    question: str
    results: list


@app.post("/chat")
def chat(req: ChatRequest):

    answer = agent.explain(req.question, req.results)

    return {
        "answer": answer
    }