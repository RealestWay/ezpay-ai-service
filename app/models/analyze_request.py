from pydantic import BaseModel
from typing import List, Optional, Dict

class PropertyMetadata(BaseModel):
    typology: Optional[str] = None
    state: Optional[str] = None
    area: Optional[str] = None
    bedrooms: Optional[int] = 0
    bathrooms: Optional[int] = 0
    landlord_name: Optional[str] = None
    property_address: Optional[str] = None

class PropertyImages(BaseModel):
    exterior_shot: List[str] = []
    compound_road: List[str] = []
    power_system: List[str] = []
    interior_rooms: List[str] = []

class AnalyzeRequest(BaseModel):
    listing_id: str
    landlord_package: str
    images: PropertyImages
    property_metadata: PropertyMetadata
