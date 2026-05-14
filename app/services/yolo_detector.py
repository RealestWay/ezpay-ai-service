from ultralytics import YOLO
from PIL import Image
from typing import List, Dict

# Load pre-trained YOLOv8n model (lightest for CPU/Render free plan)
model = YOLO('yolov8n.pt')

def detect_objects(images_dict: Dict[str, List[Image.Image]]) -> Dict[str, bool]:
    detections = {
        "has_ac_unit": False,
        "has_ceiling_fan": False,
        "has_modern_fixtures": False,
        "has_tiles": False,
        "has_solar_panel": False,
        "has_generator": False,
        "has_security_gate": False,
        "has_interlock_compound": False,
        "has_kitchen_cabinets": False,
        "has_modern_bathroom": False
    }

    # Simplified detection logic mapping COCO classes to our criteria
    # In a real production scenario, you would use more specific classes or fine-tuning
    for category, images in images_dict.items():
        for img in images:
            results = model(img, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    label = result.names[cls_id]
                    
                    # Mapping logic
                    if label in ['air conditioner']:
                        detections["has_ac_unit"] = True
                    if label in ['refrigerator', 'sink', 'oven']:
                        detections["has_kitchen_cabinets"] = True
                    if label in ['toilet']:
                        detections["has_modern_bathroom"] = True
                    
                    # Logic based on image category + detection
                    if category == 'compound_road':
                        detections["has_interlock_compound"] = True # Assume if they upload compound shot, we check texture in real usage
                    
                    if category == 'power_system':
                        # Check for panel-like shapes or specific labels if available
                        detections["has_solar_panel"] = True
                        
    return detections
