from pydantic import BaseModel, Field

# Entidade
class Sugestao(BaseModel):
    id: int = Field()
    nome: str = Field()
    email: str = Field()
    titulo: str = Field()
    descricao: str = Field()

class SugestaoCadastro(BaseModel):
    nome: str = Field()
    email: str = Field()
    titulo: str = Field()
    descricao: str = Field()

