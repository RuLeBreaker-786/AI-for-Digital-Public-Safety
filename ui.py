
import os
import streamlit as st
from ui_modules.currency_ui import render_currency_module
from ui_modules.scam_ui import render_scam_module
from ui_modules.citizen_threat_shield_ui import render_threat_module
from ui_modules.heatmap_ui import render_heatmap_module
from ui_modules.fraud_graph_ui import render_fraud_graph_module

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Fraud Detection Agent", page_icon="🛡️", layout="wide")

st.title("🛡️ Unified Fraud Detection Agent")
st.markdown("A single interface for counterfeit currency verification, digital arrest scam detection, citizen threat shield analysis, cyber heatmap insights, and fraud graph intelligence.")

st.sidebar.title("Modules")
module = st.sidebar.radio("Select application module", [
    "Counterfeit Currency", "Digital Arrest Scam", "Citizen Threat Shield", "Cyber Heatmap", "Fraud Graph Intelligence"
])

if module == "Counterfeit Currency":
    render_currency_module()
elif module == "Digital Arrest Scam":
    render_scam_module()
elif module == "Citizen Threat Shield":
    render_threat_module()
elif module == "Cyber Heatmap":
    render_heatmap_module()
elif module == "Fraud Graph Intelligence":
    render_fraud_graph_module()
