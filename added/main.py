from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4 , UUID
app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title : str
    description : Optional[str] = None
    completed : bool = False

tasks = []


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_task():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    return HTTPException(status_code=404, details="Task Not FOund")


@app.put("/tasks/{task_id}" , response_model=Task)
def update_task(task_id: UUID, t_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id :
            updated_task = task.copy(update = t_update.dict(exclude_uset=True))
            tasks[idx] = updated_task
            return updated_task

    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id : UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return task.pop(idx)

    raise HTTPException(status_code=404, detail="Task Not Found")

@ app.get("/")
async def welcome():
    return "Welcome to my api nigga"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)