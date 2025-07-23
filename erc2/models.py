from pydantic import BaseModel
from typing import Optional


# Define pydantic models here
class NoteCreate(BaseModel):
    id: int
    title: Optional[str]
    content: str
