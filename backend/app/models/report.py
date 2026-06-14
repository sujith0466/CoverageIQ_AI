from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, JSON
from sqlalchemy.sql import func
import enum
import uuid
from app.db.base_class import Base

class ReportStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    ANALYZED = "ANALYZED"
    FAILED = "FAILED"

class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    coverage_percent = Column(Float, nullable=True)
    total_files = Column(Integer, nullable=True)
    total_classes = Column(Integer, nullable=True)
    total_lines = Column(Integer, nullable=True)
    covered_lines = Column(Integer, nullable=True)
    line_rate = Column(Float, nullable=True)
    branch_rate = Column(Float, nullable=True)
    raw_metrics = Column(JSON, nullable=True)
    status = Column(Enum(ReportStatus), default=ReportStatus.UPLOADED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
