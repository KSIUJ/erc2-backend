from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Annotated
from .config import settings


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
