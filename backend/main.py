from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.file_parsers import extract_text_from_pdf, extract_text_from_docx
from utils.nlp_utils import analyze_resume
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/extract-text/")
async def extract_text_from_files(files: List[UploadFile]):
    extracted_texts = []
    for file in files:
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file.file)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(file.file)
        else:
            return {"error": "Unsupported file type"}
        extracted_texts.append(text)
    return {"texts": extracted_texts}

@app.post("/analyze-resume/")
async def analyze_resume_endpoint(request: AnalyzeResumeRequest):
    try:
        analysis_result = analyze_resume(request.resume_text, request.job_description)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)