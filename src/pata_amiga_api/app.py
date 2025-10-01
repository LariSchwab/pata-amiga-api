from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

# IMPORTANTE: garantir que os modelos sejam carregados antes do create_all() no main.py
from src.pata_amiga_api.database import modelos

router = APIRouter()

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET, PUT, DELETE, PATCH, OPTIONS, HEAD
    allow_headers=["*"]
)