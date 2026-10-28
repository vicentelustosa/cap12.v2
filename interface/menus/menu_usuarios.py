# Python — interface/menus/menu_usuarios.py

from interface.menu import Menu
from interface.telas import TelaUsuarios


class MenuUsuarios(Menu):

    def __init__(self, usuario_service):
        self.__service = usuario_service
        self.__tela = TelaUsuarios()

    def exibir_opcoes(self):
        print(
            "\n=== USUÁRIOS ==="
            "\n1 - Cadastrar usuário"
            "\n2 - Listar usuários"
            "\n3 - Buscar usuário"
            "\n4 - Remover usuário"
            "\n0 - Voltar"
        )

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                usuario = self.__service.cadastrar(
                    input("Nome do usuário: ")
                )

                self.__tela.sucesso(
                    f"Usuário '{usuario.nome}' "
                    f"cadastrado com ID {usuario.id}."
                )

            elif opcao == "2":
                usuarios = self.__service.listar()
                self.__tela.exibir(usuarios)

            elif opcao == "3":
                termo = input(
                    "Trecho do nome para buscar: "
                )

                usuarios = self.__service.buscar_por_nome(
                    termo
                )

                if usuarios:
                    self.__tela.exibir(usuarios)
                else:
                    self.__tela.erro(
                        "Nenhum usuário encontrado."
                    )

            elif opcao == "4":
                id_usuario = int(
                    input("ID do usuário a remover: ")
                )

                self.__service.remover(id_usuario)

                self.__tela.sucesso(
                    "Usuário removido."
                )

            elif opcao == "0":
                return False

            else:
                self.__tela.erro("Opção inválida.")

        except ValueError as erro:
            self.__tela.erro(str(erro))

        return True