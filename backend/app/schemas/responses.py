from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal
from datetime import datetime

class HealthCheckResponse(BaseModel):
  status: str
  models_loaded: bool
  name: Optional[str] = None
  error: Optional[str] = None
  timestamp: datetime = Field(default_factory=datetime.utcnow)