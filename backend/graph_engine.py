import pandas as pd
import networkx as nx
from io import BytesIO

from detectors.cycle_detector import detect_cycles
from detectors.smurfing_detector import detect_smurfing
from detectors.shell_detector import detect_shells
from scoring import calculate_scores


def run_detection(csv_bytes: bytes):
    """
    Main entry point for fraud detection.
    Returns graph data, suspicious accounts, fraud rings, summary.
    """

    # ---------- 1. Load CSV ----------
    df = pd.read_csv(BytesIO(csv_bytes))

    required_cols = {
        "transaction_id",
        "sender_id",
        "receiver_id",
        "amount",
        "timestamp",
    }

    if not required_cols.issubset(df.columns):
        raise ValueError("CSV schema mismatch")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ---------- 2. Build Directed Graph ----------
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["sender_id"],
            row["receiver_id"],
            amount=row["amount"],
            timestamp=row["timestamp"],
        )

    total_accounts = G.number_of_nodes()

    # ---------- 3. Run Detectors ----------
    cycle_rings = detect_cycles(G)
    smurf_rings = detect_smurfing(G, df)
    shell_rings = detect_shells(G)

    all_rings = cycle_rings + smurf_rings + shell_rings

    # ---------- 4. Score Accounts ----------
    suspicious_accounts = calculate_scores(G, all_rings)

    # ---------- 5. Prepare Graph Output ----------
    graph_nodes = []
    suspicious_ids = {a["account_id"] for a in suspicious_accounts}

    ring_lookup = {}
    for ring in all_rings:
        for acc in ring["member_accounts"]:
            ring_lookup[acc] = ring["ring_id"]

    for node in G.nodes():
        graph_nodes.append(
            {
                "account_id": node,
                "suspicion_score": next(
                    (a["suspicion_score"] for a in suspicious_accounts if a["account_id"] == node),
                    0.0,
                ),
                "suspicious": node in suspicious_ids,
                "ring_id": ring_lookup.get(node),
            }
        )

    graph_edges = [
        {"from": u, "to": v} for u, v in G.edges()
    ]

    graph_data = {
        "nodes": graph_nodes,
        "edges": graph_edges,
    }

    # ---------- 6. Summary ----------
    summary = {
        "total_accounts_analyzed": total_accounts,
        "suspicious_accounts_flagged": len(suspicious_accounts),
        "fraud_rings_detected": len(all_rings),
    }

    return graph_data, suspicious_accounts, all_rings, summary
