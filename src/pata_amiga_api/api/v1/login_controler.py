from fastapi import HTTPException, Depends, status, Form
from sqlalchemy.orm import Session
from datetime import timedelta

from pata_amiga_api.schemas.login_schemas import LoginResponse
from src.pata_amiga_api.app import router
from src.pata_amiga_api.dependencias import get_db
from src.pata_amiga_api.seguranca import (
    autenticar_usuario_pf, 
    autenticar_usuario_pj, 
    criar_token_acesso,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

@router.post("/api/auth/login/pf", tags=["auth"], response_model=LoginResponse)
def login_pf(
    email: str = Form(), 
    senha: str = Form(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint de login para usuários pessoa física.
    Retorna um token JWT para autenticação Bearer.
    """
    usuario = autenticar_usuario_pf(email, senha, db)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        dados={"sub": usuario.email}, 
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        usuario_id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        tipo="pf"
    )

@router.post("/api/auth/login/pj", tags=["auth"], response_model=LoginResponse)
def login_pj(
    email: str = Form(), 
    senha: str = Form(), 
    db: Session = Depends(get_db)
):

    usuario = autenticar_usuario_pj(email, senha, db)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        dados={"sub": usuario.email}, 
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        usuario_id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        tipo="pj",
        ong=usuario.ong
    )
