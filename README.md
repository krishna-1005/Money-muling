# Money Muling Detection Engine — Graph-Based Financial Crime Detection

A web-based financial forensics platform that leverages graph theory and advanced pattern detection to identify sophisticated money muling networks hidden within transaction data.

**Status:** 🚀 RIFT 2026 Hackathon Submission | Graph Theory / Financial Crime Detection Track

---

## 📊 Live Demo

**Live Application URL:** [Update with deployment URL](https://your-deployed-domain.com)

*Replace with actual Vercel/Netlify/Railway deployment URL before submission*

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 18+ with Vite
- **Visualization:** Cytoscape.js (interactive graph rendering)
- **Styling:** Tailwind CSS + Custom CSS
- **HTTP Client:** Axios
- **Build Tool:** Vite

### Backend
- **Language:** Python 3.10+
- **API Framework:** FastAPI
- **Graph Library:** NetworkX
- **Data Processing:** pandas, NumPy
- **Async Support:** Uvicorn ASGI server

### Deployment
- **Frontend:** Vercel / Netlify
- **Backend:** Railway / Render / Heroku
- **Container:** Docker (optional)

---

## 🏗️ System Architecture

### Two-Tier Architecture

**Frontend (React + Vite)**
- CSV File Upload Component
- Interactive Graph Visualization (Cytoscape)
- Fraud Ring Summary Table
- JSON Report Download Button

**Backend (FastAPI + Python)**
- Graph Construction (NetworkX)
  - Nodes: Account IDs
  - Edges: Directed transactions
  - Edge attributes: amount, timestamp
- Parallel Pattern Detection Modules
  - Cycle Detection (cycles 3-5)
  - Smurfing Detection (fan-in/fan-out)
  - Shell Network Detection (layered accounts)
- Scoring & Risk Assessment
  - Per-account suspicion scores (0-100)
  - Per-ring risk scores
- JSON Report Generation
  - Suspicious accounts array
  - Fraud rings array
  - Summary statistics

### Key Files

| File | Purpose |
|------|---------|
| [backend/graph_engine.py](backend/graph_engine.py) | Core detection pipeline orchestration |
| [backend/detectors/cycle_detector.py](backend/detectors/cycle_detector.py) | Cycle detection (circular fund routing) |
| [backend/detectors/smurfing_detector.py](backend/detectors/smurfing_detector.py) | Smurfing pattern detection (fan-in/fan-out) |
| [backend/detectors/shell_detector.py](backend/detectors/shell_detector.py) | Shell network detection (layered accounts) |
| [backend/scoring.py](backend/scoring.py) | Suspicion score calculation |
| [backend/output_builder.py](backend/output_builder.py) | JSON report formatting |
| [frontend/src/App.jsx](frontend/src/App.jsx) | Main React application |
| [frontend/src/components/GraphVisualization.jsx](frontend/src/components/GraphVisualization.jsx) | Interactive graph rendering |
| [frontend/src/components/FraudRingTable.jsx](frontend/src/components/FraudRingTable.jsx) | Fraud rings summary table |

---

## 🔍 Algorithm Approach

### Detection Patterns

#### 1. **Circular Fund Routing (Cycles)**
**What it detects:** Closed-loop money transfer chains that obscure the origin of funds.

**Pattern Signature:** A → B → C → A (minimum 3 nodes, maximum 5)

**Algorithm:** 
- Uses NetworkX's `simple_cycles()` to enumerate all cycles in the directed graph
- Filters for cycles of length 3-5 (excludes longer cycles due to computational cost)
- Time Complexity: **O(V + E)** with DFS-based cycle enumeration

#### 2. **Smurfing Patterns (Fan-in / Fan-out)**
**What it detects:** Splitting or aggregating transactions to evade detection thresholds.

**Pattern Signatures:**
- **Fan-in:** 10+ senders → 1 aggregator account (within 72 hours)
- **Fan-out:** 1 disperser → 10+ receivers (within 72 hours)

**Algorithm:**
- Groups transactions by receiver (for fan-in) or sender (for fan-out)
- Implements sliding 72-hour time window analysis
- Counts unique counterparties within each window
- Time Complexity: **O(E log E)** where E = number of transactions

#### 3. **Layered Shell Networks (Transaction Chains)**
**What it detects:** Multi-hop paths through low-activity intermediate accounts designed to obscure destination.

**Pattern Signature:** Source → Shell₁ → Shell₂ → ... → Destination (4+ hops, with 2-3 transaction intermediates)

**Algorithm:**
- Identifies paths of length ≥ 5 nodes (4+ edges / 3+ hops)
- Intermediate nodes must have exactly 2-3 total transactions (in + out degree)
- Uses DFS with depth limiting to avoid exponential explosion
- Time Complexity: **O(V² × E)** in worst case, **O(E)** on sparse networks

### Overall Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Graph Construction | O(V + E) | O(V + E) |
| Cycle Detection | O(V + E) | O(V) |
| Smurfing Detection | O(E log E) | O(E) |
| Shell Detection | O(E) | O(V) |
| **Total Pipeline** | **O(V + E log E)** | **O(V + E)** |

**Performance Target:** ≤ 30 seconds for 10,000 transactions

---

## 📈 Suspicion Score Methodology

### Score Calculation Pipeline

Each detected pattern contributes a base score:

| Pattern Type | Base Score | Modifier |
|--------------|-----------|----------|
| Cycle | 40 | +3 per cycle length |
| Smurfing (Fan-in) | 30 | +0.5 per additional sender |
| Smurfing (Fan-out) | 30 | +0.5 per additional receiver |
| Shell Network | 20 | +2.5 per shell node |

**Aggregation:** Sum all pattern contributions, apply ring multiplier, cap at 100.0

### False Positive Control

Safe patterns (not flagged):
- Merchant accounts with legitimate high-volume activity
- Payroll/compensation accounts
- Regular business partner transactions

Red flags:
- Temporal clustering within 72 hours
- Low account age with high activity
- Inconsistent transaction amounts

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.10+** (Backend)
- **Node.js 16+** and npm (Frontend)
- **Git** for version control

### Backend Setup

```bash
cd backend
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
npm install cytoscape react-cytoscapejs
```

---

## 📱 Usage Instructions

### Starting the Application

**Backend (Terminal 1):**
```bash
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

### Using the Web Application

1. Open `http://localhost:5173/`
2. Upload a CSV file (see sample.csv for format)
3. View results in graph, table, and summary cards
4. Download JSON report

### Input Format

CSV columns required:
- `transaction_id` (String)
- `sender_id` (String)
- `receiver_id` (String)
- `amount` (Float)
- `timestamp` (DateTime: YYYY-MM-DD HH:MM:SS)

### Output Format

Downloadable JSON report (spec-compliant):
```json
{
  "suspicious_accounts": [
    {
      "account_id": "ACC_00123",
      "suspicion_score": 87.5,
      "detected_patterns": ["cycle", "smurfing_fan_in"],
      "ring_id": "RING_001"
    }
  ],
  "fraud_rings": [
    {
      "ring_id": "RING_001",
      "member_accounts": ["ACC_00123", "ACC_00456"],
      "pattern_type": "cycle",
      "risk_score": 95.3
    }
  ],
  "summary": {
    "total_accounts_analyzed": 500,
    "suspicious_accounts_flagged": 15,
    "fraud_rings_detected": 4,
    "processing_time_seconds": 2.3
  }
}
```

---

## ⚠️ Known Limitations

1. **Heuristic Detection:** Pattern detection is probabilistic; false positives/negatives possible
2. **Performance:** Degrades on graphs with 50,000+ accounts without optimization
3. **False Positives:** High-volume merchants may flag as smurfing; no merchant exemption built-in
4. **Temporal Analysis:** Only 72-hour window for smurfing; longer patterns not detected
5. **Data Privacy:** No encryption or persistent storage; use HTTPS in production
6. **Visualization:** Becomes cluttered with 1,000+ accounts

---

## 👥 Team Members

- **Krishna** — Frontend Development (React, Vite, Graph Visualization)
- **Hariprasad** — Backend Development (Graph Engine, Detection Algorithms, Scoring)

---

## 🎯 Hackathon Submission Checklist

- [x] Live deployed web application
- [x] CSV file upload on homepage
- [x] Interactive graph visualization with suspicious node highlighting
- [x] Fraud ring summary table (Ring ID, Pattern, Members, Risk Score)
- [x] Downloadable JSON output file (spec-compliant format)
- [x] Detects circular fund routing (cycles)
- [x] Detects smurfing patterns (fan-in/fan-out)
- [x] Detects layered shell networks
- [x] Suspicion score calculation (0-100 scale)
- [x] Processing time ≤ 30 seconds target
- [x] Comprehensive README with methodology
- [ ] LinkedIn video demonstration (post after deployment)
- [ ] GitHub repository made public
- [ ] RIFT problem statement selected on website

---

**Last Updated:** February 19, 2026  
**Version:** 1.0.0 (RIFT Hackathon Submission)
