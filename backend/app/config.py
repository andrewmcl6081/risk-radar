from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  # General
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Risk Radar"
  
  # Models
  HF_TOKEN: Optional[str] = None
  MODEL_CACHE_DIR: str = "./model_cache"
  
  # News
  NEWSAPI_KEY: Optional[str] = None
  
  model_config = {
    "env_file": ".env",
    "case_sensitive": True,
  }

@lru_cache()
def get_settings() -> Settings:
  return Settings()