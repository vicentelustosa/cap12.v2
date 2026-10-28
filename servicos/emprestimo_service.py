# Python — servicos/emprestimo_service.py

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from modelos.livro import Livro
from modelos.usuario import Usuario
from modelos.emprestimo import Emprestimo


class EmprestimoService:

    def __init__(self, sessao: Session):
        self.__sessao = sessao

    def emprestar(
        self,
        id_livro: int,
        id_usuario: int
    ) -> Emprestimo:

        livro = self.__sessao.get(
            Livro,
            id_livro
        )

        if livro is None:
            raise ValueError("Livro não encontrado.")

        usuario = self.__sessao.get(
            Usuario,
            id_usuario
        )

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        comando = select(Emprestimo.id).where(
            Emprestimo.livro_id == livro.id,
            Emprestimo.data_devolucao.is_(None)
        )

        emprestimo_id = self.__sessao.scalars(
            comando
        ).first()

        if emprestimo_id is not None:
            raise ValueError(
                "O livro já está emprestado."
            )

        emprestimo = Emprestimo(
            usuario=usuario,
            livro=livro
        )

        try:
            self.__sessao.add(emprestimo)
            self.__sessao.commit()
            self.__sessao.refresh(emprestimo)

        except Exception:
            self.__sessao.rollback()
            raise

        return emprestimo

    def listar(self) -> list[Emprestimo]:
        comando = select(Emprestimo).order_by(
            Emprestimo.id
        )

        return self.__sessao.scalars(comando).all()

    def devolver(self, id_livro: int) -> Emprestimo:
        livro = self.__sessao.get(
            Livro,
            id_livro
        )

        if livro is None:
            raise ValueError("Livro não encontrado.")

        comando = select(Emprestimo).where(
            Emprestimo.livro_id == livro.id,
            Emprestimo.data_devolucao.is_(None)
        )

        emprestimo = self.__sessao.scalars(
            comando
        ).first()

        if emprestimo is None:
            raise ValueError(
                "O livro não está emprestado."
            )

        try:
            emprestimo.data_devolucao = func.now()

            self.__sessao.commit()
            self.__sessao.refresh(emprestimo)

        except Exception:
            self.__sessao.rollback()
            raise

        return emprestimo