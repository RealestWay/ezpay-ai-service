import httpx
import os
from PIL import Image
from io import BytesIO
from typing import List, Dict

async def download_images(image_urls_dict: Dict[str, List[str]]) -> Dict[str, List[Image.Image]]:
    downloaded_images = {}
    async with httpx.AsyncClient() as client:
        for category, urls in image_urls_dict.items():
            images = []
            for url in urls:
                try:
                    response = await client.get(url, timeout=10.0)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        images.append(img)
                except Exception as e:
                    print(f"Error downloading image {url}: {e}")
            downloaded_images[category] = images
    return downloaded_images
