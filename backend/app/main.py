from logging_config import setup_logging
setup_logging()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import get_settings
from api.v1 import endpoints as v1_endpoints
from core.sentiment import get_sentiment_model
from db.connection import init_db

logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
  logger.info("Starting Risk Radar API...")
  
  try:
    # Initialize db
    init_db()
    logger.info("Database initialized")
    
    # Pre-load sentiment model
    model = get_sentiment_model()
    model.initialize()
    logger.info("Sentiment model loaded successfully")
  except Exception as e:
    logger.error(f"Failed to start services: {e}")
  
  yield
  
  # Shutdown
  logger.info("Shutting down Financial Sentiment API...")

app = FastAPI(
  title=settings.PROJECT_NAME,
  version="1.0.0",
  lifespan=lifespan
)

# Configure CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(
  v1_endpoints.router,
  prefix=f"{settings.API_V1_STR}/sentiment",
  tags=["sentiment"]
)

@app.get("/")
def root():
  return {
    "message": settings.PROJECT_NAME,
    "version": settings.model_config.get("version", "1.0.0"),
    "docs": "/docs",
    "health": f"{settings.API_V1_STR}/sentiment/health"
  }