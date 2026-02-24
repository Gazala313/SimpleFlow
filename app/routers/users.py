from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate
from ..dependencies import require_role, get_db
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate,
                db: Session = Depends(get_db)):
                # current=Depends(require_role(["admin"]))):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    # current=Depends(require_role(["admin"]))  # optional
):
    return db.query(User).all()


@router.get("/{user_id}")
def get_project(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}")
def update_project(
    user_id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email
    user.role_id = updated_user.role_id

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_project(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}



