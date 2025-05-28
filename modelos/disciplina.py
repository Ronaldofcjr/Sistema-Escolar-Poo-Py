from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base
from database import session
from sqlalchemy.orm import Session

class Disciplina(Base):
    __tablename__ = 'disciplinas'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    nome = Column(String, nullable=False, unique=True)

    notas = relationship("Nota", back_populates="disciplina", cascade="all, delete-orphan")

    def __init__(self, nome):
        self.nome = nome

    @classmethod
    def criar_disciplina(cls):
        try:
            nome = input("Digite o nome da Disciplina: ").strip()

            if not nome:
                raise ValueError("O nome da disciplina não pode estar vazio.")
            
            disciplina_existente = session.query(cls).filter_by(nome=nome).first()
            if disciplina_existente:
                print(f'A disciplina {nome} já existe')
                return
            
            nova_disciplina = cls(nome=nome)
            session.add(nova_disciplina)
            session.commit()

            print(f"Disciplina '{nome}' criada com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro ao criar a disciplina: {e}")

    def listar_notas(self):
        for nota in self.notas:
            print(f'Aluno: {nota.aluno.nome} || AV1: {nota.av1} || AV2: {nota.av2} || Média: {nota.media()}')


    @classmethod
    def listar_disciplina(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def excluir_disciplina(cls, session: Session, id:int):
        id_disciplina = int(input('Coloque o ID da disciplina que deseja excluir'))
        disciplina = session.query(cls).filter_by(id_disciplina=id).first()
        if disciplina:
            session.delete(disciplina)
            session.commit()
            return True
        return False
    


