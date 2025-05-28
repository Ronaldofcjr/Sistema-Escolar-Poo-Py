from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, session
from modelos.pessoa import Pessoa
from modelos.disciplina import Disciplina

class ProfessorJaExisteError(Exception):
    pass

class DisciplinaNaoEncontradaError(Exception):
    pass

class CPFInvalidoError(Exception):
    pass

class NotaNaoEncontradaError(Exception):
    pass

class Professor(Pessoa):
    __tablename__ = 'professores'

    disciplina_nome = Column(String, ForeignKey('disciplinas.nome'))

    disciplina = relationship("Disciplina", back_populates="professores")

    def __init__(self, cpf, nome, disciplina):
        super().__init__(cpf, nome)
        self.disciplina = disciplina

    @classmethod
    def criar_professor(cls):
        cpf = input("Digite o CPF do professor (somente números): ").strip()
        if not cpf.isdigit():
            raise CPFInvalidoError("CPF inválido, precisa ser numérico.")
        cpf = int(cpf)

        nome = input("Digite o nome do professor: ").strip()
        disciplina_nome = input("Digite o nome da disciplina: ").strip()

        if session.query(cls).filter_by(cpf=cpf).first():
            raise ProfessorJaExisteError("Já existe um professor com esse CPF!")

        disciplina = session.query(Disciplina).filter_by(nome=disciplina_nome).first()
        if not disciplina:
            raise DisciplinaNaoEncontradaError("Disciplina não encontrada.")

        novo_professor = cls(cpf=cpf, nome=nome, disciplina=disciplina)
        session.add(novo_professor)
        session.commit()

        print(f"Professor {nome} cadastrado com sucesso na disciplina {disciplina_nome}!")

    def criar_prof_com_tratamentos(cls):
        try:
            cls.criar_professor()
        except (CPFInvalidoError, ProfessorJaExisteError, DisciplinaNaoEncontradaError) as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def consultar_disciplinas_e_notas_com_tratamento(self):
        if self.disciplina and self.disciplina.notas:
            for nota in self.disciplina.notas:
                print(nota.obter_notas())
        else:
            raise NotaNaoEncontradaError("Nenhuma nota encontrada para as disciplinas do professor.")
