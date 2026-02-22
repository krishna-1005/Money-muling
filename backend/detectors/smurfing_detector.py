from collections import defaultdict
from datetime import timedelta

def detect_smurfing(G, df):
    """
    Detect smurfing patterns:
    - Fan-in: many senders -> one receiver (10+ senders)
    - Fan-out: one sender -> many receivers (10+ receivers)
    Transactions must occur within a 72-hour window.
    """

    rings = []
    ring_counter = 1
    TIME_WINDOW = timedelta(hours=72)
    THRESHOLD = 10  # Spec requires 10+ participants

    # Sort by time for window analysis
    df_sorted = df.sort_values("timestamp").reset_index(drop=True)

    # ---------- FAN-IN ----------
    fan_in_map = defaultdict(list)

    for _, row in df_sorted.iterrows():
        fan_in_map[row["receiver_id"]].append(
            {
                "sender_id": row["sender_id"],
                "timestamp": row["timestamp"],
                "amount": row["amount"],
            }
        )

    for receiver, txns in fan_in_map.items():
        # Sliding window to find any 72-hour interval with 10+ unique senders
        for i in range(len(txns)):
            window_start = txns[i]["timestamp"]
            senders_in_window = set()
            
            for j in range(i, len(txns)):
                if txns[j]["timestamp"] - window_start <= TIME_WINDOW:
                    senders_in_window.add(txns[j]["sender_id"])
                else:
                    break
            
            if len(senders_in_window) >= THRESHOLD:
                ring = {
                    "ring_id": f"RING_SMURF_IN_{ring_counter:03d}",
                    "member_accounts": sorted(list(senders_in_window)) + [receiver],
                    "pattern_type": "smurfing_fan_in",
                    "risk_score": round(80.0 + (len(senders_in_window) * 0.5), 2),
                }
                rings.append(ring)
                ring_counter += 1
                break  # Avoid duplicate rings for same receiver

    # ---------- FAN-OUT ----------
    fan_out_map = defaultdict(list)

    for _, row in df_sorted.iterrows():
        fan_out_map[row["sender_id"]].append(
            {
                "receiver_id": row["receiver_id"],
                "timestamp": row["timestamp"],
                "amount": row["amount"],
            }
        )

    for sender, txns in fan_out_map.items():
        # Sliding window to find any 72-hour interval with 10+ unique receivers
        for i in range(len(txns)):
            window_start = txns[i]["timestamp"]
            receivers_in_window = set()
            
            for j in range(i, len(txns)):
                if txns[j]["timestamp"] - window_start <= TIME_WINDOW:
                    receivers_in_window.add(txns[j]["receiver_id"])
                else:
                    break
            
            if len(receivers_in_window) >= THRESHOLD:
                ring = {
                    "ring_id": f"RING_SMURF_OUT_{ring_counter:03d}",
                    "member_accounts": [sender] + sorted(list(receivers_in_window)),
                    "pattern_type": "smurfing_fan_out",
                    "risk_score": round(80.0 + (len(receivers_in_window) * 0.5), 2),
                }
                rings.append(ring)
                ring_counter += 1
                break  # Avoid duplicate rings for same sender

    return rings
