from fastapi import FastAPI
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    completed: bool = False
    
app = FastAPI()

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.put("/todos/{id}")
def update_todo(id: int, todo: Todo):
    todos[id] = todo
    return todo

@app.delete("/todos/{id}")
def delete_todo(id: int):
    todos.pop(id)
    return

todos = []