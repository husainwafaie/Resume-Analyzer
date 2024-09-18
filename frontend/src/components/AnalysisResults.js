import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function AnalysisResults() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const location = useLocation();
  const navigate = useNavigate();
  const { resumeText, jobDescription } = location.state || {};

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (!resumeText || !jobDescription) {
        setError('Missing resume or job description data.');
        setLoading(false);
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/analyze-resume/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to analyze resume');
        }

        const result = await response.json();
        setAnalysisResult(result);
      } catch (err) {
        setError('An error occurred during analysis. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [resumeText, jobDescription]);

  const handleGoBack = () => {
    navigate('/');
  };

  if (loading) {
    return <div className="text-center mt-5"><div className="spinner-border" role="status"></div></div>;
  }

  return (
    <div className="card shadow-sm p-4">
      <h2 className="mb-3">Analysis Results</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      {analysisResult && (
        <div>
          <h3>Resume-Job Description Similarity</h3>
          <p>Similarity Score: {(analysisResult.similarity * 100).toFixed(2)}%</p>

          <h3>Keyword Analysis</h3>
          <h4>Matching Keywords:</h4>
          <p>{analysisResult.matching_keywords.join(', ')}</p>
          <h4>Missing Keywords:</h4>
          <p>{analysisResult.missing_keywords.join(', ')}</p>

          <h3>Feedback</h3>
          <ul>
            {analysisResult.feedback.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
      <button className="btn btn-secondary mt-3" onClick={handleGoBack}>Go Back</button>
    </div>
  );
}

export default AnalysisResults;