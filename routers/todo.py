from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todo", tags=["todo"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos