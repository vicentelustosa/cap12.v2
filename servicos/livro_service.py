# Python — servicos/livro_service.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelos.livro import Livro
from modelos.emprestimo import Emprestimo


class LivroService:

    def __init__(self, sessao: Session):
        self.__sessao = sessao

    def cadastrar(self, titulo: str) -> Livro:
        titulo = titulo.strip()

        if not titulo:
            raise ValueError(
                "O título do livro não pode ser vazio."
            )

        livro = Livro(titulo=titulo)

        try:
            self.__sessao.add(livro)
            self.__sessao.commit()

        except Exception:
            self.__sessao.rollback()
            raise

        return livro

    def listar(self) -> list[Livro]:
        comando = select(Livro).order_by(
            Livro.titulo,
            Livro.id
        )

        return self.__sessao.scalars(comando).all()

    def buscar(self, id_livro: int) -> Livro | None:
        return self.__sessao.get(Livro, id_livro)

    def remover(self, id_livro: int) -> None:
        livro = self.buscar(id_livro)

        if livro is None:
            raise ValueError("Livro não encontrado.")

        comando = select(Emprestimo.id).where(
            Emprestimo.livro_id == livro.id
        )

        emprestimo_id = self.__sessao.scalars(
            comando
        ).first()

        if emprestimo_id is not None:
            raise ValueError(
                "O livro possui histórico de empréstimos "
                "e não pode ser removido."
            )

        try:
            self.__sessao.delete(livro)
            self.__sessao.commit()

        except Exception:
            self.__sessao.rollback()
            raise