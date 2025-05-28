# teste_criar_tabelas.py
from database import Base, engine
import modelos  # importa tudo que está no __init__.py de modelos

def criar_tabelas():
    # Criar todas as tabelas no banco
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    criar_tabelas()