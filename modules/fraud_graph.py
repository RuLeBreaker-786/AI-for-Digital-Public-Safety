FRAUD_GRAPH_SAMPLE = {
    "nodes": [
        {"id": "A", "role": "Victim", "alerts": 3},
        {"id": "B", "role": "Scammer", "alerts": 12},
        {"id": "C", "role": "Money Mule", "alerts": 7},
        {"id": "D", "role": "Bank Account", "alerts": 5},
        {"id": "E", "role": "Device", "alerts": 4},
    ],
    "edges": [
        {"source": "A", "target": "B", "relation": "contact"},
        {"source": "B", "target": "C", "relation": "fund transfer"},
        {"source": "C", "target": "D", "relation": "deposit"},
        {"source": "B", "target": "E", "relation": "device link"},
    ],
}


def analyze_fraud_graph() -> dict:
    clusters = [
        {
            "cluster_id": 1,
            "members": ["B", "C", "D", "E"],
            "focus": "Fraudster infrastructure and associated mule network",
        },
        {
            "cluster_id": 2,
            "members": ["A"],
            "focus": "Victim reporting node",
        },
    ]
    return {
        "summary": "Graph intelligence package based on transaction and device linkage data.",
        "clusters": clusters,
        "nodes": FRAUD_GRAPH_SAMPLE["nodes"],
        "edges": FRAUD_GRAPH_SAMPLE["edges"],
    }
