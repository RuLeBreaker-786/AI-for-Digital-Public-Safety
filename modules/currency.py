import io
import re
from typing import Optional

from PIL import Image, ImageOps
import pytesseract

FAKE_TEXT_BLACKLIST = [r"\bmanoranjan\b", r"\bchildren\b", r"\bfun\b", r"\bchuran\b", r"\bcoupon\b", r"\bpoints\b", r"\bschool\b"]
VALID_DENOMINATIONS = {10, 20, 50, 100, 200, 500, 2000}

def extract_ocr_denomination(raw_text: str) -> Optional[int]:
    processed_text = raw_text.replace("₹", " ").replace("rs", " ")
    processed_text = re.sub(r"[^0-9a-z\s]", " ", processed_text)

    match = re.search(r"\b(10|20|50|100|200|500|2000)\b", processed_text)
    if match:
        value = int(match.group(1))
        return value if value in VALID_DENOMINATIONS else None

    text_map = {
        r"\bten\b": 10, r"\btwenty\b": 20, r"\bfifty\b": 50,
        r"\bhundred\b": 100, r"\btwo hundred\b": 200,
        r"\bfive hundred\b": 500, r"\btwo thousand\b": 2000,
    }
    for pattern, value in text_map.items():
        if re.search(pattern, processed_text):
            return value
    return None

def classify_counterfeit(image_bytes: bytes, model) -> dict:
    raw_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = ImageOps.exif_transpose(raw_image)

    # 1. Native YOLO Inference (fixes accuracy discrepancies)
    results = model.predict(image, imgsz=640, device="cpu", verbose=False)
    result = results[0]
    
    # 2. Extract Top Visual Prediction
    class_id = int(result.probs.top1)
    confidence = float(result.probs.top1conf.item())
    raw_class = result.names[class_id]

    if "_" in raw_class:
        denom, status = raw_class.split("_", 1)
    else:
        denom, status = "Unknown", raw_class

    predicted_denom = int(denom) if denom.isdigit() else None
    final_status = "LEGITIMATE" if status.lower() == "real" else "COUNTERFEIT"
    override_warning: Optional[str] = None

    if confidence < 0.65:
        final_status = "UNCERTAIN"
        override_warning = "Low AI confidence. Ensure the note image is clear, well-lit, and fully visible."

    # 3. OCR Text Engine Integration
    extracted_text = ""
    try:
        ocr_target = image.copy()
        ocr_target.thumbnail((1024, 1024))
        extracted_text = pytesseract.image_to_string(ocr_target, config="--psm 6").lower()
    except Exception:
        override_warning = "OCR processing unavailable. Classification based on visual model output only."

    ocr_denomination = None
    if extracted_text:
        ocr_denomination = extract_ocr_denomination(extracted_text)
        
    if ocr_denomination and predicted_denom and ocr_denomination != predicted_denom:
        if confidence < 0.90:
            final_status = "UNCERTAIN"
            override_warning = f"OCR detected a different denomination (₹{ocr_denomination}) than the model's prediction (₹{predicted_denom}). Please verify."
        else:
            override_warning = f"OCR detected ₹{ocr_denomination}, while the model predicted ₹{predicted_denom}. Verification recommended."

    if extracted_text and final_status in ["LEGITIMATE", "UNCERTAIN"]:
        for pattern in FAKE_TEXT_BLACKLIST:
            if re.search(pattern, extracted_text):
                final_status = "COUNTERFEIT"
                override_warning = "OCR security override: suspicious toy-note text detected."
                confidence = 0.99
                break

    display_denom = f"₹{predicted_denom}" if predicted_denom else (f"₹{ocr_denomination}" if ocr_denomination else "Unknown")

    return {
        "denomination": display_denom,
        "status": final_status,
        "confidence": round(confidence * 100, 2),
        "raw_class": raw_class,
        "model_denomination": f"₹{denom}" if denom.isdigit() else denom,
        "ocr_denomination": f"₹{ocr_denomination}" if ocr_denomination else None,
        "override_warning": override_warning,
    }
