from fastapi import APIRouter, HTTPException
from app.models.analyze_request import AnalyzeRequest
from app.models.analyze_response import AnalyzeResponse, CategoryScores, ConsistencyReport, Flag
from app.services.image_downloader import download_images
from app.services.yolo_detector import detect_objects
from app.services.ocr_processor import process_ocr
from app.services.consistency_engine import verify_consistency
from app.services.scoring_engine import calculate_scores
import asyncio

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_property(request: AnalyzeRequest):
    try:
        # 1. Download images
        images_dict = await download_images(request.images.model_dump())
        
        # 2. Run detections (YOLO)
        detections = detect_objects(images_dict)
        
        # 3. Process OCR
        ocr_text = process_ocr(images_dict)
        
        # 4. Consistency check
        consistency = verify_consistency(ocr_text, request.property_metadata.model_dump())
        
        # 5. Calculate scores
        results = calculate_scores(detections, request.property_metadata.model_dump())
        
        # Map to response model
        return AnalyzeResponse(
            listing_id=request.listing_id,
            overall_score=results["overall_score"],
            status=results["status"],
            confidence=results["confidence"],
            category_scores=CategoryScores(**results["category_scores"]),
            detected_objects=detections,
            ocr_text=ocr_text,
            flags=[Flag(**f) for f in results["flags"]],
            recommendations=results["recommendations"],
            consistency_report=ConsistencyReport(**consistency)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
