from database import Base, engine, session
from modelos import Aluno, Turma, Nota, Professor, Disciplina

def test_criar_aluno_com_notas():
    # Cria todas as tabelas (turmas, alunos, notas, disciplinas)
    Base.metadata.create_all(engine)

    # Criar uma turma
    turma = Turma(nome="1A", periodo="Manhã")
    session.add(turma)

    # Criar uma disciplina
    disciplina = Disciplina(nome="Matemática")
    session.add(disciplina)
    session.commit()

    # Criar aluno e vincular à turma
    aluno = Aluno(cpf=12345678901, nome="João Silva")
    aluno.turma = turma
    session.add(aluno)
    session.commit()

    # Criar nota vinculada ao aluno e disciplina
    nota1 = Nota(aluno_cpf=aluno.cpf, disciplina_nome=disciplina.nome, av1=7.5, av2=8.0)
    session.add(nota1)
    session.commit()

    # Buscar aluno e imprimir notas
    aluno_no_db = session.query(Aluno).filter_by(cpf=12345678901).first()
    aluno_no_db.consultar_notas()

    # Verificações básicas
    assert aluno_no_db.turma.nome == "1A"
    assert len(aluno_no_db.notas) == 1
    assert aluno_no_db.notas[0].disciplina_nome == "Matemática"

    session.close()

if __name__ == "__main__":
    test_criar_aluno_com_notas()
