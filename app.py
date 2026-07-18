
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.currency import classify_counterfeit
from modules.digital_arrest_scam import scan_for_scam
from modules.citizen_threat_shield import citizen_threat_shield
from modules.heatmap import generate_heatmap_data
from modules.fraud_graph import analyze_fraud_graph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILES = [os.path.join(BASE_DIR, "best.pt"), os.path.join(BASE_DIR, "best.onnx")]

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["USE_CPU"] = "1"

app = FastAPI(
    title="Fraud Detection Agent",
    description="A unified application for counterfeit currency verification, digital arrest scam detection, citizen threat shield, cyber heatmap, and fraud network intelligence.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def find_model_path() -> str:
    for model_path in MODEL_FILES:
        if os.path.exists(model_path):
            return model_path
    raise FileNotFoundError(
        "Model asset not found. Please place best.pt or best.onnx in the repository root."
    )

model = None


def get_model():
    global model
    if model is None:
        from ultralytics import YOLO

        model = YOLO(find_model_path(), task="classify")
    return model


@app.get("/")
async def root():
    return {
        "status": "Online",
        "engine": "Unified Fraud Detection Agent",
        "model": os.path.basename(find_model_path()),
    }


@app.post("/predict/currency")
async def predict_currency(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/jpg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Upload must be an image file.")
    image_bytes = await file.read()
    return classify_counterfeit(image_bytes, get_model())


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
async def insights_heatmap():
    return generate_heatmap_data()


@app.get("/insights/fraud-graph")
async def insights_fraud_graph():
    return analyze_fraud_graph()
