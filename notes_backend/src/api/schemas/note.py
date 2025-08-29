"""
Pydantic schemas for Note API.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Common properties shared by Note create/update operations."""

    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field("", description="Content/body of the note")


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note (partial update allowed)."""

    title: str | None = Field(None, description="Updated title", min_length=1, max_length=255)
    content: str | None = Field(None, description="Updated content")


class NoteOut(BaseModel):
    """Schema for returning a note to clients."""

    id: int = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
