from pydantic import BaseModel, Field

# Entidade
class Animal(BaseModel):
    id: int = Field()
    nome: str = Field()
    especie: str = Field()
    raca: str = Field()
    sexo: str = Field()
    porte: str = Field()
    idade: str = Field()
    peso: str = Field()
    ong: str = Field()

class AnimalCadastro(BaseModel):
    nome: str = Field()
    especie: str = Field()
    raca: str = Field()
    sexo: str = Field()
    porte: str = Field()
    idade: str = Field()
    peso: str = Field()
    ong: str = Field()

class AnimalEditar(BaseModel):
    nome: str = Field()
    especie: str = Field()
    raca: str = Field()
    sexo: str = Field()
    porte: str = Field()
    idade: str = Field()
    peso: str = Field()
    ong: str = Field()