from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
  # API Settings
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Risk Radar"
  
  HF_TOKEN: Optional[str] = None
  MODEL_CACHE_DIR: str = "./model_cache"
  
  class Config:
    env_file = ".env"
    case_sensitive = True

@lru_cache()
def get_settings():
  return Settings()
  