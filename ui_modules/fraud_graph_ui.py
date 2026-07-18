import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


def render_fraud_graph_module():
    st.header("Fraud Graph Intelligence")
    if st.button("Load Fraud Graph"):
        try:
            resp = requests.get(f"{API_URL}/insights/fraud-graph", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                st.write(data)
                nodes = pd.DataFrame(data["nodes"])
                edges = pd.DataFrame(data["edges"])
                st.subheader("Nodes")
                st.dataframe(nodes)
                st.subheader("Edges")
                st.dataframe(edges)
            else:
                st.error(f"Backend error: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Unable to call backend: {e}")
