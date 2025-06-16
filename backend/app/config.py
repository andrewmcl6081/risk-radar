from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Risk Radar"
  
  HF_TOKEN: Optional[str] = None
  MODEL_CACHE_DIR: str = "./model_cache"
  
  model_config = {
    "env_file": ".env",
    "case_sensitive": True,
  }

@lru_cache()
def get_settings() -> Settings:
  return Settings()