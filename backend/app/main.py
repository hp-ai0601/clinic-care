from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME, APP_VERSION
from app.database import Base, engine

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
