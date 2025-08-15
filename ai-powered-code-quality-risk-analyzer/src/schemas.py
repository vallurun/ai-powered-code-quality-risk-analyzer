from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyzeRequest(BaseModel):
    patch: str

class FileSuggestion(BaseModel):
    path: str
    risk: float
    suggestions: List[str]

class AnalyzeResponse(BaseModel):
    overall_risk: float
    files: List[FileSuggestion]
