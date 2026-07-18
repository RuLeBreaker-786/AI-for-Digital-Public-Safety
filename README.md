# AI-for-Digital-Public-Safety
## Overview

A unified AI-powered platform for detecting and preventing financial fraud and digital threats. The agent integrates multiple detection modules—counterfeit currency verification, digital scam analysis, citizen threat assessment, geospatial hotspot intelligence, and fraud network analysis—into a single, easy-to-use interface.

## Features

### 1. Counterfeit Currency Detection
- AI-powered visual classification using YOLO
- OCR-based text extraction and validation
- Confidence scoring and denomination verification
- Support for multiple currency formats

### 2. Digital Arrest Scam Detection
- Pattern-based scam keyword analysis
- Risk scoring for suspicious messages
- Detection of urgency tactics and payment pressure
- Actionable threat recommendations

### 3. Citizen Threat Shield
- Multi-channel threat assessment (SMS, WhatsApp, Email, IVR, Phone)
- Regional context analysis
- Risk level categorization with tailored guidance
- Integration with emergency response recommendations

### 4. Cyber Heatmap Intelligence
- Satellite-style geospatial visualization
- Real-time fraud hotspot mapping across India
- Severity-based incident clustering
- Interactive location-based threat intelligence

### 5. Fraud Graph Intelligence
- Network-based fraud pattern analysis
- Relationship mapping between actors and incidents
- Fraud ring identification
- Connection strength visualization

## Architecture

- **Backend**: FastAPI REST API (`app.py`) providing real-time analysis endpoints
- **Frontend**: Streamlit web interface (`ui.py`) for intuitive user interaction
- **ML Models**: Pre-trained YOLO weights for currency classification
- **Data Processing**: Modular detection engines with independent scalability

## Installation

```bash
# Clone the repository
git clone https://github.com/RuLeBreaker-786/fraud_Detection_Agent.git
cd fraud_Detection_Agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Terminal 1: Run Backend
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Terminal 2: Run Frontend
```bash
streamlit run ui.py
```

Open your browser to `http://localhost:8501` and select a module from the sidebar.

## Project Structure

```
fraud_Detection_Agent/
├── app.py                      # FastAPI backend
├── ui.py                       # Streamlit frontend
├── requirements.txt            # Python dependencies
├── best.pt / best.onnx        # Pre-trained ML models
├── modules/
│   ├── currency.py            # Currency detection logic
│   ├── digital_arrest_scam.py # Scam detection engine
│   ├── citizen_threat_shield.py # Threat assessment
│   ├── heatmap.py             # Geospatial hotspots
│   └── fraud_graph.py         # Network analysis
└── ui_modules/
    ├── currency_ui.py
    ├── scam_ui.py
    ├── citizen_threat_shield_ui.py
    ├── heatmap_ui.py
    └── fraud_graph_ui.py
```

## API Endpoints

- `POST /predict/currency` — Verify counterfeit currency from image
- `POST /predict/scam` — Analyze scam message text
- `POST /predict/threat` — Assess citizen threat report
- `GET /insights/heatmap` — Retrieve fraud hotspot data
- `GET /insights/fraud-graph` — Get fraud network intelligence

## Deployment

Recommended platforms for free/easy deployment:

- **Streamlit Community Cloud** — Frontend hosting
- **Render** — Full-stack deployment (backend + frontend)
- **Railway** — Simple container-based deployment

## Requirements

- Python 3.8+
- PyTorch / YOLO for ML inference
- FastAPI + Uvicorn for backend
- Streamlit for web interface
- Folium for geospatial visualization

## License

Open source. Use responsibly for fraud prevention and public safety.

## Notes

- Large model files (`best.pt`, `best.onnx`) are tracked with Git LFS for deployment compatibility
- The backend requires both models available in the repository root
- API responses include confidence scores and detailed reasoning for each detection
- All modules operate independently and can be extended with custom logic
