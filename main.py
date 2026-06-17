import os
import shutil
import tempfile
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from resume_parser import parse_resume
from matcher import match_resume
from chat import ask_llm

app = FastAPI(title="Smart Resume Screener")
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

            parsed = parse_resume(dest)
            result = match_resume(job_description, parsed)
            results.append({"filename": resume_file.filename, **result})

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results}

class ChatRequest(BaseModel):
    question: str
    results: list

@app.post("/chat")
def chat(req: ChatRequest):
    answer = ask_llm(req.question, req.results)
    return {"answer": answer}
