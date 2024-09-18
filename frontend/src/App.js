import React from 'react';
import ResumeAnalyzer from './components/ResumeAnalyzer';
import './index.css';

function App() {
  return (
    <div className="container mt-5">
      <div className="text-center mb-4">
        <h1 className="display-4">AI Resume Analyzer</h1>
        <p className="lead">Optimize your resume based on job descriptions with AI insights</p>
      </div>
      <ResumeAnalyzer />
    </div>
  );
}

export default App;