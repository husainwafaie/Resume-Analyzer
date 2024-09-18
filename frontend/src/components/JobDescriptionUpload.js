import React, { useState } from 'react';

function JobDescriptionUpload() {
  const [jobDescription, setJobDescription] = useState('');
  const [analyzeSuccess, setAnalyzeSuccess] = useState(false);

  const handleInputChange = (event) => {
    setJobDescription(event.target.value);
    setAnalyzeSuccess(false);
  };

  const handleAnalyze = async () => {
    const response = await fetch('http://localhost:8000/compare-keywords/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        job_description: jobDescription,
        resume_text: "Placeholder for resume text", // Replace this with actual resume text later
      }),
    });

    if (response.ok) {
      setAnalyzeSuccess(true);
    }
  };

  return (
    <div className="card shadow-sm p-4">
      <h2 className="mb-3">Enter Job Description</h2>
      <textarea
        className="form-control mb-3"
        placeholder="Paste job description here"
        onChange={handleInputChange}
        rows="6"
      />
      <button className="btn btn-primary" onClick={handleAnalyze}>
        Analyze Keywords
      </button>
      {analyzeSuccess && <div className="alert alert-success mt-3">Job description analyzed successfully!</div>}
    </div>
  );
}

export default JobDescriptionUpload;
