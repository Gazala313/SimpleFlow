from fastapi import FastAPI
from .database import Base, engine
from .routers import users, roles, projects, tasks
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:5174",
]

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(roles.router)
app.include_router(projects.router)
app.include_router(tasks.router)
