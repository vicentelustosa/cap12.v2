from interface.menu import Menu
from interface.telas import TelaUsuarios


class MenuUsuarios(Menu):
    def __init__(self, usuario_service):
        self.__service = usuario_service
        self.__tela = TelaUsuarios()

    def exibir_opcoes(self):
        print("\n=== USUÁRIOS ===\n1 - Cadastrar usuário\n2 - Listar usuários\n3 - Buscar usuário\n4 - Remover usuário\n0 - Voltar")

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                usuario = self.__service.cadastrar(input("Nome do usuário: "))
                self.__tela.sucesso(f"Usuário '{usuario.nome}' cadastrado.")
            elif opcao == "2":
                self.__tela.exibir(self.__service.listar())
            elif opcao == "3":
                usuario = self.__service.buscar(input("Nome do usuário: "))
                self.__tela.exibir([usuario]) if usuario else self.__tela.erro("Usuário não encontrado.")
            elif opcao == "4":
                self.__service.remover(input("Nome do usuário: "))
                self.__tela.sucesso("Usuário removido.")
            elif opcao == "0":
                return False
            else:
                self.__tela.erro("Opção inválida.")
        except ValueError as erro:
            self.__tela.erro(str(erro))
        return True
