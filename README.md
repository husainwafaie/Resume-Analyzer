# AI Resume Analyzer

AI Resume Analyzer is a web application that uses artificial intelligence to analyze resumes against job descriptions. It detects keywords in the job description and provides feedback to users regarding 
resume compatability and how to impore resume tailoring for the given job.

## Features

- Upload resume in PDF or DOCX format
- Input job descriptions
- Analyze resume-job description similarity
- Extract and compare keywords
- Provide detailed feedback and recommendations
- User-friendly interface with animated results

## Tech Stack

- Frontend: React.js
- Backend: FastAPI (Python)
- NLP: scikit-learn, NLTK
- File Parsing: PyPDF2, python-docx

## Setup

### Prerequisites

- Node.js and npm
- Python 3.7+
- pip

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

## Usage

1. Open your web browser and go to `http://localhost:3000`
2. Upload your resume (PDF or DOCX format)
3. Paste the job description in the provided text area
4. Click "Analyze Resume"
5. View the analysis results, including similarity score, matching and missing keywords, and detailed feedback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2.0 License.