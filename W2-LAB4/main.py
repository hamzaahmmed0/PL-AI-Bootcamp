"""
To-Do List REST API
Built with FastAPI. Data is stored in-memory using a Python list (no database).

Run with:
    uvicorn main:app --reload

Then open:
    Swagger UI -> http://127.0.0.1:8000/docs
    ReDoc      -> http://127.0.0.1:8000/redoc
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="To-Do List API",
    description="A simple To-Do List REST API built with FastAPI (in-memory storage).",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory storage
# ---------------------------------------------------------------------------
todos: List[dict] = []
next_id: int = 1


# ---------------------------------------------------------------------------
# Pydantic Models (Schemas)
# ---------------------------------------------------------------------------
class TodoCreate(BaseModel):
    title: str = Field(..., example="Finish Python assignment")


class TodoReplace(BaseModel):
    """Used for PUT — full replacement, both fields are required."""
    title: str = Field(..., example="Finish FastAPI assignment")
    completed: bool = Field(..., example=True)


class TodoUpdate(BaseModel):
    """Used for PATCH — partial update, both fields are optional."""
    title: Optional[str] = Field(None, example="Finish FastAPI assignment")
    completed: Optional[bool] = Field(None, example=True)


class Todo(BaseModel):
    id: int
    title: str
    completed: bool


# ---------------------------------------------------------------------------
# Helper function
# ---------------------------------------------------------------------------
def find_todo(todo_id: int) -> Optional[dict]:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


# ---------------------------------------------------------------------------
# Question 1: Create a new task
# POST /todos
# ---------------------------------------------------------------------------
@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"])
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "completed": False,
    }
    todos.append(new_todo)
    next_id += 1
    return new_todo


# ---------------------------------------------------------------------------
# Question 2: Retrieve all tasks
# GET /todos
# ---------------------------------------------------------------------------
@app.get("/todos", response_model=List[Todo], tags=["Todos"])
def get_all_todos():
    return todos


# ---------------------------------------------------------------------------
# Question 3: Retrieve a specific task by ID
# GET /todos/{id}
# ---------------------------------------------------------------------------
@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def get_todo(todo_id: int):
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {todo_id} not found")
    return todo


# ---------------------------------------------------------------------------
# Question 4: Update an existing task (full replacement)
# PUT /todos/{id}
# Both "title" and "completed" must be provided by the client — this fully
# replaces the task's data instead of relying on hardcoded/default values.
# ---------------------------------------------------------------------------
@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def update_todo(todo_id: int, updated: TodoReplace):
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {todo_id} not found")

    todo["title"] = updated.title
    todo["completed"] = updated.completed

    return todo


# ---------------------------------------------------------------------------
# Bonus: Partially update an existing task
# PATCH /todos/{id}
# Only the fields provided by the client are updated; everything else
# stays unchanged.
# ---------------------------------------------------------------------------
@app.patch("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def patch_todo(todo_id: int, updated: TodoUpdate):
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {todo_id} not found")

    if updated.title is not None:
        todo["title"] = updated.title
    if updated.completed is not None:
        todo["completed"] = updated.completed

    return todo


# ---------------------------------------------------------------------------
# Question 5: Delete a task
# DELETE /todos/{id}
# ---------------------------------------------------------------------------
@app.delete("/todos/{todo_id}", tags=["Todos"])
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Task with id {todo_id} not found")

    todos.remove(todo)
    return {"message": f"Task with id {todo_id} deleted successfully"}


# ---------------------------------------------------------------------------
# Root endpoint (optional, just a friendly welcome message)
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the To-Do List API. Visit /docs for Swagger UI."}