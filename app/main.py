from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
import stripe
from fastapi.staticfiles import StaticFiles
import os
import logging

from .database import SessionLocal, engine
from .models import Base
from .services import (
   SubscriptionService, 
   UsageTracker,
   FeatureGuard, 
   ExportService,
   IntegrationAuth,
   MeetingSummarizerService
)
from .config import Settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
settings = Settings()

# CORS middleware
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True, 
   allow_methods=["*"],
   allow_headers=["*"],
)

# Get absolute path to static directory
STATIC_DIR = os.path.abspath(os.path.join(os.getcwd(), "static"))
logger.info(f"Static directory path: {STATIC_DIR}")

# Serve static files
if os.path.exists(STATIC_DIR):
    logger.info(f"Static directory exists at {STATIC_DIR}")
    app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")), name="static")
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")
else:
    logger.error(f"Static directory not found at {STATIC_DIR}")

# API routes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api")
async def api_root():
    return JSONResponse({
        "status": "online",
        "message": "Meeting Summarizer API is running",
        "endpoints": {
            "process_meeting": "/api/process-meeting/",
            "health": "/api/health",
            "export": "/api/export/{format}",
            "oauth": "/api/oauth/callback/{provider}"
        }
    })

# Initialize services
subscription_service = SubscriptionService()
usage_tracker = UsageTracker()
feature_guard = FeatureGuard(subscription_service)
export_service = ExportService()
integration_auth = IntegrationAuth()
meeting_service = MeetingSummarizerService()

# Database dependency
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@app.post("/process-meeting/")
async def process_meeting(
   request: Request,
   file: UploadFile = File(...),
   db: Session = Depends(get_db)
):
   try:
       result = await meeting_service.process_meeting(file.file)
       await usage_tracker.track_meeting(request.state.user.id, {
           "duration": result.duration,
           "features": ["transcription", "summary"]
       }, db)
       return result
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
   return await subscription_service.handle_webhook(request)

@app.post("/export/{format}")
async def export_summary(
   format: str,
   summary_id: int,
   db: Session = Depends(get_db)
):
   summary = await meeting_service.get_summary(summary_id, db)
   return await export_service.export_summary(summary, format)

@app.get("/oauth/callback/{provider}")
async def oauth_callback(
   provider: str,
   code: str,
   db: Session = Depends(get_db)
):
   return await integration_auth.handle_oauth(provider, code, db)

# Catch-all route
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404)
    
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        logger.info(f"Serving {index_path}")
        return FileResponse(index_path)
    
    logger.error(f"index.html not found at {index_path}")
    return JSONResponse({
        "status": "error",
        "message": "Frontend not built",
        "path": index_path,
        "cwd": os.getcwd(),
        "dir_contents": os.listdir(".")
    })