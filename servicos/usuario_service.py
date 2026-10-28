# Python — servicos/usuario_service.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelos.usuario import Usuario
from modelos.emprestimo import Emprestimo


class UsuarioService:

    def __init__(self, sessao: Session):
        self.__sessao = sessao

    def cadastrar(self, nome: str) -> Usuario:
        nome = nome.strip()

        if not nome:
            raise ValueError(
                "O nome do usuário não pode ser vazio."
            )

        usuario = Usuario(nome=nome)

        try:
            self.__sessao.add(usuario)
            self.__sessao.commit()

        except Exception:
            self.__sessao.rollback()
            raise

        return usuario

    def listar(self) -> list[Usuario]:
        comando = select(Usuario).order_by(
            Usuario.nome,
            Usuario.id
        )

        return self.__sessao.scalars(comando).all()

    def buscar(self, id_usuario: int) -> Usuario | None:
        return self.__sessao.get(Usuario, id_usuario)

    def remover(self, id_usuario: int) -> None:
        usuario = self.buscar(id_usuario)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        comando = select(Emprestimo.id).where(
            Emprestimo.usuario_id == usuario.id
        )

        emprestimo_id = self.__sessao.scalars(
            comando
        ).first()

        if emprestimo_id is not None:
            raise ValueError(
                "O usuário possui histórico de empréstimos "
                "e não pode ser removido."
            )

        try:
            self.__sessao.delete(usuario)
            self.__sessao.commit()

        except Exception:
            self.__sessao.rollback()
            raise