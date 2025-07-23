from fastapi import APIRouter
from sqlalchemy.sql import select
from ..database import SessionDep
from ..models import NoteCreate
from ..schema import Note

router = APIRouter()


@router.get("/notes")
def get_notes(db: SessionDep):
    notes = db.execute(select(Note)).scalars().all()
    return notes


@router.post("/notes")
def add_note(db: SessionDep, note: NoteCreate):
    entity = Note(id=note.id, title=note.title, content=note.content)

    db.add(entity)
    db.commit()

    return entity
