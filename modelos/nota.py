from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Nota(Base):
    __tablename__ = 'notas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_cpf = Column(Integer, ForeignKey('alunos.cpf'))
    disciplina_nome = Column(String, ForeignKey('disciplinas.nome'))

    av1 = Column(DECIMAL(4, 2))
    av2 = Column(DECIMAL(4, 2))

    aluno = relationship("Aluno", back_populates="notas")
    disciplina = relationship("Disciplina", back_populates="notas")

    def __init__(self, aluno_cpf, disciplina_nome, av1, av2):
        self.aluno_cpf = aluno_cpf
        self.disciplina_nome = disciplina_nome
        self.av1 = av1
        self.av2 = av2

    def obter_notas(self):
        return (f'Disciplina {self.disciplina.nome} || '
                f'Aluno {self.aluno.nome}. Nota: Av1 = {self.av1}. '
                f'Av2 = {self.av2}. Média: {self.media()}. '
                f'Situação: {self.situacao()}.')

    def media(self):
        return (self.av1 + self.av2) / 2

    def situacao(self):
        m = self.media()
        if m >= 5:
            return "Aprovado"
        elif m == 4:
            return "Recuperação"
        else:
            return "Reprovado"