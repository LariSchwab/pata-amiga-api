from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.pata_amiga_api.database.banco_dados import Base


# from datetime import datetime
# from sqlalchemy import Column, Integer, String, DateTime
# from src.pata_amiga_api.database.banco_dados import Base

class AlunoEntidade(Base):
    __tablename__ = "alunos"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(20), nullable=False)
    sobrenome: str = Column(String(50), nullable=False)
    cpf: str = Column(String(14), nullable=False)
    data_nascimento: date = Column(Date(), nullable=False, name="data_nascimento")

