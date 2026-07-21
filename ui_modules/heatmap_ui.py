import os
import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render_heatmap_module():
    st.header("Cyber Heatmap Intelligence")
    st.caption("Interactive command-center geospatial view with district-level filtering & live incident logging.")

    # 1. State & Severity Control Panel
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox(
            "Filter by State / Region",
            ["All", "Delhi NCR", "Maharashtra", "Karnataka", "West Bengal", "Telangana", "Tamil Nadu", "Jharkhand", "Bihar"]
        )
    with col2:
        selected_severity = st.selectbox("Filter by Threat Severity", ["All", "High", "Medium", "Low"])

    # Fetch dynamic heatmap data from backend
    try:
        resp = requests.get(
            f"{API_URL}/insights/heatmap",
            params={"state": selected_state, "severity": selected_severity},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            hotspots = data.get("hotspots", [])
            
            st.info(f"📍 **Active Incidents Displayed:** {data.get('total_incidents', 0)}")

            if hotspots:
                # 2. Dynamic Auto-Centering and Zooming
                lats = [h["lat"] for h in hotspots if "lat" in h]
                lons = [h["lon"] for h in hotspots if "lon" in h]

                if selected_state != "All" and lats and lons:
                    map_center = [sum(lats) / len(lats), sum(lons) / len(lons)]
                    zoom_level = 9  # Deep district zoom
                else:
                    map_center = [22.9734, 78.6569]
                    zoom_level = 5  # All-India zoom

                m = folium.Map(location=map_center, zoom_start=zoom_level, control_scale=True)

                folium.TileLayer(
                    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                    attr="Esri World Imagery",
                    name="Satellite",
                    overlay=False,
                ).add_to(m)

                folium.TileLayer("OpenStreetMap", name="Street").add_to(m)

                severity_colors = {"High": "#ff4b4b", "Medium": "#ffa726", "Low": "#4caf50"}

                for hotspot in hotspots:
                    lat, lon = hotspot.get("lat"), hotspot.get("lon")
                    if lat is None or lon is None:
                        continue

                    severity = hotspot.get("severity", "Medium")
                    color = severity_colors.get(severity, "#1f77b4")
                    
                    popup_html = f"""
                    <div style="font-family: sans-serif; width: 220px;">
                        <h4 style="margin: 0 0 5px 0;">{hotspot.get('location', 'Unknown')}</h4>
                        <b>State:</b> {hotspot.get('state', 'N/A')}<br>
                        <b>Type:</b> {hotspot.get('type', 'Unknown')}<br>
                        <b>Severity:</b> <span style="color: {color}; font-weight: bold;">{severity}</span><br>
                        <hr style="margin: 5px 0;">
                        <small>{hotspot.get('notes', '')}</small>
                    </div>
                    """

                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=9,
                        popup=popup_html,
                        tooltip=f"{hotspot.get('location')} ({severity})",
                        color=color,
                        weight=2,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.85,
                    ).add_to(m)

                folium.LayerControl().add_to(m)
                st_folium(m, width=1400, height=600, returned_objects=[])

                # Data Table View
                with st.expander("View Raw Geospatial Table"):
                    df = pd.DataFrame(hotspots)
                    st.dataframe(df[["location", "state", "type", "severity", "notes", "lat", "lon"]], use_container_width=True)

        else:
            st.error(f"Backend error: {resp.status_code} {resp.text}")
    except Exception as e:
        st.error(f"Unable to connect to heatmap backend service: {e}")

    # 3. Dynamic Incident Submission Form (Demonstrates Live Data Ingestion)
    with st.expander("🚨 Log New Geospatial Incident (Live Dynamic Update)"):
        st.subheader("Report Real-Time Field Incident")
        with st.form("new_incident_form"):
            f_location = st.text_input("Location Name (e.g., Connaught Place Phase II)", value="New District Cyber Cell")
            f_state = st.selectbox("State", ["Delhi NCR", "Maharashtra", "Karnataka", "West Bengal", "Telangana", "Tamil Nadu", "Jharkhand", "Bihar"])
            f_type = st.selectbox("Incident Type", ["Counterfeit seizure", "Digital scam cluster", "Cyber payment fraud", "Identity theft network"])
            f_severity = st.selectbox("Severity Level", ["High", "Medium", "Low"])
            c1, c2 = st.columns(2)
            with c1:
                f_lat = st.number_input("Latitude", value=28.6139, format="%.4f")
            with c2:
                f_lon = st.number_input("Longitude", value=77.2090, format="%.4f")
            f_notes = st.text_area("Incident Context / Notes", value="New fake currency shipment flagged by inter-district patrol.")
            
            submit_btn = st.form_submit_button("Submit Incident to Map")

            if submit_btn:
                try:
                    p_resp = requests.post(
                        f"{API_URL}/insights/heatmap/report",
                        data={
                            "location": f_location,
                            "state": f_state,
                            "incident_type": f_type,
                            "severity": f_severity,
                            "lat": f_lat,
                            "lon": f_lon,
                            "notes": f_notes,
                        },
                        timeout=15
                    )
                    if p_resp.status_code == 200:
                        st.success("✅ Incident logged dynamically! Refreshing map...")
                        st.rerun()
                    else:
                        st.error(f"Failed to log incident: {p_resp.text}")
                except Exception as ex:
                    st.error(f"Error submitting incident: {ex}")
