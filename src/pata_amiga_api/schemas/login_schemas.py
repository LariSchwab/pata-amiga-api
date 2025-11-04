from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: str = Field()
    senha: str = Field()

class LoginResponse(BaseModel):
    access_token: str = Field(description="Token JWT para autenticação Bearer")
    token_type: str = Field(default="bearer", description="Tipo do token")
    usuario_id: int = Field(description="ID do usuário")
    nome: str = Field(description="Nome do usuário")
    email: str = Field(description="Email do usuário")
    tipo: str = Field(description="Tipo de usuário: 'pf' ou 'pj'")
    ong: Optional[str] = Field(default=None, description="Nome da ONG (apenas para PJ)")
