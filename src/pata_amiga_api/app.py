from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.pata_amiga_api.database.banco_dados import engine
from src.pata_amiga_api.database import modelos
from pathlib import Path



router = APIRouter()
app = FastAPI()

# static/ está na raiz do projeto, ao lado de src/
STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)  # garante que a pasta exista

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://0.0.0.0:4200",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET, PUT, DELETE, PATCH, OPTIONS, HEAD
    allow_headers=["*"]
)