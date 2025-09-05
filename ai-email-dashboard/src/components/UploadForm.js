import React, { useState } from "react";

function UploadForm({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onUpload(file);
    } else {
      alert("Please select a CSV file");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit" style={{ marginLeft: "10px" }}>
        Upload
      </button>
    </form>
  );
}

export default UploadForm;
