import { useState } from "react";
import "./App.css";
import ThreeScene from "./components/ThreeScene";

import UploadSection from "./components/UploadSection";
import GraphVisualization from "./components/GraphVisualization";
import FraudRingTable from "./components/FraudRingTable";
import DownloadButton from "./components/DownloadButton";

function App() {
  const [result, setResult] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleResult = (data) => {
    setResult(data);
    setShowResults(true);   // switch to results "page"
  };

  const goBack = () => {
    setShowResults(false);
  };

  return (
    <div className="app">

      {/* 3D Background */}
      <ThreeScene />

      {!showResults ? (
        /* ================= UPLOAD PAGE ================= */
        <div className="upload-page">
          <h1 className="main-title">
            Graph-Based Financial Crime Detection Engine
          </h1>
          <p className="sub-title">
            Money Muling Detection | RIFT 2026
          </p>

          <div className="upload-box">
            <UploadSection onResult={handleResult} />
          </div>
        </div>
      ) : (
        /* ================= RESULT PAGE ================= */
        <div className="result-page">

          <h1 className="main-title">Analysis Results</h1>

          <div className="summary-grid">
            <SummaryCard title="Accounts Analyzed" value={result.summary.total_accounts_analyzed} />
            <SummaryCard title="Suspicious Accounts" value={result.summary.suspicious_accounts_flagged} />
            <SummaryCard title="Fraud Rings" value={result.summary.fraud_rings_detected} />
            <SummaryCard title="Processing Time (s)" value={result.summary.processing_time_seconds} />
          </div>

          <div className="content-grid">
            <div className="card large-card">
              <h2>Transaction Network</h2>
              <GraphVisualization graph={result.graph} />
            </div>

            <div className="card">
              <h2>Fraud Rings</h2>
              <FraudRingTable rings={result.fraud_rings} />
            </div>
          </div>

          <div className="download-container">
            <DownloadButton data={result.report_json} />
            <button onClick={goBack}>← Back to Upload</button>
          </div>

        </div>
      )}

    </div>
  );
}

function SummaryCard({ title, value }) {
  return (
    <div className="summary-card">
      <p className="summary-title">{title}</p>
      <p className="summary-value">{value}</p>
    </div>
  );
}

export default App;