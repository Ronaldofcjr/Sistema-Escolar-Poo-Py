from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base

class Turma(Base):
    __tablename__ = 'turmas'

    nome = Column(String, primary_key=True)
    periodo = Column(String)

    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")

    def __init__(self, nome, periodo):
        self.nome = nome
        self.periodo = periodo