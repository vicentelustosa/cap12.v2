# Python — modelos/emprestimo.py

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from modelos.base import Base
from modelos.livro import Livro
from modelos.usuario import Usuario


class Emprestimo(Base):

    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livros.id")
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    data_emprestimo: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    data_devolucao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )

    livro: Mapped["Livro"] = relationship(
        back_populates="emprestimos"
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="emprestimos"
    )

    def __str__(self) -> str:
        data_formatada = self.data_emprestimo.strftime(
            "%d/%m/%Y às %H:%M"
        )

        if self.data_devolucao is None:
            situacao = "Em andamento"
        else:
            situacao = (
                "Devolvido em "
                + self.data_devolucao.strftime(
                    "%d/%m/%Y às %H:%M"
                )
            )

        return (
            f"{self.usuario.nome} → {self.livro.titulo} "
            f"(Emprestado em {data_formatada}; {situacao})"
        )