from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from src.pata_amiga_api.database.banco_dados import Base
# from datetime import datetime
# from sqlalchemy import Column, Integer, String, DateTime
# from src.pata_amiga_api.database.banco_dados import Base

class UsuarioEntidade(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(191), nullable=False, unique=True, index=True)
    telefone = Column(String(30))
    senha_hash = Column(String(255), nullable=False)
    dataNascimento = Column(Date, nullable=False)

class UsuarioPJEntidade(Base):
    __tablename__ = "usuario_pj"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False, index=True)
    ong = Column(String(150), nullable=False, index=True)
    cnpj = Column(String(14), nullable=False, unique=True, index=True)  # só dígitos
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)

class AnimalEntidade(Base):
    __tablename__ = "animais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False, index=True)
    especie = Column(String(50), nullable=False, index=True)
    raca = Column(String(100), nullable=True)
    sexo = Column(String(10), nullable=True)  # 'M'/'F'
    porte = Column(String(20), nullable=True)  # 'pequeno/médio/grande'
    idade = Column(String(30), nullable=True)  # '2 anos', '6 meses'
    peso = Column(String(20), nullable=True)  # '10 kg'
    ong = Column(String(150), nullable=True)
    
    fotos = relationship("AnimalFotoEntidade", back_populates="animal")

class AnimalFotoEntidade(Base):
    __tablename__ = "animal_fotos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animais.id"))
    url = Column(String(255), nullable=False)
    legenda = Column(String(255), nullable=False)
    ordem = Column(Integer, default=0)
    capa = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)

    animal = relationship("AnimalEntidade", back_populates="fotos")


class SugestaoEntidade(Base):
    __tablename__ = "sugestao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(String(150), nullable=True)



