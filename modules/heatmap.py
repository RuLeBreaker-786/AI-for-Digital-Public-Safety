# Comprehensive Geospatial Intelligence Dataset Covering All 28 States & 8 UTs
HOTSPOT_DATA = [
    # States
    {"location": "Visakhapatnam - MVP Colony", "state": "Andhra Pradesh", "type": "Cyber payment fraud", "severity": "Medium", "notes": "Phishing sites targeting naval & port workers.", "lat": 17.7412, "lon": 83.3323},
    {"location": "Itanagar - Ganga Market", "state": "Arunachal Pradesh", "type": "Counterfeit seizure", "severity": "Low", "notes": "Fake ₹200 note circulation detected in retail markets.", "lat": 27.0844, "lon": 93.6053},
    {"location": "Guwahati - Fancy Bazar", "state": "Assam", "type": "Counterfeit currency report", "severity": "High", "notes": "High-quality FICN network active near railway transit hubs.", "lat": 26.1858, "lon": 91.7415},
    {"location": "Patna - Junction Corridor", "state": "Bihar", "type": "Counterfeit currency report", "severity": "High", "notes": "Fake currency movement reported along rail transport routes.", "lat": 25.6093, "lon": 85.1235},
    {"location": "Raipur - Pandri Market", "state": "Chhattisgarh", "type": "Identity theft network", "severity": "Medium", "notes": "Aadhaar spoofing & illegal biometric cloning ring.", "lat": 21.2514, "lon": 81.6296},
    {"location": "Panaji - Calangute Beach Belt", "state": "Goa", "type": "Digital scam cluster", "severity": "Medium", "notes": "Fake hotel booking portals & QR code payment scams.", "lat": 15.5438, "lon": 73.7552},
    {"location": "Ahmedabad - CG Road", "state": "Gujarat", "type": "Cyber payment fraud", "severity": "High", "notes": "Spoofed stock trading apps & bogus investment schemes.", "lat": 23.0300, "lon": 72.5600},
    {"location": "Gurugram - Cyber City", "state": "Haryana", "type": "Digital scam cluster", "severity": "High", "notes": "Illegal call center hub executing international tech support scams.", "lat": 28.4950, "lon": 77.0895},
    {"location": "Shimla - Mall Road", "state": "Himachal Pradesh", "type": "Digital scam cluster", "severity": "Low", "notes": "Fake homestay booking websites targeting tourists.", "lat": 31.1048, "lon": 77.1734},
    {"location": "Dhanbad - Station Road", "state": "Jharkhand", "type": "Digital scam cluster", "severity": "High", "notes": "Phishing & KYC update scam helpline network flagged by cyber cell.", "lat": 23.7957, "lon": 86.4304},
    {"location": "Bengaluru - Koramangala", "state": "Karnataka", "type": "Cyber payment fraud", "severity": "High", "notes": "App cloning and malicious QR code scams at retail outlets.", "lat": 12.9352, "lon": 77.6245},
    {"location": "Kochi - MG Road", "state": "Kerala", "type": "Identity theft network", "severity": "Medium", "notes": "Overseas job-guarantee phishing networks.", "lat": 9.9723, "lon": 76.2783},
    {"location": "Bhopal - MP Nagar", "state": "Madhya Pradesh", "type": "Identity theft network", "severity": "Medium", "notes": "Loan app harassment & unauthorized data scraping ring.", "lat": 23.2331, "lon": 77.4343},
    {"location": "Mumbai - BKC", "state": "Maharashtra", "type": "Counterfeit seizure", "severity": "High", "notes": "Fake ₹500 note syndicate operational around commercial hubs.", "lat": 19.0657, "lon": 72.8686},
    {"location": "Imphal - Thangal Bazar", "state": "Manipur", "type": "Counterfeit seizure", "severity": "Low", "notes": "Mismatched security thread patterns detected on fake notes.", "lat": 24.8081, "lon": 93.9368},
    {"location": "Shillong - Police Bazar", "state": "Meghalaya", "type": "Cyber payment fraud", "severity": "Low", "notes": "Unsolicited payment link SMS campaigns.", "lat": 25.5788, "lon": 91.8831},
    {"location": "Aizawl - Zarkawt", "state": "Mizoram", "type": "Identity theft network", "severity": "Low", "notes": "Fake lottery & SMS portal scams.", "lat": 23.7307, "lon": 92.7173},
    {"location": "Kohima - BOC Area", "state": "Nagaland", "type": "Counterfeit currency report", "severity": "Low", "notes": "Circulation of fake ₹500 notes during seasonal fairs.", "lat": 25.6747, "lon": 94.1100},
    {"location": "Bhubaneswar - Saheed Nagar", "state": "Odisha", "type": "Digital scam cluster", "severity": "Medium", "notes": "Electricity bill disconnection SMS scam pattern.", "lat": 20.2897, "lon": 85.8437},
    {"location": "Ludhiana - Clock Tower Market", "state": "Punjab", "type": "Counterfeit seizure", "severity": "High", "notes": "High-volume counterfeit ₹500 bills in textile trade.", "lat": 30.9010, "lon": 75.8573},
    {"location": "Jaipur - Johari Bazar", "state": "Rajasthan", "type": "Digital scam cluster", "severity": "High", "notes": "Part-time task scams & fraudulent job portals.", "lat": 26.9196, "lon": 75.8256},
    {"location": "Gangtok - M.G. Marg", "state": "Sikkim", "type": "Cyber payment fraud", "severity": "Low", "notes": "Fake taxi aggregators operating bogus UPI gateways.", "lat": 27.3314, "lon": 88.6138},
    {"location": "Chennai - T. Nagar", "state": "Tamil Nadu", "type": "Fake note circulation", "severity": "Medium", "notes": "Counterfeit ₹500 notes detected in retail jewelry markets.", "lat": 13.0418, "lon": 80.2341},
    {"location": "Hyderabad - HITECH City", "state": "Telangana", "type": "Identity theft network", "severity": "High", "notes": "Mule account network operation and instant loan app extortion.", "lat": 17.4435, "lon": 78.3772},
    {"location": "Agartala - Battala Market", "state": "Tripura", "type": "Counterfeit seizure", "severity": "Low", "notes": "Low-grade print fake currency moving across border towns.", "lat": 23.8315, "lon": 91.2768},
    {"location": "Noida - Sector 62", "state": "Uttar Pradesh", "type": "Digital scam cluster", "severity": "High", "notes": "Fake 'Digital Arrest' call center syndicate posing as CBI officers.", "lat": 28.6273, "lon": 77.3725},
    {"location": "Dehradun - Rajpur Road", "state": "Uttarakhand", "type": "Cyber payment fraud", "severity": "Medium", "notes": "Char Dham Yatra helicopter booking scam websites.", "lat": 30.3256, "lon": 78.0437},
    {"location": "Kolkata - Burrabazar", "state": "West Bengal", "type": "Counterfeit currency report", "severity": "High", "notes": "High-quality FICN smuggling transit route via border districts.", "lat": 22.5804, "lon": 88.3570},

    # Union Territories
    {"location": "Port Blair - Aberdeen Bazar", "state": "Andaman and Nicobar Islands", "type": "Cyber payment fraud", "severity": "Low", "notes": "Fake ferry ticket booking platforms.", "lat": 11.6680, "lon": 92.7378},
    {"location": "Chandigarh - Sector 17", "state": "Chandigarh", "type": "Digital scam cluster", "severity": "Medium", "notes": "Student visa & immigration scam operations.", "lat": 30.7398, "lon": 76.7827},
    {"location": "Daman - Seaface Road", "state": "Dadra and Nagar Haveli and Daman and Diu", "type": "Counterfeit seizure", "severity": "Low", "notes": "Fake currency notes detected at liquor retail outlets.", "lat": 20.4137, "lon": 72.8328},
    {"location": "New Delhi - Connaught Place", "state": "Delhi NCR", "type": "Digital scam cluster", "severity": "High", "notes": "Digital arrest scam call centers impersonating ED/CBI officials.", "lat": 28.6315, "lon": 77.2167},
    {"location": "Srinagar - Lal Chowk", "state": "Jammu and Kashmir", "type": "Counterfeit currency report", "severity": "Medium", "notes": "Counterfeit currency notes circulated in handicraft markets.", "lat": 34.0754, "lon": 74.8092},
    {"location": "Leh - Main Bazar", "state": "Ladakh", "type": "Cyber payment fraud", "severity": "Low", "notes": "Fake permit & trekking agency UPI payment pages.", "lat": 34.1642, "lon": 77.5848},
    {"location": "Kavaratti - Beach Road", "state": "Lakshadweep", "type": "Cyber payment fraud", "severity": "Low", "notes": "Phishing calls attempting OTP interception.", "lat": 10.5669, "lon": 72.6420},
    {"location": "Puducherry - Heritage Town", "state": "Puducherry", "type": "Identity theft network", "severity": "Low", "notes": "Unregistered French visa consultation portals.", "lat": 11.9338, "lon": 79.8297},
]

# All 28 States & 8 Union Territories Master List
ALL_INDIA_REGIONS = [
    "All",
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi NCR", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

DYNAMIC_INCIDENTS = []

def generate_heatmap_data(state_filter: str = "All", severity_filter: str = "All", incident_type_filter: str = "All") -> dict:
    all_hotspots = HOTSPOT_DATA + DYNAMIC_INCIDENTS
    
    filtered = all_hotspots
    if state_filter and state_filter != "All":
        filtered = [h for h in filtered if h.get("state") == state_filter]
        
    if severity_filter and severity_filter != "All":
        filtered = [h for h in filtered if h.get("severity") == severity_filter]

    if incident_type_filter and incident_type_filter != "All":
        filtered = [h for h in filtered if h.get("type") == incident_type_filter]

    return {
        "description": "Geospatial crime and counterfeit intelligence across all Indian States & Union Territories.",
        "regions": ALL_INDIA_REGIONS,
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
