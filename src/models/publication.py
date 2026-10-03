# src/models/publication.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class Publication(BaseModel):
    id: str                          # hash(url) или uuid
    title: str
    text: str
    url: HttpUrl
    source_id: str
    published_at: Optional[datetime]
    lang: str = "ru"
    
    # заполняется по ходу пайплайна
    embedding: Optional[list[float]] = None
    relevance_score: Optional[float] = None
    cluster_id: Optional[int] = None
    is_duplicate_of: Optional[str] = None
    rejection_reason: Optional[str] = None  # для логирования