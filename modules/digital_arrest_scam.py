import re

SCAM_KEYWORDS = [
    ("arrest", 24),
    ("police", 22),
    ("court", 20),
    ("fine", 18),
    ("pay immediately", 24),
    ("verify your account", 20),
    ("verify account", 18),
    ("upi", 22),
    ("paytm", 18),
    ("phonepe", 18),
    ("western union", 18),
    ("your account is suspended", 24),
    ("account suspended", 24),
    ("suspended", 18),
    ("call from officer", 22),
    ("case filed", 24),
    ("legal notice", 23),
    ("investigation", 16),
    ("refund", 14),
    ("one-time password", 22),
    ("otp", 20),
    ("scan qr", 18),
    ("click link", 18),
    ("click the link", 18),
    ("login details", 18),
    ("urgent", 16),
    ("immediately", 16),
    ("now", 12),
    ("fake note", 28),
    ("fake currency", 24),
    ("counterfeit", 22),
    ("url", 16),
    ("link", 14),
    ("verify", 12),
    ("bank", 10),
    ("officer", 14),
]

THREAT_ADVICE = {
    "low": "No immediate threat detected. Stay cautious and verify unsolicited contacts.",
    "medium": "Suspicious activity identified. Do not share sensitive details and report the interaction.",
    "high": "High-risk scam behavior found. Stop communication immediately and file a complaint with local authorities.",
}


def scan_for_scam(text: str) -> dict:
    lower_text = text.lower()
    matched = []
    score = 0

    for phrase, weight in SCAM_KEYWORDS:
        if phrase in lower_text and phrase not in matched:
            matched.append(phrase)
            score += weight

    if re.search(r"https?://\S+", lower_text):
        score += 18
        if "url" not in matched:
            matched.append("url/link")

    if "fake" in lower_text and ("note" in lower_text or "currency" in lower_text or "money" in lower_text):
        score += 10

    if ("pay" in lower_text or "send" in lower_text) and ("immediately" in lower_text or "now" in lower_text):
        score += 12

    if any(term in lower_text for term in ["upi", "otp", "paytm", "phonepe"]):
        score += 10

    if any(term in lower_text for term in ["arrest", "police", "court", "case filed", "legal notice", "account suspended", "suspended"]):
        score += 8

    score = min(100, score)

    if score >= 75 or (
        score >= 65 and ("fake" in lower_text and ("note" in lower_text or "currency" in lower_text))
    ):
        level = "high"
        summary = "High-risk digital arrest scam pattern detected."
    elif score >= 45:
        level = "medium"
        summary = "Medium-risk suspicious activity found."
    else:
        level = "low"
        summary = "No strong scam indicators found."

    return {
        "score": score,
        "risk_level": level,
        "summary": summary,
        "matched_terms": matched,
        "advice": THREAT_ADVICE[level],
    }


def citizen_threat_shield(channel: str, region: str, description: str) -> dict:
    result = scan_for_scam(description)
    result["channel"] = channel
    result["region"] = region
    result["service"] = "Citizen Threat Shield"
    result["recommendation"] = (
        "Report immediately to local cyber cell and national helpline."
        if result["risk_level"] == "high"
        else "Treat this as urgent and verify before sharing any payment or personal details."
        if result["risk_level"] == "medium"
        else "Monitor closely and verify all requests before paying."
    )
    return result
