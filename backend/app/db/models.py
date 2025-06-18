from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Index, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
import enum

class RatingAction(enum.Enum):
  UPGRADE = "upgrade"
  DOWNGRADE = "downgrade"
  REITERATE = "reiterate"
  INITIATE = "initiate"

class RatingGrade(enum.Enum):
  BUY = "buy"
  HOLD = "hold"
  SELL = "sell"
  STRONG_BUY = "strong buy"
  STRONG_SELL = "strong sell"

class Broker(Base):
  __tablename__ = "brokers"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), unique=True, nullable=False)
  company = Column(String(100))
  
  # Performance metrics
  hit_rate_30d = Column(Float)
  hit_rate_90d = Column(Float)
  total_ratings = Column(Integer, default=0)
  successful_ratings = Column(Integer, default=0)
  
  # Relationships
  ratings = relationship("AnalystRating", back_populates="broker")
  
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
class Stock(Base):
  __tablename__ = "stocks"
  
  id = Column(Integer, primary_key=True, index=True)
  symbol = Column(String(10), unique=True, nullable=False, index=True)
  company_name = Column(String(255))
  sector = Column(String(100))
  
  # Latest price info
  latest_price = Column(Float)
  price_updated_at = Column(DateTime)
  
  # Relationships
  ratings = relationship("AnalystRating", back_populates="stock")
  
  created_at = Column(DateTime, default=datetime.utcnow)

class AnalystRating(Base):
  __tablename__ = "analyst_ratings"
  
  id = Column(Integer, primary_key=True, index=True)
  
  # Core rating info
  stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
  broker_id = Column(Integer, ForeignKey("brokers.id"), nullable=False)
  
  action = Column(Enum(RatingAction), nullable=False)
  from_grade = Column(String(20))
  to_grade = Column(String(20), nullable=False)
  price_target = Column(Float)
  
  # Timing
  rating_date = Column(DateTime, nullable=False)
  
  # Price tracking
  price_at_rating = Column(Float)
  price_after_30d = Column(Float)
  price_checked_at = Column(DateTime)
  
  # Performance
  is_successful = Column(Boolean)
  price_change_pct = Column(Float)
  
  # News sentiment
  news_sentiment = Column(String(20))
  news_sentiment_score = Column(Float)
  news_headlines_count = Column(Integer, default=0)
  
  # Source
  source_url = Column(Text)
  finnhub_id = Column(String(100), unique=True)
  
  # Relationships
  stock = relationship("Stock", back_populates="ratings")
  broker = relationship("Broker", back_populates="ratings")
  news_items = relationship("RatingNews", back_populates="ratings")
  
  created_at = Column(DateTime, default=datetime.utcnow)
  
  # Indexes for performance
  __table_args__ = (
    Index('idx_rating_date', 'rating_date'),
    Index('idx_stock_rating_date', 'stock_id', 'rating_date'),
    Index('idx_broker_rating_date', 'broker_id', 'rating_date'),
    Index('idx_price_check', 'price_checked_at'),
  )

class RatingNews(Base):
  __tablename__ = "rating_news"
  
  id = Column(Integer, primary_key=True, index=True)
  rating_id = Column(Integer, ForeignKey("analyst_ratings.id"), nullable=False)
  
  headline = Column(Text, nullable=False)
  source = Column(String(100))
  url = Column(Text)
  published_at = Column(DateTime)
  
  # Sentiment
  sentiment_label = Column(String(20))
  sentiment_score = Column(Float)
  
  # Relationship
  rating = relationship("AnalystRating", back_populates="news_items")
  
  created_at = Column(DateTime, default=datetime.utcnow)