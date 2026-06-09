from fastapi import FastAPI, HTTPException
from .models import Task

app = FastAPI()
tasks: dict[str, Task] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    tasks[task.id] = task
    return task

@app.get("/tasks")
def list_tasks():
    return list(tasks.values())

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    del tasks[task_id]
    return {"ok": True}
