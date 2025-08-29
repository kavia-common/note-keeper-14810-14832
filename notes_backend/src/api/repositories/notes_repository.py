"""
Repository layer for Note model CRUD operations.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from ..models.note import Note


class NotesRepository:
    """Encapsulates database operations for notes."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_notes(self, skip: int = 0, limit: int = 50) -> list[Note]:
        stmt = select(Note).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_note(self, note_id: int) -> Optional[Note]:
        return self.db.get(Note, note_id)

    def create_note(self, title: str, content: str) -> Note:
        note = Note(title=title, content=content or "")
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update_note(self, note: Note, *, title: str | None = None, content: str | None = None) -> Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_note(self, note_id: int) -> bool:
        stmt = delete(Note).where(Note.id == note_id)
        res = self.db.execute(stmt)
        self.db.commit()
        return res.rowcount > 0
