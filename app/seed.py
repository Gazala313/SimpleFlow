from .database import SessionLocal
from .models import Role

def seed_roles():
    db = SessionLocal()

    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "task_creator"},
        {"id": 3, "name": "read_only"},
    ]

    for role in roles:
        existing = db.query(Role).filter(Role.id == role["id"]).first()
        if not existing:
            db.add(Role(id=role["id"], name=role["name"]))

    db.commit()
    db.close()
