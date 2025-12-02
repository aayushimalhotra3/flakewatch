from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False, index=True)
    suite_name = Column(String(512), nullable=False)
    test_name = Column(String(512), nullable=False)
    full_name = Column(String(1024), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TestRun(Base):
    __tablename__ = "test_runs"
    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False, index=True)
    commit_sha = Column(String(64), nullable=False, index=True)
    branch = Column(String(255), nullable=False, index=True)
    status = Column(String(32), nullable=False)
    duration_ms = Column(Integer, nullable=True)
    environment_json = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    run_at = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
