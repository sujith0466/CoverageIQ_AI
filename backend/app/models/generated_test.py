from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
import uuid
from app.db.base_class import Base

class GeneratedTest(Base):
    __tablename__ = "generated_tests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    function_id = Column(String(36), ForeignKey("functions.id"), nullable=False)
    test_code = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=True)
    test_quality_score = Column(Float, nullable=True)
    model_used = Column(String, nullable=True)
    generation_status = Column(String, nullable=True, default="PENDING")
    prompt_version = Column(String, nullable=True)
    generated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
