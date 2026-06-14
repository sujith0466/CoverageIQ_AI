from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.sql import func
import uuid
from app.db.base_class import Base

class Function(Base):
    __tablename__ = "functions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = Column(String(36), ForeignKey("reports.id"), nullable=False)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # AST Extracted Fields
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)
    parameters = Column(JSON, nullable=True)
    docstring = Column(String, nullable=True)
    function_type = Column(String, nullable=True) # e.g. 'function', 'method'
    is_async = Column(Boolean, default=False)
    return_type = Column(String, nullable=True)
    decorators = Column(JSON, nullable=True)
    called_functions = Column(JSON, nullable=True)

    # Coverage Gap Fields
    coverage_percent = Column(Float, nullable=True)
    executable_lines = Column(Integer, nullable=True)
    covered_lines = Column(Integer, nullable=True)
    coverage_details = Column(JSON, nullable=True)

    risk_score = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)
    risk_reasons = Column(JSON, nullable=True)
    risk_priority_rank = Column(Integer, nullable=True)
    dependency_count = Column(Integer, default=0)
    impact_radius = Column(Integer, default=0)
    critical_dependency_score = Column(Float, nullable=True)
    dependency_level = Column(String, nullable=True)
    
    potential_coverage_gain = Column(Float, nullable=True)
    test_priority_score = Column(Float, nullable=True)
    recommended_test_order = Column(Integer, nullable=True)
    recommendation_category = Column(String, nullable=True)
    
    coverage_status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
