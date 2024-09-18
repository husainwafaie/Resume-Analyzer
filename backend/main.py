from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.file_parsers import extract_text_from_pdf, extract_text_from_docx
from utils.nlp_utils import extract_keywords
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

class CompareKeywordsRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/compare-keywords/")
async def compare_keywords(request: CompareKeywordsRequest):
    resume_keywords = extract_keywords(request.resume_text)
    job_description_keywords = extract_keywords(request.job_description)

    matching_keywords = set(resume_keywords).intersection(set(job_description_keywords))
    missing_keywords = set(job_description_keywords) - set(resume_keywords)

    return {
        "matching_keywords": list(matching_keywords),
        "missing_keywords": list(missing_keywords)
    }

# Upload resume and extract text
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
