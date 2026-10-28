from sqlalchemy.orm import Session

from persistencia.banco import (
    criar_sessao,
    criar_tabelas
)

from servicos.livro_service import LivroService
from servicos.usuario_service import UsuarioService
from servicos.emprestimo_service import EmprestimoService


class Aplicacao:

    def __init__(self):
        criar_tabelas()
        self.__sessao: Session | None = None

        self.__livro_service = None
        self.__usuario_service = None
        self.__emprestimo_service = None

    def __enter__(self):
        self.__sessao = criar_sessao()

        self.__livro_service = LivroService(
            self.sessao
        )

        self.__usuario_service = UsuarioService(
            self.sessao
        )

        self.__emprestimo_service = EmprestimoService(
            self.sessao
        )

        return self

    def __exit__(
        self,
        tipo_excecao,
        excecao,
        traceback
    ):
        if self.__sessao is not None:
            self.__sessao.close()
            self.__sessao = None

    @property
    def sessao(self) -> Session:
        if self.__sessao is None:
            raise RuntimeError(
                "A aplicação não foi inicializada."
            )

        return self.__sessao

    @property
    def livro_service(self) -> LivroService:
        if self.__livro_service is None:
            raise RuntimeError(
                "A aplicação não foi inicializada."
            )

        return self.__livro_service

    @property
    def usuario_service(self) -> UsuarioService:
        if self.__usuario_service is None:
            raise RuntimeError(
                "A aplicação não foi inicializada."
            )

        return self.__usuario_service

    @property
    def emprestimo_service(self) -> EmprestimoService:
        if self.__emprestimo_service is None:
            raise RuntimeError(
                "A aplicação não foi inicializada."
            )

        return self.__emprestimo_service