from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from src.pata_amiga_api.app import router
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.database.modelos import SugestaoEntidade
from src.pata_amiga_api.schemas.sugestao_schemas import Sugestao, SugestaoCadastro

@router.post("/api/sugestoes", tags=["sugestao"])
def cadastrar_sugestoes(form: SugestaoCadastro, db: Session = Depends(get_db)):
    sugestao = SugestaoEntidade(
        nome=form.nome,
        email=form.email,
        titulo=form.titulo,
        descricao=form.descricao)

    db.add(sugestao)
    db.commit()
    db.refresh(sugestao)

    return sugestao