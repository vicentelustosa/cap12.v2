from modelos import Emprestimo


class EmprestimoService:
    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def emprestar(self, titulo_livro: str, nome_usuario: str):
        livro = self.__biblioteca.buscar_livro(titulo_livro.strip())
        if livro is None:
            raise ValueError("Livro não encontrado.")
        usuario = self.__biblioteca.buscar_usuario(nome_usuario.strip())
        if usuario is None:
            raise ValueError("Usuário não encontrado.")
        if any(e.livro == livro for e in self.__biblioteca.listar_emprestimos()):
            raise ValueError("O livro já está emprestado.")
        emprestimo = Emprestimo(usuario, livro)
        self.__biblioteca.adicionar_emprestimo(emprestimo)
        self.__biblioteca.salvar()
        return emprestimo

    def listar(self):
        return self.__biblioteca.listar_emprestimos()

    def devolver(self, titulo_livro: str):
        livro = self.__biblioteca.buscar_livro(titulo_livro.strip())
        if livro is None:
            raise ValueError("Livro não encontrado.")
        for emprestimo in self.__biblioteca.listar_emprestimos():
            if emprestimo.livro == livro:
                self.__biblioteca.remover_emprestimo(emprestimo)
                self.__biblioteca.salvar()
                return emprestimo
        raise ValueError("O livro não está emprestado.")
