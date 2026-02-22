import os
import sys
import time

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# 👇 Make backend folder importable in Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from graph_engine import run_detection
from output_builder import build_output_json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Main endpoint for fraud detection analysis.
    """
    start_time = time.time()

    try:
        contents = await file.read()

        # Run detection pipeline
        graph_data, suspicious_accounts, fraud_rings, summary = run_detection(contents)

        # Add processing time
        processing_time = round(time.time() - start_time, 2)
        summary["processing_time_seconds"] = processing_time

        # Build output JSON
        report_json = build_output_json(
            suspicious_accounts=suspicious_accounts,
            fraud_rings=fraud_rings,
            summary=summary,
        )

        return {
            "graph": graph_data,
            "suspicious_accounts": suspicious_accounts,
            "fraud_rings": fraud_rings,
            "summary": summary,
            "report_json": report_json,
        }

    except ValueError as e:
        return {
            "error": str(e),
            "detail": "Invalid CSV format or schema mismatch"
        }

    except Exception as e:
        return {
            "error": str(e),
            "detail": "An error occurred during analysis"
        }

@app.get("/health")
def health():
    return {"status": "ok"}