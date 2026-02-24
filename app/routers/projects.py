from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, require_role
from ..models import Project
from ..schemas import ProjectCreate
from fastapi import HTTPException



router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
def create_project(project: ProjectCreate,
                   db: Session = Depends(get_db)):
                #    current=Depends(require_role(["admin"]))
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    return db_project


@router.get("/")
def get_projects(
    db: Session = Depends(get_db),
    # current=Depends(require_role(["admin"]))  # optional
):
    return db.query(Project).all()


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.put("/{project_id}")
def update_project(
    project_id: int,
    updated_project: ProjectCreate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = updated_project.name
    project.description = updated_project.description

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}



