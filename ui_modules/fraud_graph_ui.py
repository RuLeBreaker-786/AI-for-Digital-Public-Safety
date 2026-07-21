import os
import json
import streamlit as st
import requests
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render_fraud_graph_module():
    st.header("Fraud Graph Intelligence")
    st.caption("Interactive Graph AI mapping transaction metadata, scammer infrastructure, and money mule networks.")

    # 1. Campaign Selection & Filtering Controls
    c1, c2 = st.columns([2, 1])
    with c1:
        campaign_option = st.selectbox(
            "Select Investigation Case / Fraud Ring",
            options=["digital_arrest", "counterfeit_ring", "loan_extortion"],
            format_func=lambda x: {
                "digital_arrest": "🚨 Digital Arrest Syndicate (Delhi-NCR & Mewat Ring)",
                "counterfeit_ring": "💵 Multi-State Counterfeit Currency Syndicate",
                "loan_extortion": "📱 Instant APK Loan Extortion Network"
            }[x]
        )
    with c2:
        role_filter = st.selectbox(
            "Filter Network Node Role",
            ["All", "Scammer", "Money Mule", "Bank Account", "Device", "Victim"]
        )

    # Fetch Data from Backend
    try:
        resp = requests.get(
            f"{API_URL}/insights/fraud-graph",
            params={"campaign": campaign_option, "role": role_filter},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()

            # 2. Key Intelligence Metrics Cards
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Financial Exposure", data.get("exposure", "N/A"))
            m2.metric("Flagged Mule Accounts", data.get("mules_count", 0))
            m3.metric("Linked Jurisdictions", data.get("jurisdictions", "N/A"))
            m4.metric("Active Network Nodes", len(data.get("nodes", [])))

            st.divider()

            raw_nodes = data.get("nodes", [])
            raw_edges = data.get("edges", [])

            if raw_nodes:
                # 3. Interactive Graph Visualization
                nodes = []
                role_colors = {
                    "Scammer": "#e31a1c",     # Red
                    "Money Mule": "#ff7f00",  # Orange
                    "Bank Account": "#33a02c", # Green
                    "Device": "#984ea3",       # Purple
                    "Victim": "#1f78b4"        # Blue
                }

                for n in raw_nodes:
                    node_role = n.get("role", "Victim")
                    color = role_colors.get(node_role, "#1f78b4")
                    
                    nodes.append(
                        Node(
                            id=n["id"],
                            label=f"{n['label']}\n({n['id']})",
                            size=30 if node_role in ["Scammer", "Money Mule"] else 22,
                            color=color,
                            title=f"Role: {node_role} | Alerts: {n.get('alerts', 0)}\nContext: {n.get('details', '')}"
                        )
                    )

                edges = []
                for e in raw_edges:
                    edges.append(
                        Edge(
                            source=e["source"],
                            target=e["target"],
                            label=e.get("relation", ""),
                            color="#888888",
                            width=2
                        )
                    )

                # Adjusted Physics & Canvas Dimensions to Spread Graph Cleanly
                config = Config(
                    width="100%",
                    height=550,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6",
                    solver="forceAtlas2Based",
                    forceAtlas2Based={"gravitationalConstant": -50, "centralGravity": 0.01, "springLength": 100, "springConstant": 0.08}
                )

                st.subheader("Interactive Network Topology")
                
                # Legend Bar
                st.markdown(
                    "**Legend:** 🔴 **Scammer** | 🟧 **Money Mule** | 🟩 **Bank Account** | 🟪 **Device** | 🟦 **Victim**"
                )
                
                agraph(nodes=nodes, edges=edges, config=config)

                # 4. Export Court-Admissible Intelligence Package
                st.divider()
                st.subheader("Actionable Law Enforcement Export")
                
                export_json = json.dumps(data, indent=2)
                st.download_button(
                    label="📄 Export Court-Admissible Evidence Package (JSON)",
                    data=export_json,
                    file_name=f"evidence_package_{campaign_option}.json",
                    mime="application/json",
                    use_container_width=True
                )

                # Raw Datasets
                with st.expander("View Underlying Node & Edge Datasets"):
                    st.subheader("Network Nodes")
                    st.dataframe(pd.DataFrame(raw_nodes), use_container_width=True)
                    st.subheader("Transaction Edges")
                    st.dataframe(pd.DataFrame(raw_edges), use_container_width=True)
            else:
                st.warning("No graph nodes found matching the selected filter criteria.")

        else:
            st.error(f"Backend error: {resp.status_code} {resp.text}")
    except Exception as e:
        st.error(f"Unable to connect to fraud graph backend service: {e}")
