import React, { useState } from 'react';

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadSuccess(false);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('files', file);

    const response = await fetch('http://localhost:8000/extract-text/', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      setUploadSuccess(true);
    }
  };

  return (
    <div className="card shadow-sm p-4">
      <h2 className="mb-3">Upload Resume</h2>
      <input type="file" className="form-control mb-3" onChange={handleFileChange} />
      <button className="btn btn-primary" onClick={handleUpload}>
        Upload and Analyze
      </button>
      {uploadSuccess && <div className="alert alert-success mt-3">Resume uploaded successfully!</div>}
    </div>
  );
}

export default ResumeUpload;
