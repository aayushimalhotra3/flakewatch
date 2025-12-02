from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CiTestInput(BaseModel):
    suite: str = Field(..., max_length=512)
    name: str = Field(..., max_length=512)
    status: str
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None

class CiRunBatch(BaseModel):
    repository: str = Field(..., max_length=255)
    commit_sha: str = Field(..., max_length=64)
    branch: str = Field(..., max_length=255)
    environment: Dict[str, Any] = {}
    tests: List[CiTestInput]
