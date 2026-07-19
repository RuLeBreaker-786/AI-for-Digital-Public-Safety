import os
import streamlit as st
import requests
from PIL import Image, ImageEnhance

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render_currency_module():
    st.header("Counterfeit Currency Verification")
    uploaded_file = st.file_uploader("Upload a currency note image", type=["jpg", "jpeg", "png", "webp"])
    
    # IMPROVEMENT 2: UV/Fluorescence Simulation Toggle
    simulate_uv = st.checkbox("🔦 Simulate UV/Fluorescence Filter")
    
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        
        # Apply UV Simulation filter to the UI Image
        if simulate_uv:
            enhancer = ImageEnhance.Color(image)
            image_filtered = enhancer.enhance(2.5)  # Boost color saturation
            blue_overlay = Image.new("RGB", image_filtered.size, (50, 0, 150))
            image_filtered = Image.blend(image_filtered, blue_overlay, alpha=0.4) # Add purple/UV tint
            st.image(image_filtered, caption="Uploaded Note (UV Filter Simulated)", use_container_width=True)
        else:
            st.image(image, caption="Uploaded Note (Standard)", use_container_width=True)
        
        # Reset file pointer for the API request payload
        uploaded_file.seek(0)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        with st.spinner("Analyzing currency image..."):
            try:
                resp = requests.post(f"{API_URL}/predict/currency", files=files, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()

                    if data["status"] == "LEGITIMATE":
                        st.success(f"✅ GENUINE TENDER: {data['denomination']}")
                    elif data["status"] == "UNCERTAIN":
                        st.warning(f"⚠️ VERIFICATION UNCERTAIN: {data['denomination']}")
                    else:
                        st.error(f"🚨 COUNTERFEIT ALERT: {data['denomination']}")

                    if data.get("override_warning"):
                        st.warning(data["override_warning"])

                    st.progress(int(min(data["confidence"], 100)))

                    with st.expander("View classifier details"):
                        st.write("**Model prediction:**", data.get("raw_class", "Unknown"))
                        st.write("**Model denomination:**", data.get("model_denomination", "Unknown"))
                        st.write("**OCR denomination:**", data.get("ocr_denomination", "Not detected"))
                        st.write("**Confidence:**", f"{data.get('confidence', 0)}%")
                        st.write("**Status:**", data.get("status", "Unknown"))
                        if simulate_uv:
                            st.write("**UV Status:**", "Simulated security thread check applied.")
                else:
                    st.error(f"Backend error: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Unable to call backend: {e}")
