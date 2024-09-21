import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faTimesCircle, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import { useSpring, animated } from 'react-spring';
import { TypeAnimation } from 'react-type-animation';
import './AnalysisResults.css';

function AnalysisResults() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const location = useLocation();
  const navigate = useNavigate();
  const { resumeText, jobDescription } = location.state || {};

  const [showKeywords, setShowKeywords] = useState(false);
  const [currentFeedbackIndex, setCurrentFeedbackIndex] = useState(-1);

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

  const getSimilarityLabel = (similarity) => {
    if (similarity < 0.25) return 'No Match';
    if (similarity < 0.5) return 'Low Match';
    if (similarity < 0.75) return 'Good Match';
    return 'Perfect Match';
  };

  const getProgressBarColor = (similarity) => {
    const red = Math.max(0, Math.min(255, 510 * (1 - similarity)));
    const green = Math.max(0, Math.min(255, 510 * similarity));
    return `rgb(${red}, ${green}, 0)`;
  };

  const progressBarAnimation = useSpring({
    width: `${analysisResult ? analysisResult.similarity * 100 : 0}%`,
    from: { width: '0%' },
    config: { duration: 1100 },
    onRest: () => setShowKeywords(true),
  });

  const keywordsAnimation = useSpring({
    opacity: showKeywords ? 1 : 0,
    transform: showKeywords ? 'translateY(0)' : 'translateY(20px)',
    config: { duration: 1000 },
    delay: 500,
    onRest: () => setCurrentFeedbackIndex(0),
  });

  const handleTypingComplete = () => {
    if (currentFeedbackIndex < analysisResult.feedback.length - 1) {
      setCurrentFeedbackIndex(prevIndex => prevIndex + 1);
    }
  };

  if (loading) {
    return <div className="loader-container"><div className="loader"></div></div>;
  }

  return (
    <div className="analysis-results-container">
      <div className="card glass-effect">
        <h1 className="title">Analysis Results</h1>
        {error && <div className="alert alert-danger">{error}</div>}
        {analysisResult && (
          <div>
            <section className="similarity-section">
              <h2 className="section-title">Resume-Job Description Similarity</h2>
              <div className="similarity-score">
                <span className="score-value">{(analysisResult.similarity * 100).toFixed(2)}%</span>
                <span className="score-label">
                  {getSimilarityLabel(analysisResult.similarity)}
                </span>
              </div>
              <div className="progress-bar-container">
                <animated.div 
                  className="progress-bar"
                  style={{
                    ...progressBarAnimation,
                    backgroundColor: getProgressBarColor(analysisResult.similarity)
                  }}
                ></animated.div>
              </div>
            </section>

            <animated.section className="keywords-section" style={keywordsAnimation}>
              <h2 className="section-title" style={{ marginBottom: '2rem' }}>Keyword Analysis</h2>
              <div className="keyword-lists">
                <div className="keyword-list">
                  <h3 className="list-title">
                    <FontAwesomeIcon icon={faCheckCircle} className="icon-match" /> Matching Keywords
                  </h3>
                  <div className="keyword-tags">
                    {analysisResult.matching_keywords.map(keyword => 
                      <span key={keyword} className="keyword-tag match">{keyword}</span>
                    )}
                  </div>
                </div>
                <div className="keyword-list">
                  <h3 className="list-title">
                    <FontAwesomeIcon icon={faTimesCircle} className="icon-missing" /> Missing Keywords
                  </h3>
                  <div className="keyword-tags">
                    {analysisResult.missing_keywords.map(keyword => 
                      <span key={keyword} className="keyword-tag missing">{keyword}</span>
                    )}
                  </div>
                </div>
              </div>
            </animated.section>

            <section className="feedback-section">
              <h2 className="section-title">Feedback</h2>
              <ul className="feedback-list">
                {analysisResult.feedback.map((item, index) => (
                  <li key={index} className="feedback-item">
                    {index === currentFeedbackIndex ? (
                      <TypeAnimation
                        sequence={[
                          item,
                          500,
                          handleTypingComplete
                        ]}
                        wrapper="span"
                        cursor={true}
                        repeat={0}
                        speed={80}
                        style={{ display: 'inline-block' }}
                      />
                    ) : index < currentFeedbackIndex ? (
                      item
                    ) : null}
                  </li>
                ))}
              </ul>
            </section>
          </div>
        )}
        <button className="btn-back" onClick={handleGoBack}>
          <FontAwesomeIcon icon={faArrowLeft} /> Go Back
        </button>
      </div>
    </div>
  );
}

export default AnalysisResults;