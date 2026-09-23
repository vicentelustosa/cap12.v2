from interface.menu import Menu
from interface.telas import TelaLivros


class MenuLivros(Menu):
    def __init__(self, livro_service):
        self.__service = livro_service
        self.__tela = TelaLivros()

    def exibir_opcoes(self):
        print("\n=== LIVROS ===\n1 - Cadastrar livro\n2 - Listar livros\n3 - Buscar livro\n4 - Remover livro\n0 - Voltar")

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                livro = self.__service.cadastrar(input("Título do livro: "))
                self.__tela.sucesso(f"Livro '{livro.titulo}' cadastrado.")
            elif opcao == "2":
                self.__tela.exibir(self.__service.listar())
            elif opcao == "3":
                livro = self.__service.buscar(input("Título do livro: "))
                self.__tela.exibir([livro]) if livro else self.__tela.erro("Livro não encontrado.")
            elif opcao == "4":
                self.__service.remover(input("Título do livro: "))
                self.__tela.sucesso("Livro removido.")
            elif opcao == "0":
                return False
            else:
                self.__tela.erro("Opção inválida.")
        except ValueError as erro:
            self.__tela.erro(str(erro))
        return True
