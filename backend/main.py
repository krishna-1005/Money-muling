import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from graph_engine import run_detection
from output_builder import build_output_json

# Load environment variables
load_dotenv()

app = FastAPI()

# Get frontend URL from .env
frontend_url = os.getenv("FRONTEND_URL", "https://money-muling-detection-q8wj.vercel.app")
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Main endpoint for fraud detection analysis.
    Accepts: CSV file with transaction data
    Returns: Graph data, detected fraud rings, suspicious accounts, and downloadable JSON report
    """
    start_time = time.time()

    try:
        contents = await file.read()

        # Run detection pipeline
        graph_data, suspicious_accounts, fraud_rings, summary = run_detection(contents)

        # Calculate processing time
        processing_time = round(time.time() - start_time, 2)
        summary["processing_time_seconds"] = processing_time

        # Build JSON output
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
    """Health check endpoint"""
    return {"status": "ok"}


# Run locally with dynamic port
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
