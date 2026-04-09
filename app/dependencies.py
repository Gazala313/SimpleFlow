from fastapi import Depends, HTTPException
from .auth import get_current_user
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_role(allowed_roles: list):
    def role_checker(
        user=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        db_user = db.query(User).filter(User.email == user["oid"]).first()
        print("DB USER:", db_user)


        if db_user:
            print("ROLE:", db_user.role.name)
        if not db_user or db_user.role.name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")

        return db_user

    return role_checker
