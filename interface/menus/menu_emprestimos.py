from interface.menu import Menu
from interface.telas import TelaEmprestimos


class MenuEmprestimos(Menu):
    def __init__(self, emprestimo_service):
        self.__service = emprestimo_service
        self.__tela = TelaEmprestimos()

    def exibir_opcoes(self):
        print("\n=== EMPRÉSTIMOS ===\n1 - Realizar empréstimo\n2 - Listar empréstimos\n3 - Devolver livro\n0 - Voltar")

    def processar_opcao(self, opcao):
        try:
            if opcao == "1":
                emprestimo = self.__service.emprestar(input("Título do livro: "), input("Nome do usuário: "))
                self.__tela.sucesso(f"Empréstimo realizado: {emprestimo.livro.titulo} para {emprestimo.usuario.nome}.")
            elif opcao == "2":
                self.__tela.exibir(self.__service.listar())
            elif opcao == "3":
                emprestimo = self.__service.devolver(input("Título do livro: "))
                self.__tela.sucesso(f"Livro '{emprestimo.livro.titulo}' devolvido.")
            elif opcao == "0":
                return False
            else:
                self.__tela.erro("Opção inválida.")
        except ValueError as erro:
            self.__tela.erro(str(erro))
        return True
