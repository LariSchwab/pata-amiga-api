from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    email = Column(String(255), nullable=False, unique=True, index=True)
    telefone = Column(String(30))



