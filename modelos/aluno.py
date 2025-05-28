from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from database import Base, session
from modelos.pessoa import Pessoa
from modelos.nota import Nota
from modelos.turma import Turma

class CPFInvalidoError(Exception):
    pass

class AlunoJaExisteError(Exception):
    pass

class NenhumaDisciplinaEncontradaError(Exception):
    pass

class Aluno(Base, Pessoa):
    __tablename__ = 'alunos'

    cpf = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    turma_nome = Column(String, ForeignKey('turmas.nome'))

    turma = relationship("Turma", back_populates="alunos")
    notas = relationship("Nota", back_populates="aluno", cascade="all, delete-orphan")

    def __init__(self, cpf, nome, turma=None):
        Pessoa.__init__(self, cpf, nome)  # chama construtor abstrato
        self.turma = turma

    @classmethod
    def criar_aluno(cls):
        print("\n--- Criar Aluno ---")
        try:
            cpf = input("Digite o CPF do aluno (somente números): ").strip()
            if not cpf.isdigit():
                raise CPFInvalidoError("CPF inválido, deve conter somente números.")
            cpf = int(cpf)
            
            nome = input("Digite o nome do aluno: ").strip()
            
            aluno_existente = session.query(cls).filter_by(cpf=cpf).first()
            if aluno_existente:
                raise AlunoJaExisteError("Já existe um aluno com esse CPF!")
            
            novo_aluno = cls(cpf=cpf, nome=nome)
            session.add(novo_aluno)
            session.commit()
            
            print(f"\nAluno {nome} cadastrado com sucesso!")
        
        except (CPFInvalidoError, AlunoJaExisteError) as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    @classmethod
    def criar_aluno_com_tratamento(cls):
        try:
            cls.criar_aluno()
        except (CPFInvalidoError, AlunoJaExisteError) as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def mostrar_disciplinas_e_notas(self, session):
        if not self.notas:
            raise NenhumaDisciplinaEncontradaError("O aluno não está matriculado em nenhuma disciplina.")

        print(f"\nDisciplinas e notas do aluno {self.nome} (CPF: {self.cpf}):")
        for nota in self.notas:
            disciplina_nome = nota.disciplina.nome if nota.disciplina else "Disciplina desconhecida"
            av1 = nota.av1 if nota.av1 is not None else "nota indisponível"
            av2 = nota.av2 if nota.av2 is not None else "nota indisponível"
            media = nota.media() if (nota.av1 is not None and nota.av2 is not None) else "nota indisponível"

            print(f"Disciplina: {disciplina_nome}")
            print(f"  AV1: {av1}")
            print(f"  AV2: {av2}")
            print(f"  Média: {media}")

    @classmethod
    def consultar_disciplinas_e_notas_com_tratamento(cls, session):
        cpf = input("Digite o CPF do aluno: ").strip()
        aluno = session.query(cls).filter_by(cpf=cpf).first()
        if not aluno:
            print("Aluno não encontrado.")
            return
        try:
            aluno.mostrar_disciplinas_e_notas(session)
        except NenhumaDisciplinaEncontradaError as e:
            print(e)

    @classmethod
    def listar_turma(cls, session):
        
            cpf = input("Digite o CPF do aluno: ").strip()
            aluno = session.query(Aluno).filter_by(cpf=cpf).first()

            if aluno:
                print(f'Aluno: {aluno.nome}')
                if aluno.turma:
                    print(f"Turma: {aluno.turma.nome} - Período: {aluno.turma.periodo}")

                else:
                    print("Este aluno não está matriculado em nenhuma turma.")
            else:
                print("Aluno não encontrado.")



        
    @classmethod
    def adicionar_turma(cls, session):
            try:
                cpf = input("Digite o CPF do aluno (somente números): ").strip()
                if not cpf.isdigit():
                    raise ValueError("CPF inválido.")
                cpf = int(cpf)

                aluno = session.query(cls).filter_by(cpf=cpf).first()
                if not aluno:
                     print("Aluno não encontrado.")
                     return
                turma_nome = input("Digite o nome da turma: ").strip()
                turma = session.query(Turma).filter_by(nome=turma_nome).first()
                if not turma:
                    print("Turma não encontrada.")
                    return
                
                aluno.turma = turma
                session.commit()

                print(f"Aluno {aluno.nome} foi adicionado à turma {turma.nome} com sucesso!")

            except Exception as e:
                print(f"Ocorreu um erro ao adicionar o aluno à turma: {e}")

