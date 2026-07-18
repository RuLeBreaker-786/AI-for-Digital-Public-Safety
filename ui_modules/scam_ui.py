import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def render_scam_module():
    st.header("Digital Arrest Scam Detection")
    scam_text = st.text_area("Paste scam message or suspicious digital arrest text:")
    if st.button("Analyze Scam Text"):
        if scam_text.strip():
            try:
                resp = requests.post(f"{API_URL}/predict/scam", data={"message": scam_text}, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    st.write(data)
                    if data["risk_level"] == "high":
                        st.error("🚨 High-risk scam pattern detected")
                    elif data["risk_level"] == "medium":
                        st.warning("⚠️ Medium-risk scam pattern detected")
                    else:
                        st.success("✅ Low-risk scam pattern")
                else:
                    st.error(f"Backend error: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Unable to call backend: {e}")
        else:
            st.warning("Please enter the scam text before analyzing.")
