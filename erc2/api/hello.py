from fastapi import APIRouter
from ..database import SessionDep

router = APIRouter()


@router.get("/hello/{name}")
def get_hello(name: str, db: SessionDep):
    return {"hello": name}
