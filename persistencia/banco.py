# Python — persistencia/banco.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from modelos.base import Base
from modelos import livro, usuario, emprestimo


engine = create_engine("sqlite:///biblioteca.db")


def criar_tabelas() -> None:
    Base.metadata.create_all(engine)


def criar_sessao() -> Session:
    return Session(engine)