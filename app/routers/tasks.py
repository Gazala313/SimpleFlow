from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, require_role
from ..models import Task
from ..schemas import TaskCreate
from fastapi import HTTPException

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(task: TaskCreate,
                db: Session = Depends(get_db)):
                # current=Depends(require_role(["admin", "task_creator"]))):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    return db_task


@router.put("/{task_id}/complete")
def mark_complete(task_id: int,
                  db: Session = Depends(get_db)):
                #   current=Depends(require_role(["admin", "read_only"]))):
    task = db.query(Task).get(task_id)
    task.status = "COMPLETED"
    db.commit()
    return task


@router.get("/project/{project_id}")
def get_tasks_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    # current=Depends(require_role(["admin", "task_creator", "read_only"]))
):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks


@router.delete("/{task_id}")
def delete_project(task_id: int, db: Session = Depends(get_db)):
                #    current=Depends(require_role(["admin", "task_creator"]))):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(task)
    db.commit()

    return {"message": "Project deleted successfully"}
