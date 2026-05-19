from fastapi import FastAPI, UploadFile, File
from resume_parser import parse_resume
from job_matcher import find_jobs, export_excel
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = parse_resume(file_path)

    skills = parsed["skills"]

    jobs = find_jobs(skills)

    excel_path = export_excel(jobs)

    return {
        "skills_detected": skills,
        "total_jobs": len(jobs),
        "excel_file": excel_path
    }