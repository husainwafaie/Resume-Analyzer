import React, { useState } from 'react';

function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError('');
  };

  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!file || !jobDescription) {
      setError('Please upload a resume and enter a job description.');
      return;
    }
  
    const formData = new FormData();
    formData.append('files', file);
  
    try {
      // First, extract text from the resume
      const extractResponse = await fetch('http://localhost:8000/extract-text/', {
        method: 'POST',
        body: formData,
      });
  
      if (!extractResponse.ok) {
        throw new Error('Failed to extract text from resume');
      }
  
      const extractResult = await extractResponse.json();
      const resumeText = extractResult.texts[0];
  
      // Then, compare keywords
      const compareResponse = await fetch('http://localhost:8000/compare-keywords/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });
  
      if (!compareResponse.ok) {
        throw new Error('Failed to compare keywords');
      }
  
      const result = await compareResponse.json();
      setAnalysisResult(result);
      setError('');
    } catch (err) {
      setError('An error occurred during analysis. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="card shadow-sm p-4">
      <h2 className="mb-3">Resume Analysis</h2>
      <input type="file" className="form-control mb-3" onChange={handleFileChange} accept=".pdf,.docx" required />
      <textarea
        className="form-control mb-3"
        placeholder="Paste job description here"
        onChange={handleJobDescriptionChange}
        rows="6"
        required
      />
      <button className="btn btn-primary" onClick={handleAnalyze}>
        Analyze Resume
      </button>
      {error && <div className="alert alert-danger mt-3">{error}</div>}
      {analysisResult && (
        <div className="mt-3">
          <h3>Analysis Results:</h3>
          <p>Matching Keywords: {analysisResult.matching_keywords.join(', ')}</p>
          <p>Missing Keywords: {analysisResult.missing_keywords.join(', ')}</p>
        </div>
      )}
    </div>
  );
}

export default ResumeAnalyzer;