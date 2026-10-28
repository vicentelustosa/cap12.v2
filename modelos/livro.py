# Python — modelos/livro.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modelos.base import Base


class Livro(Base):

    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(200)
    )

    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        back_populates="livro"
    )

    def __str__(self) -> str:
        return self.titulo