# Python — modelos/usuario.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modelos.base import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(200)
    )

    emprestimos: Mapped[list["Emprestimo"]] = relationship(
        back_populates="usuario"
    )

    def __str__(self) -> str:
        return self.nome