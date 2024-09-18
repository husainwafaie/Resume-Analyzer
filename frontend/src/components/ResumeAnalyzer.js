import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

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

      // Navigate to results page with the necessary data
      navigate('/results', { state: { resumeText, jobDescription } });
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
    </div>
  );
}

export default ResumeAnalyzer;