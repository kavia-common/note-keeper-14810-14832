"""
API router for Notes endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.notes_service import NotesService
from ..schemas.note import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Notes"])


def get_service(db: Session = Depends(get_db)) -> NotesService:
    return NotesService(db)


@router.get(
    "",
    summary="List notes",
    description="Retrieve a paginated list of notes.",
    response_model=list[NoteOut],
    responses={200: {"description": "List of notes returned successfully"}},
)
# PUBLIC_INTERFACE
def list_notes(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of items to return"),
    service: NotesService = Depends(get_service),
) -> list[NoteOut]:
    """List notes with pagination."""
    return service.list_notes(skip=skip, limit=limit)


@router.post(
    "",
    summary="Create a note",
    description="Create a new note with title and optional content.",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteOut,
    responses={
        201: {"description": "Note created successfully"},
        400: {"description": "Invalid input"},
    },
)
# PUBLIC_INTERFACE
def create_note(payload: NoteCreate, service: NotesService = Depends(get_service)) -> NoteOut:
    """Create a note and return the created resource."""
    try:
        return service.create_note(title=payload.title, content=payload.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get(
    "/{note_id}",
    summary="Get a note",
    description="Retrieve a single note by its ID.",
    response_model=NoteOut,
    responses={
        200: {"description": "Note found"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def get_note(
    note_id: int = Path(..., ge=1, description="ID of the note to retrieve"),
    service: NotesService = Depends(get_service),
) -> NoteOut:
    """Get a note by ID."""
    note = service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put(
    "/{note_id}",
    summary="Update a note",
    description="Replace the title/content of a note. Both fields required.",
    response_model=NoteOut,
    responses={
        200: {"description": "Note updated"},
        400: {"description": "Invalid input"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def update_note(
    payload: NoteCreate,
    note_id: int = Path(..., ge=1, description="ID of the note to update"),
    service: NotesService = Depends(get_service),
) -> NoteOut:
    """Update a note by replacing its title and content."""
    try:
        updated = service.update_note(note_id, title=payload.title, content=payload.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.patch(
    "/{note_id}",
    summary="Partially update a note",
    description="Update one or more fields (title/content) of a note.",
    response_model=NoteOut,
    responses={
        200: {"description": "Note updated"},
        400: {"description": "Invalid input"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def patch_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1, description="ID of the note to update"),
    service: NotesService = Depends(get_service),
) -> NoteOut:
    """Partially update a note."""
    try:
        updated = service.update_note(note_id, title=payload.title, content=payload.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


from fastapi import Response

@router.delete(
    "/{note_id}",
    summary="Delete a note",
    description="Delete a note by ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,  # Explicitly indicate no response body for 204
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def delete_note(
    note_id: int = Path(..., ge=1, description="ID of the note to delete"),
    service: NotesService = Depends(get_service),
) -> Response:
    """
    Delete a note. Returns 204 No Content on success.

    FastAPI enforces that 204 responses must not include a response body.
    We therefore return an empty Response with status_code=204.
    """
    deleted = service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    # Return an explicit empty response to avoid any implicit body serialization.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
