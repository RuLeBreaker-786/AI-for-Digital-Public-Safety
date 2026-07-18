import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

API_URL = "http://127.0.0.1:8000"


def render_heatmap_module():
    st.header("Cyber Heatmap Intelligence")
    st.caption("Satellite-style view of India with hotspot coordinates and incident context.")

    if st.button("Load Heatmap Insights", use_container_width=True):
        try:
            resp = requests.get(f"{API_URL}/insights/heatmap", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                hotspots = data.get("hotspots", [])

                if not hotspots:
                    st.warning("No hotspot data available at the moment.")
                    return

                df = pd.DataFrame(hotspots)
                st.dataframe(
                    df[["location", "type", "severity", "lat", "lon"]],
                    use_container_width=True,
                    hide_index=True,
                )

                india_center = [22.9734, 78.6569]
                m = folium.Map(location=india_center, zoom_start=5, tiles=None, control_scale=True)

                folium.TileLayer(
                    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                    attr="Esri World Imagery",
                    name="Satellite",
                    overlay=False,
                    control=True,
                ).add_to(m)

                folium.TileLayer(
                    tiles="OpenStreetMap",
                    name="Street",
                    control=True,
                ).add_to(m)

                severity_colors = {"High": "#ff4b4b", "Medium": "#ffa726", "Low": "#4caf50"}

                for hotspot in hotspots:
                    lat = hotspot.get("lat")
                    lon = hotspot.get("lon")
                    if lat is None or lon is None:
                        continue

                    severity = hotspot.get("severity", "Medium")
                    color = severity_colors.get(severity, "#1f77b4")
                    popup_html = f"""
                    <b>{hotspot.get('location', 'Unknown')}</b><br>
                    Type: {hotspot.get('type', 'Unknown')}<br>
                    Severity: {severity}<br>
                    Coordinates: {lat}, {lon}<br>
                    Notes: {hotspot.get('notes', '')}
                    """

                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=10,
                        popup=popup_html,
                        tooltip=f"{hotspot.get('location')} • {severity}",
                        color=color,
                        weight=2,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.85,
                    ).add_to(m)

                folium.LayerControl().add_to(m)
                st_folium(m, width=1400, height=700, returned_objects=["last_object_clicked"])
            else:
                st.error(f"Backend error: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Unable to call backend: {e}")
