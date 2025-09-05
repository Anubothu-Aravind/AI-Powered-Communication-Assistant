import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import EmailTable from "./components/EmailTable";
import AnalyticsChart from "./components/AnalyticsChart";
import { uploadCSV } from "./services/api";

function App() {
  const [emails, setEmails] = useState([]);

  const handleUpload = async (file) => {
    try {
      const data = await uploadCSV(file);
      setEmails(data.emails);
    } catch (err) {
      console.error(err);
      alert("Error uploading CSV");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI-Powered Communication Assistant</h2>
      <UploadForm onUpload={handleUpload} />
      {emails.length > 0 && (
        <>
          <EmailTable emails={emails} />
          <AnalyticsChart emails={emails} />
        </>
      )}
    </div>
  );
}

export default App;
