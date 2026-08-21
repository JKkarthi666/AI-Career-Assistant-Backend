import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from config import UPLOAD_DIR, logger
from resume_parser import parse_resume
from job_matcher import find_jobs, export_excel

app = FastAPI(title="Job Matching Engine API")

class JobMatchResponse(BaseModel):
    skills_detected: List[str]
    total_jobs: int
    excel_file: str

@app.post("/upload-resume/", response_model=JobMatchResponse)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    file_path = UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"Processing resume: {file.filename}")
        parsed = parse_resume(str(file_path))
        skills = parsed.get("skills", [])
        
        if not skills:
            raise HTTPException(status_code=422, detail="No extractable skills found in the document.")
            
        # Await the concurrent scraping engine
        jobs = await find_jobs(skills)
        excel_path = export_excel(jobs)
        
        return JobMatchResponse(
            skills_detected=skills,
            total_jobs=len(jobs),
            excel_file=excel_path
        )
        
    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during processing.")
    finally:
        # Clean up the uploaded file to save disk space
        if file_path.exists():
            file_path.unlink()
