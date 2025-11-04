import uvicorn

from src.pata_amiga_api.database.banco_dados import Base, engine, popular_banco_dados
from src.pata_amiga_api.api.v1 import usuario_controller
from src.pata_amiga_api.api.v1 import usuarioPJ_controller
from src.pata_amiga_api.api.v1 import animal_controller
from src.pata_amiga_api.api.v1 import animal_fotos_controller
from src.pata_amiga_api.api.v1 import sugestao_controller
from src.pata_amiga_api.app import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
popular_banco_dados()

app.include_router(usuario_controller.router)
app.include_router(usuarioPJ_controller.router)
app.include_router(animal_controller.router)
app.include_router(animal_controller.router)
app.include_router(animal_fotos_controller.router)
app.include_router(sugestao_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)