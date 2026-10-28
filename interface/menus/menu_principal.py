from interface.menu import Menu
from interface.menus.menu_livros import MenuLivros
from interface.menus.menu_usuarios import MenuUsuarios
from interface.menus.menu_emprestimos import MenuEmprestimos


class MenuPrincipal(Menu):

    def __init__(self, aplicacao):
        self.__menu_livros = MenuLivros(
            aplicacao.livro_service
        )

        self.__menu_usuarios = MenuUsuarios(
            aplicacao.usuario_service
        )

        self.__menu_emprestimos = MenuEmprestimos(
            aplicacao.emprestimo_service
        )

    def exibir_opcoes(self):
        print(
            "\n=== SISTEMA DE BIBLIOTECA ==="
            "\n1 - Livros"
            "\n2 - Usuários"
            "\n3 - Empréstimos"
            "\n0 - Sair"
        )

    def processar_opcao(self, opcao):
        if opcao == "1":
            self.__menu_livros.executar()

        elif opcao == "2":
            self.__menu_usuarios.executar()

        elif opcao == "3":
            self.__menu_emprestimos.executar()

        elif opcao == "0":
            print("\nEncerrando sistema...")
            return False

        else:
            print("\n[ERRO] Opção inválida.")

        return True