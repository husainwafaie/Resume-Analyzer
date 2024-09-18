import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ResumeAnalyzer from './components/ResumeAnalyzer';
import AnalysisResults from './components/AnalysisResults';
import './index.css';

function App() {
  return (
    <Router>
      <div className="container mt-5">
        <div className="text-center mb-4">
          <h1 className="display-4">AI Resume Analyzer</h1>
          <p className="lead">Optimize your resume based on job descriptions with AI insights</p>
        </div>
        <Routes>
          <Route path="/" element={<ResumeAnalyzer />} />
          <Route path="/results" element={<AnalysisResults />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;