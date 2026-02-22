import { useState } from "react";
import axios from "axios";

function UploadSection({ onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    try {
      setLoading(true);

      const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8001";

      // Create FormData and send as multipart/form-data for file upload
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(`${API_BASE}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      onResult(response.data);
    } catch (err) {
      console.error(err);
      alert("Error analyzing CSV");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Upload Transaction CSV</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>
    </div>
  );
}

export default UploadSection;
