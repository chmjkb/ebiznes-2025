from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import engine, get_db
from models import Todo, TodoCreate, TodoUpdate
import models_db

models_db.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo List API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Todo List API with Database"}


@app.get("/todos", response_model=List[Todo])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(models_db.Todo).all()
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models_db.Todo).filter(models_db.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = models_db.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models_db.Todo).filter(models_db.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    
    todo.updated_at = datetime.now()
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models_db.Todo).filter(models_db.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)