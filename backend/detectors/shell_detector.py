import networkx as nx

def detect_shells(G: nx.DiGraph):
    """
    Detect layered shell networks:
    - Paths of length >= 5 nodes (minimum 4 hops / 3+ intermediate accounts)
    - Multiple intermediate nodes have only 2–3 total transactions
    """

    rings = []
    ring_counter = 1
    MIN_PATH_LENGTH = 5  # At least 5 nodes (source + 3 intermediate + target)
    SHELL_THRESHOLD_MIN = 2
    SHELL_THRESHOLD_MAX = 3
    MIN_SHELL_NODES = 2

    # Pre-calculate transaction counts (in + out degree)
    tx_count = {
        node: G.in_degree(node) + G.out_degree(node)
        for node in G.nodes()
    }

    # Track detected paths to avoid duplicates
    detected_paths = set()

    # Use DFS to find paths more efficiently
    def find_shell_paths(source, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        
        path = path + [source]
        visited.add(source)

        # If path is long enough, check if it forms a shell pattern
        if len(path) >= MIN_PATH_LENGTH:
            intermediates = path[1:-1]
            shell_nodes = [
                n for n in intermediates
                if SHELL_THRESHOLD_MIN <= tx_count.get(n, 0) <= SHELL_THRESHOLD_MAX
            ]

            if len(shell_nodes) >= MIN_SHELL_NODES:
                path_tuple = tuple(path)
                if path_tuple not in detected_paths:
                    detected_paths.add(path_tuple)
                    ring = {
                        "ring_id": f"RING_SHELL_{ring_counter:03d}",
                        "member_accounts": path,
                        "pattern_type": "layered_shell",
                        "risk_score": round(75.0 + (len(shell_nodes) * 2.5), 2),
                    }
                    rings.append(ring)
                    return ring_counter + 1

        # Continue DFS but limit depth to avoid exponential explosion
        if len(path) < MIN_PATH_LENGTH + 3:
            for neighbor in G.neighbors(source):
                if neighbor not in visited:
                    result = find_shell_paths(neighbor, visited.copy(), path)
                    if result:
                        ring_counter = result

        return ring_counter if 'ring_counter' in locals() else ring_counter

    # Process each potential source node
    for source in list(G.nodes())[:50]:  # Limit sources to avoid excessive computation
        try:
            new_counter = find_shell_paths(source)
            if new_counter:
                ring_counter = new_counter
        except:
            continue

    return rings
