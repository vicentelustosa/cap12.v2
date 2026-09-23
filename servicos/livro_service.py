from modelos import Livro


class LivroService:
    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def cadastrar(self, titulo: str):
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("O título do livro não pode ser vazio.")
        if self.__biblioteca.buscar_livro(titulo):
            raise ValueError("Já existe um livro com esse título.")
        livro = Livro(titulo)
        self.__biblioteca.adicionar_livro(livro)
        self.__biblioteca.salvar()
        return livro

    def listar(self):
        return self.__biblioteca.listar_livros()

    def buscar(self, titulo: str):
        return self.__biblioteca.buscar_livro(titulo.strip())

    def remover(self, titulo: str):
        livro = self.buscar(titulo)
        if livro is None:
            raise ValueError("Livro não encontrado.")
        if any(e.livro == livro for e in self.__biblioteca.listar_emprestimos()):
            raise ValueError("O livro está emprestado e não pode ser removido.")
        self.__biblioteca.remover_livro(livro)
        self.__biblioteca.salvar()
