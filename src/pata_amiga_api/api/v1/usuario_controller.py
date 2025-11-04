from fastapi import HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.pata_amiga_api.app import router
from src.pata_amiga_api.database.modelos import UsuarioEntidade
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.schemas.usuario_schemas import Usuario, UsuarioCadastro, UsuarioEditar
from src.pata_amiga_api.seguranca import gerar_hash_senha


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
        dataNascimento=usuario.dataNascimento
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
            dataNascimento=usuario.dataNascimento
        )
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")


@router.post("/api/usuarios", tags=["usuario"])
def cadastrar_usuarios(form: UsuarioCadastro, db: Session = Depends(get_db)):
    # Gera o hash da senha antes de salvar
    senha_hash = gerar_hash_senha(form.senha)

    usuario = UsuarioEntidade(
        nome=form.nome,
        cpf=form.cpf,
        telefone=form.telefone,
        email=form.email,
        senha_hash=senha_hash,
        dataNascimento=form.dataNascimento)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return Usuario(
        id=usuario.id,
        nome=form.nome,
        cpf=form.cpf,
        telefone=form.telefone,
        email=form.email,
        dataNascimento=form.dataNascimento
    )


@router.delete("/api/usuarios/{id}", status_code=204, tags=["usuario"])
def apagar_usuarios(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioEntidade).filter(UsuarioEntidade.id == id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")


@router.put("/api/usuarios/{id}", tags=["usuario"])
def editar_usuarios(id: int, form: UsuarioEditar, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioEntidade).filter(UsuarioEntidade.id == id).first()
    if usuario:
        usuario.nome = form.nome
        usuario.cpf = form.cpf
        usuario.telefone = form.telefone
        usuario.email = form.email
        # Gera o hash da nova senha antes de salvar
        usuario.senha_hash = gerar_hash_senha(form.senha)
        usuario.dataNascimento = form.dataNascimento
        db.commit()
        db.refresh(usuario)
        return usuario
    raise HTTPException(status_code=404, detail=f"Usuário não encontrado com id: {id}")
