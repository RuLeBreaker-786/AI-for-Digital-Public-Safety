import os
import streamlit as st
import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

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

def render_heatmap_module():
    st.header("Cyber Heatmap Intelligence")
    st.caption("Interactive command-center geospatial view across all 28 States & 8 Union Territories.")

    # 1. Filter Control Panel
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_state = st.selectbox("Select State / UT", ALL_INDIA_REGIONS)
    with col2:
        selected_type = st.selectbox(
            "Incident Type", 
            ["All", "Counterfeit seizure", "Digital scam cluster", "Cyber payment fraud", "Identity theft network", "Counterfeit currency report", "Fake note circulation"]
        )
    with col3:
        selected_severity = st.selectbox("Severity Level", ["All", "High", "Medium", "Low"])
    with col4:
        map_style = st.selectbox("Map View Mode", ["Satellite Map", "Density HeatMap View", "Street Map"])

    # 2. Fetch Filtered Data from Backend
    try:
        resp = requests.get(
            f"{API_URL}/insights/heatmap",
            params={
                "state": selected_state,
                "severity": selected_severity,
                "incident_type": selected_type,
            },
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            hotspots = data.get("hotspots", [])

            st.info(f"📍 **Matching Intelligence Hotspots:** {len(hotspots)}")

            if hotspots:
                # Calculate dynamic centroid for auto-zoom
                lats = [h["lat"] for h in hotspots if "lat" in h]
                lons = [h["lon"] for h in hotspots if "lon" in h]

                if selected_state != "All" and lats and lons:
                    map_center = [sum(lats) / len(lats), sum(lons) / len(lons)]
                    zoom_level = 8  # Zoom directly into selected State/UT
                else:
                    map_center = [22.9734, 78.6569]
                    zoom_level = 5  # Pan-India view

                # Initialize Base Map
                m = folium.Map(location=map_center, zoom_start=zoom_level, control_scale=True)

                # Map Tile Layer Selection
                if map_style == "Satellite Map":
                    folium.TileLayer(
                        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                        attr="Esri World Imagery",
                        name="Satellite",
                        overlay=False,
                    ).add_to(m)
                else:
                    folium.TileLayer("OpenStreetMap", name="Street").add_to(m)

                # Mode A: Density HeatMap View
                if map_style == "Density HeatMap View":
                    heat_data = [[h["lat"], h["lon"], 1.0 if h.get("severity") == "High" else 0.6] for h in hotspots if "lat" in h and "lon" in h]
                    HeatMap(heat_data, radius=25, blur=15, min_opacity=0.4).add_to(m)

                # Mode B & C: Pin Markers + Information Popups
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
                        <b>State/UT:</b> {hotspot.get('state', 'N/A')}<br>
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
                with st.expander("View Intelligence Dataset Table"):
                    df = pd.DataFrame(hotspots)
                    st.dataframe(df[["location", "state", "type", "severity", "notes", "lat", "lon"]], use_container_width=True)
            else:
                st.warning("No incidents found matching the selected filter criteria.")

        else:
            st.error(f"Backend error: {resp.status_code} {resp.text}")
    except Exception as e:
        st.error(f"Unable to connect to heatmap backend service: {e}")

    # 3. Dynamic Incident Submission Form
    with st.expander("🚨 Log New Field Incident (Live Real-Time Ingestion)"):
        st.subheader("Report Real-Time Incident")
        with st.form("new_incident_form"):
            f_location = st.text_input("Location Name", value="Cyber Crime Cell")
            f_state = st.selectbox("State / UT", ALL_INDIA_REGIONS[1:])
            f_type = st.selectbox("Incident Type", ["Counterfeit seizure", "Digital scam cluster", "Cyber payment fraud", "Identity theft network"])
            f_severity = st.selectbox("Severity Level", ["High", "Medium", "Low"])
            c1, c2 = st.columns(2)
            with c1:
                f_lat = st.number_input("Latitude", value=28.6139, format="%.4f")
            with c2:
                f_lon = st.number_input("Longitude", value=77.2090, format="%.4f")
            f_notes = st.text_area("Incident Context / Notes", value="New cybercrime cluster reported by regional authorities.")

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
