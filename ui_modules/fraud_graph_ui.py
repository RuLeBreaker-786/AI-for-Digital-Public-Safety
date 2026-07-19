import os
import streamlit as st
import requests
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render_fraud_graph_module():
    st.header("Fraud Graph Intelligence")
    
    if st.button("Load Fraud Graph", use_container_width=True):
        try:
            resp = requests.get(f"{API_URL}/insights/fraud-graph", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                st.info(f"📄 {data.get('summary', 'Intelligence graph mapped.')}")
                
                raw_nodes = data.get("nodes", [])
                raw_edges = data.get("edges", [])
                
                # IMPROVEMENT 3: Interactive Graph Plotting
                nodes = []
                for n in raw_nodes:
                    # Dynamically color nodes based on their threat role
                    color = "#1f78b4" # Default blue
                    if n["role"] == "Scammer": color = "#e31a1c" # Red
                    elif n["role"] == "Victim": color = "#33a02c" # Green
                    elif n["role"] == "Money Mule": color = "#ff7f00" # Orange
                    
                    nodes.append(
                        Node(
                            id=n["id"],
                            label=f"{n['id']} ({n['role']})",
                            size=25,
                            color=color,
                            title=f"Flagged Alerts: {n['alerts']}"
                        )
                    )
                
                edges = []
                for e in raw_edges:
                    edges.append(
                        Edge(
                            source=e["source"],
                            target=e["target"],
                            label=e["relation"],
                            color="#aaaaaa"
                        )
                    )
                
                config = Config(
                    width="100%",
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                )
                
                # Render the interactive canvas
                st.subheader("Interactive Network Topology")
                agraph(nodes=nodes, edges=edges, config=config)
                
                # Retain raw data for auditing
                with st.expander("View Raw Datasets"):
                    st.subheader("Nodes")
                    st.dataframe(pd.DataFrame(raw_nodes), use_container_width=True)
                    st.subheader("Edges")
                    st.dataframe(pd.DataFrame(raw_edges), use_container_width=True)
            else:
                st.error(f"Backend error: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Unable to call backend: {e}")
