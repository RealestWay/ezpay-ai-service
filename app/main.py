from fastapi import FastAPI
from app.routers import analyze
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="EzPay AI Property Inspection Service")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ezpay-ai-service"}

app.include_router(analyze.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
