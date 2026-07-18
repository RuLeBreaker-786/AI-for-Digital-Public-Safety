HOTSPOT_DATA = [
    {
        "location": "Mumbai",
        "type": "Counterfeit seizure",
        "severity": "High",
        "notes": "Multiple recent seizures of fake ₹500 and ₹2000 notes at suburban markets and railway stations.",
        "lat": 19.0760,
        "lon": 72.8777,
    },
    {
        "location": "New Delhi",
        "type": "Digital scam cluster",
        "severity": "High",
        "notes": "Rising volume of UPI fraud and 'account suspension' phishing messages targeting senior citizens.",
        "lat": 28.6139,
        "lon": 77.2090,
    },
    {
        "location": "Bengaluru",
        "type": "Cyber payment fraud",
        "severity": "Medium",
        "notes": "Malicious payment gateway overlays and app cloning incidents reported in tech parks.",
        "lat": 12.9716,
        "lon": 77.5946,
    },
    {
        "location": "Kolkata",
        "type": "Counterfeit currency report",
        "severity": "Medium",
        "notes": "Fake ₹200 and ₹20 notes found in local bazaars and temple donation collections.",
        "lat": 22.5726,
        "lon": 88.3639,
    },
    {
        "location": "Hyderabad",
        "type": "Identity theft network",
        "severity": "Medium",
        "notes": "Organized social engineering campaigns linked to SIM swap and loan app fraud.",
        "lat": 17.3850,
        "lon": 78.4867,
    },
    {
        "location": "Chennai",
        "type": "Fake note circulation",
        "severity": "Medium",
        "notes": "Local banks report counterfeit ₹1000 notes with mismatched security thread patterns.",
        "lat": 13.0827,
        "lon": 80.2707,
    },
]


def generate_heatmap_data() -> dict:
    return {
        "description": "Geospatial fraud and counterfeit intelligence hotspots across major Indian metro locations, updated with recent incident context.",
        "hotspots": HOTSPOT_DATA,
    }
