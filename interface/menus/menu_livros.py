# Python — interface/menus/menu_livros.py

from interface.menu import Menu
from interface.telas import TelaLivros


class MenuLivros(Menu):

    def __init__(self, livro_service):
        self.__service = livro_service
        self.__tela = TelaLivros()

    def exibir_opcoes(self):
        print(
            "\n=== LIVROS ==="
            "\n1 - Cadastrar livro"
            "\n2 - Listar livros"
            "\n3 - Buscar livro"
            "\n4 - Remover livro"
            "\n0 - Voltar"
        )

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                livro = self.__service.cadastrar(
                    input("Título do livro: ")
                )

                self.__tela.sucesso(
                    f"Livro '{livro.titulo}' cadastrado "
                    f"com ID {livro.id}."
                )

            elif opcao == "2":
                livros = self.__service.listar()
                self.__tela.exibir(livros)

            elif opcao == "3":
                termo = input(
                    "Trecho do título para buscar: "
                )

                livros = self.__service.buscar_por_titulo(
                    termo
                )

                if livros:
                    self.__tela.exibir(livros)
                else:
                    self.__tela.erro(
                        "Nenhum livro encontrado."
                    )

            elif opcao == "4":
                id_livro = int(
                    input("ID do livro a remover: ")
                )

                self.__service.remover(id_livro)

                self.__tela.sucesso(
                    "Livro removido."
                )

            elif opcao == "0":
                return False

            else:
                self.__tela.erro("Opção inválida.")

        except ValueError as erro:
            self.__tela.erro(str(erro))

        return True