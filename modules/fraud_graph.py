# Rich Multi-Campaign Fraud Graph Dataset Engine
CAMPAIGNS = {
    "digital_arrest": {
        "title": "Digital Arrest Syndicate (Delhi-NCR & Mewat Ring)",
        "exposure": "₹4.82 Crore",
        "mules_count": 6,
        "jurisdictions": "Delhi, HR, UP, RJ",
        "nodes": [
            {"id": "V1", "label": "Victim (Dr. Sharma)", "role": "Victim", "alerts": 2, "details": "Defrauded ₹85 Lakhs via fake CBI video call"},
            {"id": "V2", "label": "Victim (Anand Kumar)", "role": "Victim", "alerts": 1, "details": "Defrauded ₹42 Lakhs via spoofed Customs threat"},
            {"id": "S1", "label": "VoIP Server (Spoofed)", "role": "Scammer", "alerts": 18, "details": "IP: 185.220.101.4 | Mewat Hub"},
            {"id": "S2", "label": "Fake CBI Operator", "role": "Scammer", "alerts": 24, "details": "Primary Interrogator | Telegram alias @cbi_officer_9"},
            {"id": "M1", "label": "Mule Account #1 (HDFC)", "role": "Money Mule", "alerts": 9, "details": "Account 501004... | Fast layering"},
            {"id": "M2", "label": "Mule Account #2 (ICICI)", "role": "Money Mule", "alerts": 11, "details": "Account 002105... | Rapid ATM withdrawals"},
            {"id": "M3", "label": "Crypto Cashout Wallet", "role": "Money Mule", "alerts": 15, "details": "TRC-20 USDT Wallet: T9zP...8xL"},
            {"id": "B1", "label": "Shell Corp Account", "role": "Bank Account", "alerts": 8, "details": "Registered as Enterprise Logistics Pvt Ltd"},
            {"id": "D1", "label": "Linked Device IMEI", "role": "Device", "alerts": 7, "details": "IMEI: 8642010... | 14 SIM swaps detected"},
        ],
        "edges": [
            {"source": "S2", "target": "V1", "relation": "Spoofed Call"},
            {"source": "S2", "target": "V2", "relation": "Spoofed Call"},
            {"source": "S1", "target": "S2", "relation": "VoIP Routing"},
            {"source": "V1", "target": "M1", "relation": "RTGS ₹85L"},
            {"source": "V2", "target": "M2", "relation": "NEFT ₹42L"},
            {"source": "M1", "target": "B1", "relation": "Layering Transfer"},
            {"source": "M2", "target": "B1", "relation": "Layering Transfer"},
            {"source": "B1", "target": "M3", "relation": "P2P Crypto Conversion"},
            {"source": "S2", "target": "D1", "relation": "Device Binding"},
        ]
    },
    "counterfeit_ring": {
        "title": "Multi-State Counterfeit Currency Syndicate",
        "exposure": "₹1.45 Crore (FICN)",
        "mules_count": 4,
        "jurisdictions": "WB, BR, JH, MH",
        "nodes": [
            {"id": "P1", "label": "Printing Press Hub", "role": "Scammer", "alerts": 30, "details": "Border district offset printing facility"},
            {"id": "D1", "label": "Regional Distributor", "role": "Scammer", "alerts": 16, "details": "Coordinates bulk fake note deliveries"},
            {"id": "M1", "label": "Hawala Operator A", "role": "Money Mule", "alerts": 12, "details": "Handles clean currency conversion"},
            {"id": "M2", "label": "Hawala Operator B", "role": "Money Mule", "alerts": 10, "details": "Inter-state courier handler"},
            {"id": "R1", "label": "Retail Courier Kolkata", "role": "Money Mule", "alerts": 6, "details": "Injected fake ₹500 notes in wholesale markets"},
            {"id": "R2", "label": "Retail Courier Mumbai", "role": "Money Mule", "alerts": 8, "details": "Injected fake ₹500 notes near railway hubs"},
            {"id": "V1", "label": "Suburban Bank Cashier", "role": "Victim", "alerts": 3, "details": "Flagged batch deposit of 200 fake notes"},
        ],
        "edges": [
            {"source": "P1", "target": "D1", "relation": "Bulk Supply"},
            {"source": "D1", "target": "M1", "relation": "Commission Pay"},
            {"source": "D1", "target": "R1", "relation": "Consignment"},
            {"source": "D1", "target": "R2", "relation": "Consignment"},
            {"source": "R1", "target": "V1", "relation": "Note Deposit"},
            {"source": "M1", "target": "M2", "relation": "Hawala Channel"},
        ]
    },
    "loan_extortion": {
        "title": "Instant APK Loan Extortion Network",
        "exposure": "₹2.10 Crore",
        "mules_count": 5,
        "jurisdictions": "KA, TS, MH, DL",
        "nodes": [
            {"id": "A1", "label": "Malicious Loan APK", "role": "Device", "alerts": 22, "details": "Scrapes contacts, gallery & SMS without consent"},
            {"id": "C1", "label": "Extortion Call Center", "role": "Scammer", "alerts": 28, "details": "Morphs photos for blackmail calls"},
            {"id": "M1", "label": "Mule UPI Gateway 1", "role": "Money Mule", "alerts": 14, "details": "Fake merchant QR code collection point"},
            {"id": "M2", "label": "Mule UPI Gateway 2", "role": "Money Mule", "alerts": 11, "details": "Rapid UPI split-payout account"},
            {"id": "V1", "label": "Victim A (IT Professional)", "role": "Victim", "alerts": 4, "details": "Blackmailed with morphed contact photos"},
            {"id": "V2", "label": "Victim B (Student)", "role": "Victim", "alerts": 2, "details": "Coerced into paying 300% processing fee"},
        ],
        "edges": [
            {"source": "A1", "target": "C1", "relation": "Data Exfiltration"},
            {"source": "C1", "target": "V1", "relation": "Extortion Calls"},
            {"source": "C1", "target": "V2", "relation": "Extortion Calls"},
            {"source": "V1", "target": "M1", "relation": "UPI Payment"},
            {"source": "V2", "target": "M2", "relation": "UPI Payment"},
            {"source": "M1", "target": "M2", "relation": "Fund Aggregation"},
        ]
    }
}

def analyze_fraud_graph(campaign_key: str = "digital_arrest", role_filter: str = "All") -> dict:
    case_data = CAMPAIGNS.get(campaign_key, CAMPAIGNS["digital_arrest"])
    
    raw_nodes = case_data["nodes"]
    raw_edges = case_data["edges"]

    if role_filter and role_filter != "All":
        allowed_ids = {n["id"] for n in raw_nodes if n["role"] == role_filter}
        filtered_nodes = [n for n in raw_nodes if n["role"] == role_filter]
        filtered_edges = [e for e in raw_edges if e["source"] in allowed_ids or e["target"] in allowed_ids]
    else:
        filtered_nodes = raw_nodes
        filtered_edges = raw_edges

    return {
        "summary": f"Graph Intelligence Package for {case_data['title']}",
        "title": case_data["title"],
        "exposure": case_data["exposure"],
        "mules_count": case_data["mules_count"],
        "jurisdictions": case_data["jurisdictions"],
        "nodes": filtered_nodes,
        "edges": filtered_edges,
    }
