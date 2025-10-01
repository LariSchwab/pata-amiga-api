from datetime import datetime

from pydantic import BaseModel, Field


# Entidade
class Usuario(BaseModel):
    id: int = Field()
    nome: str = Field()
    cpf: str = Field()
    telefone: str = Field()
    email: str = Field()

class UsuarioCadastro(BaseModel):
    nome: str = Field()
    cpf: str = Field()
    telefone: str = Field()
    email: str = Field()

