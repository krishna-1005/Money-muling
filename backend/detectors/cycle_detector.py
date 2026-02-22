import networkx as nx


def detect_cycles(G: nx.DiGraph):
    """
    Detect circular fund routing (cycles of length 3 to 5).
    Returns a list of fraud ring dictionaries.
    """

    rings = []
    ring_counter = 1

    for cycle in nx.simple_cycles(G):
        cycle_len = len(cycle)

        if 3 <= cycle_len <= 5:
            ring_id = f"RING_CYCLE_{ring_counter:03d}"

            ring = {
                "ring_id": ring_id,
                "member_accounts": cycle,
                "pattern_type": "cycle",
                "risk_score": round(80 + (cycle_len * 3), 2),
            }

            rings.append(ring)
            ring_counter += 1

    return rings
