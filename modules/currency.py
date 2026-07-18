import io
import re
from typing import Optional

import numpy as np
from PIL import Image, ImageOps
from ultralytics import YOLO
import pytesseract
from pytesseract import TesseractNotFoundError

# Use regex word boundaries (\b) to prevent partial matches from triggering toy-note filters
FAKE_TEXT_BLACKLIST = [r"\bmanoranjan\b", r"\bchildren\b", r"\bfun\b", r"\bchuran\b", r"\bcoupon\b", r"\bpoints\b", r"\bschool\b"]
VALID_DENOMINATIONS = {10, 20, 50, 100, 200, 500, 2000}


def normalize_probs(result) -> np.ndarray:
    probs = result.probs
    if hasattr(probs, "top1") and hasattr(probs, "top1conf"):
        top1 = probs.top1
        top1conf = probs.top1conf
        class_id = int(top1.item()) if hasattr(top1, "item") else int(top1)
        confidence = float(top1conf.item()) if hasattr(top1conf, "item") else float(top1conf)
        arr = np.zeros(len(result.names), dtype=float)
        if 0 <= class_id < len(arr):
            arr[class_id] = confidence
        return arr

    if hasattr(probs, "data") and hasattr(probs.data, "numpy"):
        return probs.data.numpy()
    if hasattr(probs, "cpu"):
        return probs.cpu().numpy()
    return np.asarray(probs)


def get_top_prediction(result) -> tuple[str, float]:
    probs_arr = normalize_probs(result)
    class_id = int(np.argmax(probs_arr))
    confidence = float(probs_arr[class_id])
    class_name = result.names[class_id]
    return class_name, confidence


def extract_ocr_denomination(image: Image.Image) -> Optional[int]:
    try:
        raw_text = pytesseract.image_to_string(image, config="--psm 6").lower()
    except (TesseractNotFoundError, Exception):
        return None

    raw_text = raw_text.replace("₹", " ")
    raw_text = raw_text.replace("rs", " ")
    raw_text = re.sub(r"[^0-9a-z\s]", " ", raw_text)

    match = re.search(r"\b(10|20|50|100|200|500|2000)\b", raw_text)
    if match:
        value = int(match.group(1))
        return value if value in VALID_DENOMINATIONS else None

    text_map = {
        r"\bten\b": 10,
        r"\btwenty\b": 20,
        r"\bfifty\b": 50,
        r"\bhundred\b": 100,
        r"\btwo hundred\b": 200,
        r"\bfive hundred\b": 500,
        r"\btwo thousand\b": 2000,
    }
    for pattern, value in text_map.items():
        if re.search(pattern, raw_text):
            return value
    return None


def classify_counterfeit(image_bytes: bytes, model: YOLO) -> dict:
    raw_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = ImageOps.exif_transpose(raw_image)

    results = model.predict(image, imgsz=640, device="cpu", verbose=False)
    result = results[0]
    raw_class, confidence = get_top_prediction(result)

    if "_" in raw_class:
        denom, status = raw_class.split("_", 1)
    else:
        denom, status = "Unknown", raw_class

    predicted_denom = int(denom) if denom.isdigit() else None
    final_status = "LEGITIMATE" if status.lower() == "real" else "COUNTERFEIT"
    override_warning: Optional[str] = None
    ocr_denomination: Optional[int] = None

    if confidence < 0.65:
        final_status = "UNCERTAIN"
        override_warning = "Low AI confidence. Ensure the note image is clear, well-lit, and fully visible."

    ocr_denomination = extract_ocr_denomination(image)
    if ocr_denomination and predicted_denom and ocr_denomination != predicted_denom:
        if confidence < 0.90:
            final_status = "UNCERTAIN"
            override_warning = (
                f"OCR detected a different denomination (₹{ocr_denomination}) than the model's prediction (₹{predicted_denom}). "
                "Please verify the note under better lighting."
            )
        else:
            override_warning = (
                f"OCR detected ₹{ocr_denomination}, while the model predicted ₹{predicted_denom}. Verification is recommended."
            )

    try:
        probs_arr = normalize_probs(result)
    except Exception:
        probs_arr = None

    if probs_arr is not None and predicted_denom is not None:
        names = result.names
        if isinstance(names, dict):
            name_to_prob = {v: float(probs_arr[k]) for k, v in names.items() if k < len(probs_arr)}
        else:
            name_to_prob = {v: float(probs_arr[i]) for i, v in enumerate(names)}

        fake_key = f"{predicted_denom}_fake"
        real_key = f"{predicted_denom}_real"
        fake_prob = name_to_prob.get(fake_key, 0.0)
        real_prob = name_to_prob.get(real_key, 0.0)

        if fake_prob > real_prob + 0.10:
            final_status = "COUNTERFEIT"
            override_warning = (
                "The model detected a significantly higher fake probability for the predicted denomination. Please inspect the note carefully."
            )
            confidence = max(confidence, fake_prob)

        if ocr_denomination:
            ocr_candidates = [
                (name, prob) for name, prob in name_to_prob.items() if name.startswith(f"{ocr_denomination}_")
            ]
            if ocr_candidates:
                best_name, best_prob = max(ocr_candidates, key=lambda x: x[1])
                if best_prob >= 0.35 and best_prob >= confidence - 0.15:
                    if best_name != raw_class:
                        denom, status = best_name.split("_", 1)
                        predicted_denom = ocr_denomination
                        final_status = "LEGITIMATE" if status.lower() == "real" else "COUNTERFEIT"
                        confidence = max(confidence, best_prob)
                        override_warning = (
                            f"OCR denomination ₹{ocr_denomination} aligned with the model's best match {best_name}. Prediction updated for better accuracy."
                        )

    if final_status in ["LEGITIMATE", "UNCERTAIN"]:
        try:
            extracted_text = pytesseract.image_to_string(image).lower()
            for pattern in FAKE_TEXT_BLACKLIST:
                if re.search(pattern, extracted_text):
                    final_status = "COUNTERFEIT"
                    override_warning = "OCR security override: suspicious toy-note text detected."
                    confidence = max(confidence, 0.99)
                    break
        except TesseractNotFoundError:
            if not override_warning:
                override_warning = "OCR unavailable. Classification is based on visual model output only."
        except Exception:
            if not override_warning:
                override_warning = "OCR processing failed. Classification is based on visual model output only."

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
