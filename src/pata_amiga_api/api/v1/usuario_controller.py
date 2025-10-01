from fastapi import HTTPException
from fastapi.params import Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.pata_amiga_api.app import router
from src.pata_amiga_api.database.modelos import UsuarioEntidade
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.schemas.usuario_schemas import Usuario


@router.get("/api/usuarios", tags=["usuario"])
def listas_todos_usuarios(filtro: str = Query(default="", alias="filtro"), db: Session = Depends(get_db)):
    pesquisa = f"%{filtro}%"
    usuarios = db.query(UsuarioEntidade).filter(
        or_(
            UsuarioEntidade.nome.ilike(pesquisa),
            UsuarioEntidade.cpf.ilike(f"{filtro}%")
        )
    ).all()
    usuarios_response = [Usuario(
        id=usuario.id,
        nome=usuario.nome,
        cpf=usuario.cpf,
        telefone=usuario.telefone,
        email=usuario.email,
    ) for usuario in usuarios]
    return usuarios_response

@router.get("/api/usuarios/{id}", tags=["usuario"], response_model=Usuario)
def obter_por_id_usuarios(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioEntidade).filter(UsuarioEntidade.id == id).first()
    if usuario:
        return Usuario(
            id=usuario.id,
            nome=usuario.nome,
            cpf=usuario.cpf,
            telefone=usuario.telefone,
            email=usuario.email,
        )
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")
