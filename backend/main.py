from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from utils.file_parsers import extract_text_from_pdf, extract_text_from_docx
from utils.nlp_utils import analyze_resume

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Assuming React is running on localhost:3000
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for AnalyzeResumeRequest
class AnalyzeResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/extract-text/")
async def extract_text_from_files(files: List[UploadFile]):
    extracted_texts = []
    for file in files:
        contents = await file.read()
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(contents)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        extracted_texts.append(text)
    return {"texts": extracted_texts}

@app.post("/analyze-resume/")
async def analyze_resume_endpoint(request: AnalyzeResumeRequest):
    resume_text = request.resume_text
    job_description = request.job_description
    
    analysis_result = analyze_resume(resume_text, job_description)

    if not analysis_result:
        raise HTTPException(status_code=500, detail="Analysis failed")
    
    return analysis_result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
