# src/models/publication.py
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class Publication(BaseModel):
    # === заполняется из источника ===
    id: str                          # hash(url) или uuid
    title: str
    text: str
    url: HttpUrl
    source_id: str
    source_name: str
    published_at: Optional[datetime] = None
    lang: str = "ru"
    
    # === заполняется LLM на этапе классификации ===
    type: Optional[str] = None               # Атака | Уязвимость | Инфо
    priority: Optional[str] = None
    tags: list[int] = Field(default_factory=list)
    confidence: Optional[float] = None
    audience: Optional[str] = None           # tech | exec | unknown
    impact_score: Optional[float] = None
    alert_worthy: Optional[bool] = None
    
    # === заполняется на этапе извлечения полей ===
    extracted: dict = Field(default_factory=dict)
    
    # заполняется по ходу пайплайна (служебное)
    embedding: Optional[list[float]] = None
    relevance_score: Optional[float] = None
    cluster_id: Optional[int] = None
    is_duplicate_of: Optional[str] = None
    rejection_reason: Optional[str] = None  # для логирования