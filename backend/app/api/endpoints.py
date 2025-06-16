from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
import logging

from app.schemas.responses import HealthCheckResponse
from app.core.models import get_sentiment_model
from app.config import get_settings
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
  try:
    model = get_sentiment_model()
    model_status = model.get_status()
    
    if model_status["initialized"]:
      return HealthCheckResponse(
        status="healthy",
        models_loaded=True,
        name=model_status["model_name"]
      )
    else:
      try:
        model.initialize()
        return HealthCheckResponse(
          status="healthy",
          models_loaded=True,
          name=model_status["model_name"]
        )
      except Exception as init_error:
        return HealthCheckResponse(
          status="unhealthy",
          models_loaded=False,
          name=model_status["model_name"],
          error=str(init_error)
        )
  except Exception as e:
    return HealthCheckResponse(
      status="error",
      models_loaded=False,
      error=str(e)
    )