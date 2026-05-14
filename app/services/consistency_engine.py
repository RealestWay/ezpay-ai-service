from typing import Dict, Any

def verify_consistency(ocr_text: str, metadata: Dict[str, Any]) -> Dict[str, str]:
    report = {
        "ocr_match": "Passed",
        "detail_match": "Passed"
    }

    # Search for landlord name in OCR text (fraud check)
    landlord_name = metadata.get('landlord_name', '').lower()
    if landlord_name and landlord_name not in ocr_text.lower():
        report["ocr_match"] = "Warning: Landlord name not found in documents"

    # Search for address in OCR text
    address = metadata.get('property_address', '').lower()
    if address and address[:10] not in ocr_text.lower():
        # Just check the start of address for common matches
        report["detail_match"] = "Warning: Address discrepancy detected"

    return report
