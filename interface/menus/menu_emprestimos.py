# Python — interface/menus/menu_emprestimos.py

from interface.menu import Menu
from interface.telas import TelaEmprestimos


class MenuEmprestimos(Menu):

    def __init__(self, emprestimo_service):
        self.__service = emprestimo_service
        self.__tela = TelaEmprestimos()

    def exibir_opcoes(self):
        print(
            "\n=== EMPRÉSTIMOS ==="
            "\n1 - Realizar empréstimo"
            "\n2 - Listar empréstimos"
            "\n3 - Devolver livro"
            "\n0 - Voltar"
        )

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                id_livro = int(
                    input("ID do livro: ")
                )

                id_usuario = int(
                    input("ID do usuário: ")
                )

                emprestimo = self.__service.emprestar(
                    id_livro,
                    id_usuario
                )

                self.__tela.sucesso(
                    f"Empréstimo realizado: "
                    f"'{emprestimo.livro.titulo}' "
                    f"para {emprestimo.usuario.nome}."
                )

            elif opcao == "2":
                emprestimos = self.__service.listar()
                self.__tela.exibir(emprestimos)

            elif opcao == "3":
                id_livro = int(
                    input("ID do livro a devolver: ")
                )

                emprestimo = self.__service.devolver(
                    id_livro
                )

                self.__tela.sucesso(
                    f"Livro '{emprestimo.livro.titulo}' "
                    f"devolvido."
                )

            elif opcao == "0":
                return False

            else:
                self.__tela.erro("Opção inválida.")

        except ValueError as erro:
            self.__tela.erro(str(erro))

        return True