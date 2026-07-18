import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def render_currency_module():
    st.header("Counterfeit Currency Verification")
    uploaded_file = st.file_uploader("Upload a currency note image", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Note", use_column_width=True)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        with st.spinner("Analyzing currency image..."):
            try:
                resp = requests.post(f"{API_URL}/predict/currency", files=files, timeout=30)
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
                else:
                    st.error(f"Backend error: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Unable to call backend: {e}")
