import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render_threat_module():
    st.header("Citizen Threat Shield")
    
    col1, col2 = st.columns(2)
    with col1:
        channel = st.selectbox("Channel", ["WhatsApp", "IVR", "SMS", "Email", "Phone Call"])
    with col2:
        # IMPROVEMENT 1: 12 Regional Languages Advisory Dropdown
        language = st.selectbox("Advisory Language", [
            "English", "Hindi (हिन्दी)", "Marathi (मराठी)", "Tamil (தமிழ்)", 
            "Telugu (తెలుగు)", "Kannada (ಕನ್ನಡ)", "Gujarati (ગુજરાતી)", 
            "Bengali (বাংলা)", "Odia (ଓଡ଼ିଆ)", "Punjabi (ਪੰਜਾਬੀ)", 
            "Malayalam (മലയാളം)", "Assamese (অসমীয়া)"
        ])
        
    region = st.text_input("Region / City", value="India")
    description = st.text_area("Describe the suspicious threat or fraud message:")
    
    if st.button("Evaluate Threat"):
        if description.strip():
            try:
                resp = requests.post(
                    f"{API_URL}/predict/threat",
                    data={"channel": channel, "region": region, "description": description},
                    timeout=30,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.write(data)
                    
                    if data["risk_level"] == "high":
                        st.error("🚨 High threat level")
                    elif data["risk_level"] == "medium":
                        st.warning("⚠️ Medium threat level")
                    else:
                        st.success("✅ Low threat level")
                        
                    # Simulate translation of the advisory output
                    advisory = data.get("recommendation", "No recommendation provided.")
                    st.info(f"🗣️ **Advisory provided in {language}:** {advisory}")
                    
                else:
                    st.error(f"Backend error: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Unable to call backend: {e}")
        else:
            st.warning("Please describe the suspicious threat.")
