from fastapi import HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.pata_amiga_api.app import router
from src.pata_amiga_api.database.modelos import UsuarioPJEntidade
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.schemas.usuarioPJ_schemas import UsuarioPJ, UsuarioPJCadastro, UsuarioPJEditar
from src.pata_amiga_api.seguranca import gerar_hash_senha

@router.get("/api/usuario_pj", tags=["usuario_pj"])
def listas_todos_usuarios_pj(filtro: str = Query(default="", alias="filtro"), db: Session = Depends(get_db)):
    pesquisa = f"%{filtro}%"
    usuarios = db.query(UsuarioPJEntidade).filter(
        or_(
            UsuarioPJEntidade.nome.ilike(pesquisa),
            UsuarioPJEntidade.cnpj.ilike(f"{filtro}%")
        )
    ).all()
    usuarios_response = [UsuarioPJ(
        id=usuario.id,
        nome=usuario.nome,
        ong=usuario.ong,
        cnpj=usuario.cnpj,
        telefone=usuario.telefone,
        email=usuario.email
    ) for usuario in usuarios]
    return usuarios_response

@router.get("/api/usuario_pj/{id}", tags=["usuario_pj"], response_model=UsuarioPJ)
def obter_por_id_usuario_pj(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioPJEntidade).filter(UsuarioPJEntidade.id == id).first()
    if usuario:
        return UsuarioPJ(
            id=usuario.id,
            nome=usuario.nome,
            ong=usuario.ong,
            cnpj=usuario.cnpj,
            telefone=usuario.telefone,
            email=usuario.email
        )
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")

@router.post("/api/usuario_pj", tags=["usuario_pj"])
def cadastrar_usuario_pj(form: UsuarioPJCadastro, db: Session = Depends(get_db)):
    # Gera o hash da senha antes de salvar
    senha_hash = gerar_hash_senha(form.senha)
    
    usuario = UsuarioPJEntidade(
        nome=form.nome,
        ong=form.ong,
        cnpj=form.cnpj,
        telefone=form.telefone,
        email=form.email,
        senha_hash=senha_hash
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario

@router.delete("/api/usuario_pj/{id}", status_code=204, tags=["usuario_pj"])
def apagar_usuario_pj(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioPJEntidade).filter(UsuarioPJEntidade.id == id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")

@router.put("/api/usuario_pj/{id}", tags=["usuario_pj"])
def editar_usuario_pj(id: int, form: UsuarioPJEditar, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioPJEntidade).filter(UsuarioPJEntidade.id == id).first()
    if usuario:
        usuario.nome = form.nome
        usuario.ong = form.ong
        usuario.cnpj = form.cnpj
        usuario.telefone = form.telefone
        usuario.email = form.email
        # Gera o hash da nova senha antes de salvar
        usuario.senha_hash = gerar_hash_senha(form.senha)
        db.commit()
        db.refresh(usuario)
        return usuario
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")