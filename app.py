import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import onnxruntime as ort

from modules.currency import classify_counterfeit
from modules.digital_arrest_scam import scan_for_scam
from modules.citizen_threat_shield import citizen_threat_shield
from modules.heatmap import generate_heatmap_data, add_hotspot_incident
from modules.fraud_graph import analyze_fraud_graph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.onnx")

app = FastAPI(
    title="Fraud Detection Agent",
    description="A unified application for fraud detection.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Missing model asset: {MODEL_PATH}")

session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])

@app.head("/")
@app.get("/")
async def root():
    return {
        "status": "Online",
        "engine": "Unified Fraud Detection Agent (ONNX Dynamic Tier)",
    }

@app.post("/predict/currency")
async def predict_currency(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Upload must be an image file.")
    image_bytes = await file.read()
    return classify_counterfeit(image_bytes, session)

@app.post("/predict/scam")
async def predict_scam(message: str = Form(...)):
    if not message.strip():
        raise HTTPException(status_code=400, detail="Scam text is required.")
    return scan_for_scam(message)

@app.post("/predict/threat")
async def predict_threat(
    channel: str = Form(...),
    region: str = Form(...),
    description: str = Form(...),
):
    if not description.strip():
        raise HTTPException(status_code=400, detail="Threat description is required.")
    return citizen_threat_shield(channel, region, description)

@app.get("/insights/heatmap")
async def insights_heatmap(state: str = "All", severity: str = "All"):
    return generate_heatmap_data(state_filter=state, severity_filter=severity)

@app.post("/insights/heatmap/report")
async def report_heatmap_incident(
    location: str = Form(...),
    state: str = Form(...),
    incident_type: str = Form(...),
    severity: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    notes: str = Form(...),
):
    return add_hotspot_incident(location, state, incident_type, severity, lat, lon, notes)

@app.get("/insights/fraud-graph")
async def insights_fraud_graph():
    return analyze_fraud_graph()
