import io
import re
import ast
from typing import Optional

import numpy as np
from PIL import Image, ImageOps
import pytesseract

FAKE_TEXT_BLACKLIST = [r"\bmanoranjan\b", r"\bchildren\b", r"\bfun\b", r"\bchuran\b", r"\bcoupon\b", r"\bpoints\b", r"\bschool\b"]
VALID_DENOMINATIONS = {10, 20, 50, 100, 200, 500, 2000}

def preprocess_image(image: Image.Image, imgsz=640) -> np.ndarray:
    width, height = image.size
    scale = imgsz / min(width, height)
    new_w, new_h = int(width * scale), int(height * scale)
    
    img_resized = image.resize((new_w, new_h), Image.BILINEAR)
    
    left = (new_w - imgsz) / 2
    top = (new_h - imgsz) / 2
    img_cropped = img_resized.crop((left, top, left + imgsz, top + imgsz))
    
    img_arr = np.array(img_cropped, dtype=np.float32) / 255.0
    img_arr = img_arr.transpose(2, 0, 1)
    img_arr = np.expand_dims(img_arr, axis=0)
    return img_arr

def extract_ocr_denomination(raw_text: str) -> Optional[int]:
    # Process text directly to skip redundant engine calls
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

def classify_counterfeit(image_bytes: bytes, session) -> dict:
    raw_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = ImageOps.exif_transpose(raw_image)

    # 1. Image Preprocessing for ONNX
    input_data = preprocess_image(image, imgsz=640)
    
    # 2. Run Accelerated ONNX Session
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    probs_arr = session.run([output_name], {input_name: input_data})[0][0]

    # 3. Retrieve Class Metadata
    meta = session.get_modelmeta().custom_metadata_map
    names_dict = ast.literal_eval(meta.get('names', '{}'))

    # 4. Top Visual Prediction Evaluation
    class_id = int(np.argmax(probs_arr))
    confidence = float(probs_arr[class_id])
    raw_class = names_dict.get(class_id, f"class_{class_id}")

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

    # 5. SINGLE-PASS SPEED-OPTIMIZED OCR ENGINE
    extracted_text = ""
    try:
        # Performance booster: Create a fast, lightweight thumbnail for OCR tracking
        ocr_target = image.copy()
        ocr_target.thumbnail((1024, 1024))
        extracted_text = pytesseract.image_to_string(ocr_target, config="--psm 6").lower()
    except Exception:
        override_warning = "OCR processing unavailable. Classification based on visual model output only."

    # Denomination Verification (Reusing string output)
    ocr_denomination = None
    if extracted_text:
        ocr_denomination = extract_ocr_denomination(extracted_text)
        
    if ocr_denomination and predicted_denom and ocr_denomination != predicted_denom:
        if confidence < 0.90:
            final_status = "UNCERTAIN"
            override_warning = f"OCR detected a different denomination (₹{ocr_denomination}) than the model's prediction (₹{predicted_denom}). Please verify."
        else:
            override_warning = f"OCR detected ₹{ocr_denomination}, while the model predicted ₹{predicted_denom}. Verification recommended."

    # Blacklist Toy-Note Validation Filter (Reusing same string output)
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
