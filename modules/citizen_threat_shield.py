from modules.digital_arrest_scam import scan_for_scam


def citizen_threat_shield(channel: str, region: str, description: str) -> dict:
    result = scan_for_scam(description)
    result["channel"] = channel
    result["region"] = region
    result["service"] = "Citizen Threat Shield"
    result["recommendation"] = (
        "Report immediately to local cyber cell and national helpline." if result["risk_level"] == "high" else "Monitor closely and verify all requests before paying."
    )
    return result
