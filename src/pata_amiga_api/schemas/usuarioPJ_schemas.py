from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Entidade
class UsuarioPJ(BaseModel):
    id: int = Field()
    nome: str = Field()
    ong: str = Field()
    cnpj: str = Field()
    telefone: str = Field()
    email: EmailStr = Field()

    class Config:
        from_attributes = True

class UsuarioPJCadastro(BaseModel):
    nome: str = Field()
    ong: str = Field()
    cnpj: str = Field()
    telefone: str = Field()
    email: EmailStr = Field()
    senha: str = Field(min_length=6)

class UsuarioPJEditar(BaseModel):
    nome: str = Field()
    ong: str = Field()
    cnpj: str = Field()
    telefone: str = Field()
    email: EmailStr = Field()
    senha: Optional[str] = Field(
        default=None, description="Nova senha (se enviado, será hasheada)"
    )
