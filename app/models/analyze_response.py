from pydantic import BaseModel
from typing import List, Optional, Dict

class CategoryScores(BaseModel):
    aesthetics: int
    power_systems: int
    comfort_space: int
    compound_environment: int

class Flag(BaseModel):
    code: str
    severity: str
    description: str

class ConsistencyReport(BaseModel):
    ocr_match: str
    detail_match: str

class AnalyzeResponse(BaseModel):
    listing_id: str
    overall_score: int
    status: str
    confidence: float
    category_scores: CategoryScores
    detected_objects: Dict[str, bool]
    ocr_text: Optional[str] = None
    flags: List[Flag]
    recommendations: List[str]
    consistency_report: Optional[ConsistencyReport] = None
