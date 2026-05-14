from fastapi import FastAPI
from app.routers import analyze
from dotenv import load_dotenv
import os

from app.services.backend_service import backend_service

load_dotenv()

app = FastAPI(title="EzPay AI Property Inspection Service")

@app.get("/health")
async def health_check():
    backend_status = await backend_service.ping_backend()
    return {
        "status": "healthy", 
        "service": "ezpay-ai-service",
        "backend_reachable": backend_status
    }

@app.get("/test-backend")
async def test_backend_connection():
    is_up = await backend_service.ping_backend()
    if is_up:
        return {"message": "Successfully connected to EzPay Backend"}
    return {"message": "Failed to connect to EzPay Backend", "url": backend_service.base_url}

app.include_router(analyze.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
