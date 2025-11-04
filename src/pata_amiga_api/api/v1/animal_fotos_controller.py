from fastapi import UploadFile, File, Form, Depends, HTTPException, status
from src.pata_amiga_api.app import router
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.database.modelos import AnimalEntidade, AnimalFotoEntidade
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4
import shutil

@router.post("/api/animais/{id}/fotos", tags=["animal"])
async def upload_foto_animal(
    id: int,
    arquivo: UploadFile = File(...),
    legenda: str | None = Form(None),
    capa: bool = Form(False),
    ordem: int = Form(0),
    db: Session = Depends(get_db),
):
    animal = db.get(AnimalEntidade, id)
    if not animal:
        raise HTTPException(404, "Animal não encontrado")

    # salva arquivo no disco
    dest_dir = Path("static/uploads/animais") / str(id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{Path(arquivo.filename).suffix}"
    filepath = dest_dir / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    # se marcar capa, você pode opcionalmente desmarcar outras
    if capa:
        db.query(AnimalFotoEntidade).filter(AnimalFotoEntidade.animal_id == id).update({"capa": False})

    foto = AnimalFotoEntidade(
        animal_id=id,
        url=f"/static/uploads/animais/{id}/{filename}",
        legenda=legenda,
        ordem=ordem,
        capa=capa,
    )
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return {"id": foto.id, "url": foto.url, "legenda": foto.legenda, "ordem": foto.ordem, "capa": foto.capa}

@router.get("/api/animais/{id}/fotos", tags=["animal"])
def listar_fotos_animal(id: int, db: Session = Depends(get_db)):
    return db.query(AnimalFotoEntidade).filter(AnimalFotoEntidade.animal_id == id).order_by(AnimalFotoEntidade.ordem).all()

@router.delete("/api/animais/{id}/fotos/{foto_id}", tags=["animal"], status_code=status.HTTP_204_NO_CONTENT)
def apagar_foto_animal(id: int, foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(AnimalFotoEntidade, foto_id)
    if not foto or foto.animal_id != id:
        raise HTTPException(404, "Foto não encontrada")
    # opcional: também remover o arquivo físico
    try:
        p = Path("." + foto.url) if foto.url.startswith("/") else Path(foto.url)
        if p.exists():
            p.unlink(missing_ok=True)
    except Exception:
        pass
    db.delete(foto)
    db.commit()
    return


