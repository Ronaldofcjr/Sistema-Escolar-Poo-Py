from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta
from abc import ABCMeta

class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    pass

Base = declarative_base(metaclass=DeclarativeABCMeta)

engine = create_engine('sqlite:///meu_banco.db')

Session = sessionmaker(bind=engine)
session = Session()