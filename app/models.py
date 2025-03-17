from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OptimizedResult(Base):
    __tablename__ = "optimized_results"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(JSON, nullable=False)
    optimized_data = Column(JSON, nullable=False)
