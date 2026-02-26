import os
from fastapi import FastAPI
from .database import Base, engine
from .routers import users, roles, projects, tasks
from fastapi.middleware.cors import CORSMiddleware
from .seed import seed_roles

# Get origins from environment variable, fallback to localhost
origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5174","https://proud-grass-004f4740f.4.azurestaticapps.net")
origins = [origin.strip() for origin in origins_str.split(",")]

Base.metadata.create_all(bind=engine)
seed_roles()

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
