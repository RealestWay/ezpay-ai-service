from typing import Dict, Any, List

def calculate_scores(detections: Dict[str, bool], metadata: Dict[str, Any]) -> Dict[str, Any]:
    # Default category scores
    scores = {
        "aesthetics": 50,
        "power_systems": 50,
        "comfort_space": 50,
        "compound_environment": 50
    }
    
    flags = []
    recommendations = []

    # Aesthetics Score (Tiles, Fixtures, Cabinets)
    if detections.get("has_tiles"): scores["aesthetics"] += 20
    if detections.get("has_kitchen_cabinets"): scores["aesthetics"] += 20
    if detections.get("has_modern_fixtures"): scores["aesthetics"] += 10
    
    # Power Score (Solar, Generator)
    if detections.get("has_solar_panel"): 
        scores["power_systems"] += 40
    else:
        flags.append({"code": "NO_SOLAR", "severity": "medium", "description": "Solar/Inverter system not detected"})
        recommendations.append("Consider installing solar/inverter systems for better energy reliability")
        
    if detections.get("has_generator"): scores["power_systems"] += 10

    # Comfort Score (AC, Ventilation, Space)
    if detections.get("has_ac_unit"): 
        scores["comfort_space"] += 40
    else:
        flags.append({"code": "NO_AC", "severity": "high", "description": "AC units not detected in images"})
        recommendations.append("Install energy-efficient split AC units in all habitable rooms")

    # Compound Score (Interlock, Gate, Security)
    if detections.get("has_interlock_compound"): 
        scores["compound_environment"] += 30
    else:
        flags.append({"code": "NO_INTERLOCK", "severity": "medium", "description": "Compound area does not appear to be interlocked"})
        recommendations.append("Pave/Interlock the compound area to meet standard criteria")

    if detections.get("has_security_gate"): scores["compound_environment"] += 20

    # Overall weighted score
    overall_score = int(
        (scores["aesthetics"] * 0.25) +
        (scores["power_systems"] * 0.30) +
        (scores["comfort_space"] * 0.25) +
        (scores["compound_environment"] * 0.20)
    )
    
    # Cap at 100
    overall_score = min(overall_score, 100)
    for k in scores: scores[k] = min(scores[k], 100)

    # Status determination
    status = "needs_review"
    if overall_score >= 85:
        status = "passed"
    elif overall_score < 60:
        status = "failed"

    return {
        "overall_score": overall_score,
        "status": status,
        "confidence": 0.85, # Static for pre-trained model demo
        "category_scores": scores,
        "flags": flags,
        "recommendations": recommendations
    }
