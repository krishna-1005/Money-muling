from collections import defaultdict

def calculate_scores(G, fraud_rings):
    """
    Calculate suspicion score per account based on detected fraud rings.
    Returns list of suspicious accounts sorted by score (desc).
    """

    score_map = defaultdict(float)
    pattern_map = defaultdict(set)
    ring_map = {}

    # ---------- Scoring weights ----------
    WEIGHTS = {
        "cycle": 40,
        "smurfing_fan_in": 30,
        "smurfing_fan_out": 30,
        "layered_shell": 20,
    }

    # ---------- Aggregate scores ----------
    for ring in fraud_rings:
        pattern = ring["pattern_type"]
        ring_id = ring["ring_id"]
        weight = WEIGHTS.get(pattern, 10)

        for acc in ring["member_accounts"]:
            score_map[acc] += weight
            pattern_map[acc].add(pattern)
            ring_map[acc] = ring_id

    # ---------- Normalize scores (cap at 100) ----------
    suspicious_accounts = []

    for acc, score in score_map.items():
        suspicious_accounts.append(
            {
                "account_id": acc,
                "suspicion_score": round(min(score, 100.0), 2),
                "detected_patterns": sorted(list(pattern_map[acc])),
                "ring_id": ring_map.get(acc),
            }
        )

    # ---------- Sort descending ----------
    suspicious_accounts.sort(
        key=lambda x: x["suspicion_score"], reverse=True
    )

    return suspicious_accounts
