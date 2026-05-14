import pytesseract
from PIL import Image
from typing import List, Dict

def process_ocr(images_dict: Dict[str, List[Image.Image]]) -> str:
    all_text = ""
    # Usually OCR is most relevant for documents, but we can scan everything for relevant keywords
    for category, images in images_dict.items():
        for img in images:
            try:
                # OCR the image
                text = pytesseract.image_to_string(img)
                all_text += f"\n--- {category} ---\n{text}"
            except Exception as e:
                print(f"OCR error: {e}")
                
    return all_text
