
from fastapi import FastAPI

from app.api.upload import router as upload_router


# Create FastAPI application
app = FastAPI(
    title="AI Investor Intelligence",
    description="AI-powered financial report analysis and investor chatbot",
    version="1.0.0"
)


# Register routers
app.include_router(upload_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Investor Intelligence",
        "status": "running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
