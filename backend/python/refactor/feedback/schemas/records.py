from datetime import datetime

from pydantic import BaseModel, Field


class TagRecord(BaseModel):
    tag_id: int
    tag: str
    sentence_idx: int


class DocumentRecord(BaseModel):
    doc_id: int
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    tags: list[TagRecord]
