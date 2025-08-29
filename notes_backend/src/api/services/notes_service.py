"""
Service layer encapsulating business logic for Notes.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from ..repositories.notes_repository import NotesRepository
from ..models.note import Note


class NotesService:
    """Provides operations on notes with validation and business rules."""

    def __init__(self, db: Session):
        self.repo = NotesRepository(db)

    # PUBLIC_INTERFACE
    def list_notes(self, skip: int = 0, limit: int = 50) -> list[Note]:
        """Return a paginated list of notes."""
        limit = max(1, min(limit, 100))  # enforce sane limits
        skip = max(0, skip)
        return self.repo.list_notes(skip=skip, limit=limit)

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Note]:
        """Retrieve a single note by ID."""
        return self.repo.get_note(note_id)

    # PUBLIC_INTERFACE
    def create_note(self, title: str, content: str) -> Note:
        """Create a new note after basic validation."""
        if not title or not title.strip():
            raise ValueError("Title is required")
        return self.repo.create_note(title=title.strip(), content=content or "")

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, *, title: str | None, content: str | None) -> Optional[Note]:
        """Update an existing note if it exists; returns None if not found."""
        note = self.repo.get_note(note_id)
        if not note:
            return None

        new_title = title.strip() if isinstance(title, str) else None
        if new_title is not None and new_title == "":
            # prevent empty title when provided
            raise ValueError("Title cannot be empty")

        return self.repo.update_note(note, title=new_title, content=content)

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID, returning True if deleted."""
        return self.repo.delete_note(note_id)
