from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  # General
  API_V1_STR: str = "/api/v1"
  PROJECT_NAME: str = "Risk Radar"
  
  # Database
  POSTGRES_USER: str
  POSTGRES_PASSWORD: SecretStr
  POSTGRES_DB: str
  POSTGRES_HOST: str = "localhost"
  POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
  
  @property
  def DATABASE_URL(self) -> str:
    pwd = self.POSTGRES_PASSWORD.get_secret_value()
    return f"postgresql://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
  
  # Models
  HF_TOKEN: Optional[str] = None
  MODEL_CACHE_DIR: str = "./model_cache"
  
  # News
  NEWSAPI_KEY: Optional[str] = None
  FINNHUB_API_KEY: Optional[str] = None
  
  model_config = {
    "env_file": ".env",
    "case_sensitive": True,
  }

@lru_cache()
def get_settings() -> Settings:
  return Settings()