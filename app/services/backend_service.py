# pyrefly: ignore [missing-import]
import httpx
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BackendService:
    def __init__(self):
        self.base_url = os.getenv("EZPAY_BACKEND_URL", "https://lightslategray-rabbit-263615.hostingersite.com/api")
    
    async def ping_backend(self) -> bool:
        """Verify that the backend is reachable."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health", timeout=5.0)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Backend health check failed: {e}")
            return False

    async def send_analysis_report(self, listing_id: str, report_data: Dict[str, Any]):
        """
        Send the analysis report back to the backend.
        This is useful for asynchronous processing or as a fallback.
        """
        url = f"{self.base_url}/ai-reports/{listing_id}/callback"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=report_data, timeout=10.0)
                if response.status_code == 200:
                    logger.info(f"Successfully pushed report for {listing_id} to backend.")
                else:
                    logger.error(f"Failed to push report to backend: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error sending report to backend: {e}")

backend_service = BackendService()
