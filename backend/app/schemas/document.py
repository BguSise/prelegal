from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class DocumentCreate(BaseModel):
    template_id: str
    title: str
    field_values: dict = {}


class DocumentUpdate(BaseModel):
    title: str | None = None
    field_values: dict | None = None
    status: Literal["draft", "complete"] | None = None


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    template_id: str
    title: str
    field_values: dict
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
