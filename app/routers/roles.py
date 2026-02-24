from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, require_role
from ..models import Role
from ..schemas import RoleCreate


router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_role(role: RoleCreate,
                db: Session = Depends(get_db),
                current=Depends(require_role(["admin"]))):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    return db_role
