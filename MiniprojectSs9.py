from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
app = FastAPI()
tasks_db = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Study CRUD",
        "assignee": "Hung",
        "priority": 2,
        "status": "todo",
        "created_at": "2026-07-06 10:00",
        "internal_notes": "Only Admin"
    }
]
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str
    assignee: str = Field(min_length=2)
    priority: int = Field(ge=1, le=5)
class TaskUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str
    assignee: str = Field(min_length=2)
    priority: int = Field(ge=1, le=5)
    status: str
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str
@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    for item in tasks_db:
        if item["title"].lower() == task.title.lower():
            raise HTTPException(
                status_code=400,
                detail="Task title already exists!"
            )
    new_id = 1
    if len(tasks_db) > 0:
        new_id = tasks_db[-1]["id"] + 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "priority": task.priority,
        "status": "todo",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "internal_notes": "Only Admin"
    }
    tasks_db.append(new_task)
    return new_task
@app.get("/tasks/search")
def search_task(keyword: str = None, status: str = None):
    result = []
    for task in tasks_db:
        if keyword:
            if keyword.lower() not in task["title"].lower() and \
               keyword.lower() not in task["assignee"].lower():
                continue
        if status:
            if task["status"] != status:
                continue
        result.append(task)
    return {
        "total": len(result),
        "data": result
    }
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    flag  = False
    for task in tasks_db:
        if task["id"] == task_id:
            flag = True
            return task
    if flag == False:
        raise HTTPException(status_code=404,detail="Task not found!")
@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task: TaskUpdate):
    flag  = False
    for task in tasks_db:
        if task["id"] == task_id:
            flag  = True
            if new_task.status not in [
                "todo",
                "in_progress",
                "done"
            ]:
                raise HTTPException(status_code=400,detail="Invalid status!")
            task["title"] = new_task.title
            task["description"] = new_task.description
            task["assignee"] = new_task.assignee
            task["priority"] = new_task.priority
            task["status"] = new_task.status
            return {'message':'Update completed','data':task}
    if flag == False:
        raise HTTPException(
            status_code=404,
            detail="Task not found!"
        )
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    flag = False
    for task in tasks_db:
        if task["id"] == task_id:
            flag = True
            tasks_db.remove(task)
            return
    if flag == False:
        raise HTTPException(
            status_code=404,
            detail="Task not found!"
        )