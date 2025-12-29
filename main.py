from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse
from routers import todo
from auth import verify_token

app = FastAPI()
app.include_router(todo.router)

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fake_auth(token: str = "secret"):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "user"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.get("/")
def root():
    return {"status": "ok"}

# Create Todo
@app.post("/todo", response_model=TodoResponse)
def create_todo(todo: TodoCreate,user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Read Todos
@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Update Todo
@app.put("/todo/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.done = data.done
    db.commit()
    db.refresh(todo)
    return todo

# Delete Todo
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"result": "deleted"}
