from fastapi import APIRouter, HTTPException
import logging
from datetime import datetime

from app.schemas.responses import HealthCheckResponse
from app.config import get_settings
from app.core.sentiment import get_sentiment_model

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
  try:
    model = get_sentiment_model()
    status = model.get_status()
    name = status.get("model_name", "unknown")
    
    if not status.get("initialized", False):
      logger.info("Sentiment model not initialized. Attempting to initialize...")
      try:
        model.initialize()
        logger.info("Model initialized successfully during health check.")
      except Exception as init_err:
        logger.exception("Model failed to initialize.")
        return HealthCheckResponse(
          status="unhealthy",
          models_loaded=False,
          name=name,
          error=str(init_err),
        )
    
    return HealthCheckResponse(
      status="healthy",
      models_loaded=True,
      name=name,
    )
  except Exception as e:
    logger.exception("Unexpected error during health check.")
    return HealthCheckResponse(
      status="error",
      models_loaded=False,
      error=str(e),
    )