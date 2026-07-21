# Expanded Geospatial Intelligence Data with Inter-District / Sub-Regional Granularity
HOTSPOT_DATA = [
    # Maharashtra
    {"location": "Mumbai - Bandra Kurla Complex", "state": "Maharashtra", "type": "Counterfeit seizure", "severity": "High", "notes": "Fake ₹500 note syndicate operational around commercial hubs.", "lat": 19.0657, "lon": 72.8686},
    {"location": "Mumbai - Dadar Wholesale Market", "state": "Maharashtra", "type": "Counterfeit seizure", "severity": "High", "notes": "Seizure of counterfeit ₹500 notes at high-volume markets.", "lat": 19.0178, "lon": 72.8478},
    {"location": "Pune - Hinjewadi Tech Park", "state": "Maharashtra", "type": "Cyber payment fraud", "severity": "Medium", "notes": "Spoofed payment gateways targeting IT employees.", "lat": 18.5912, "lon": 73.7389},
    {"location": "Nagpur - Railway Junction", "state": "Maharashtra", "type": "Counterfeit currency report", "severity": "Medium", "notes": "Circulation of fake ₹200 currency notes near booking counters.", "lat": 21.1524, "lon": 79.0888},

    # Delhi NCR
    {"location": "New Delhi - Connaught Place", "state": "Delhi NCR", "type": "Digital scam cluster", "severity": "High", "notes": "Digital arrest scam call centers impersonating ED/CBI officials.", "lat": 28.6315, "lon": 77.2167},
    {"location": "Delhi - Dwarka Sector 21", "state": "Delhi NCR", "type": "Digital scam cluster", "severity": "High", "notes": "Organized WhatsApp spoofing & illegal VoIP gateway hub.", "lat": 28.5521, "lon": 77.0585},
    {"location": "Gurugram - Cyber City", "state": "Delhi NCR", "type": "Identity theft network", "severity": "Medium", "notes": "SIM swap fraud and malicious loan app tele-calling rings.", "lat": 28.4950, "lon": 77.0895},

    # Karnataka
    {"location": "Bengaluru - Koramangala", "state": "Karnataka", "type": "Cyber payment fraud", "severity": "High", "notes": "App cloning and malicious QR code scams at retail outlets.", "lat": 12.9352, "lon": 77.6245},
    {"location": "Bengaluru - Whitefield", "state": "Karnataka", "type": "Digital scam cluster", "severity": "Medium", "notes": "Part-time job & task-based Telegram investment scams.", "lat": 12.9698, "lon": 77.7500},
    {"location": "Mysuru - Devaraja Market", "state": "Karnataka", "type": "Counterfeit seizure", "severity": "Low", "notes": "Low-grade color copy ₹100 notes detected during retail sales.", "lat": 12.3087, "lon": 76.6531},

    # West Bengal
    {"location": "Kolkata - Burrabazar", "state": "West Bengal", "type": "Counterfeit currency report", "severity": "High", "notes": "High-quality FICN smuggling transit route via border districts.", "lat": 22.5804, "lon": 88.3570},
    {"location": "Kolkata - Salt Lake Sector V", "state": "West Bengal", "type": "Digital scam cluster", "severity": "High", "notes": "Tech support scam call centers targeting citizens.", "lat": 22.5726, "lon": 88.4331},

    # Telangana
    {"location": "Hyderabad - HITECH City", "state": "Telangana", "type": "Identity theft network", "severity": "High", "notes": "Mule account network operation and instant loan app extortion.", "lat": 17.4435, "lon": 78.3772},
    {"location": "Hyderabad - Charminar Area", "state": "Telangana", "type": "Counterfeit seizure", "severity": "Medium", "notes": "Circulation of fake ₹500 notes during night trading.", "lat": 17.3616, "lon": 78.4747},

    # Tamil Nadu
    {"location": "Chennai - T. Nagar", "state": "Tamil Nadu", "type": "Fake note circulation", "severity": "Medium", "notes": "Counterfeit ₹500 notes detected in retail jewelry & textile markets.", "lat": 13.0418, "lon": 80.2341},

    # Jharkhand & Bihar
    {"location": "Dhanbad - Station Road", "state": "Jharkhand", "type": "Digital scam cluster", "severity": "High", "notes": "Phishing & KYC update scam helpline network flagged by cyber cell.", "lat": 23.7957, "lon": 86.4304},
    {"location": "Patna - Junction Corridor", "state": "Bihar", "type": "Counterfeit currency report", "severity": "Medium", "notes": "Fake currency movement reported along rail transport routes.", "lat": 25.6093, "lon": 85.1235},
]

# Dynamic in-memory store for newly reported incidents during the session
DYNAMIC_INCIDENTS = []

def generate_heatmap_data(state_filter: str = "All", severity_filter: str = "All") -> dict:
    all_hotspots = HOTSPOT_DATA + DYNAMIC_INCIDENTS
    
    filtered = all_hotspots
    if state_filter and state_filter != "All":
        filtered = [h for h in filtered if h.get("state") == state_filter]
        
    if severity_filter and severity_filter != "All":
        filtered = [h for h in filtered if h.get("severity") == severity_filter]

    states = sorted(list(set(h["state"] for h in all_hotspots if "state" in h)))

    return {
        "description": "Geospatial fraud and counterfeit intelligence hotspots across India with inter-district granularity.",
        "states": ["All"] + states,
        "total_incidents": len(filtered),
        "hotspots": filtered,
    }

def add_hotspot_incident(location: str, state: str, incident_type: str, severity: str, lat: float, lon: float, notes: str) -> dict:
    new_item = {
        "location": location,
        "state": state,
        "type": incident_type,
        "severity": severity,
        "notes": notes,
        "lat": lat,
        "lon": lon,
    }
    DYNAMIC_INCIDENTS.append(new_item)
    return {"status": "success", "message": "New geospatial incident logged successfully.", "incident": new_item}
