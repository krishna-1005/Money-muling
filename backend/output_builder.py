def build_output_json(suspicious_accounts, fraud_rings, summary):
    """
    Build the exact JSON output format required by RIFT.
    """

    output = {
        "suspicious_accounts": [],
        "fraud_rings": [],
        "summary": {
            "total_accounts_analyzed": summary.get("total_accounts_analyzed", 0),
            "suspicious_accounts_flagged": summary.get(
                "suspicious_accounts_flagged", 0
            ),
            "fraud_rings_detected": summary.get("fraud_rings_detected", 0),
            "processing_time_seconds": summary.get(
                "processing_time_seconds", 0.0
            ),
        },
    }

    # ---------- Suspicious Accounts ----------
    for acc in suspicious_accounts:
        output["suspicious_accounts"].append(
            {
                "account_id": acc["account_id"],
                "suspicion_score": float(acc["suspicion_score"]),
                "detected_patterns": acc["detected_patterns"],
                "ring_id": acc["ring_id"],
            }
        )

    # ---------- Fraud Rings ----------
    for ring in fraud_rings:
        output["fraud_rings"].append(
            {
                "ring_id": ring["ring_id"],
                "member_accounts": ring["member_accounts"],
                "pattern_type": ring["pattern_type"],
                "risk_score": float(ring["risk_score"]),
            }
        )

    return output
