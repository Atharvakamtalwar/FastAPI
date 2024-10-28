from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, posts, auth, vote

from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
# As alembic is doing the work this linne is doing

app = FastAPI()

# origins=["https://www.google.com", "https://www.youtube.com"]
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"Message":"Hello World War 3!"}