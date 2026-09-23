from modelos import Livro, Usuario, Emprestimo


class Biblioteca:
    def __init__(self, livro_persistencia, usuario_persistencia, emprestimo_persistencia):
        self.__livro_persistencia = livro_persistencia
        self.__usuario_persistencia = usuario_persistencia
        self.__emprestimo_persistencia = emprestimo_persistencia
        self.__livros = self.__livro_persistencia.carregar()
        self.__usuarios = self.__usuario_persistencia.carregar()
        self.__emprestimos = self.__emprestimo_persistencia.carregar(
            self.__livros, self.__usuarios
        )

    def adicionar_livro(self, livro: Livro):
        self.__livros.append(livro)

    def listar_livros(self):
        return self.__livros

    def buscar_livro(self, titulo: str):
        return next((livro for livro in self.__livros if livro.titulo == titulo), None)

    def remover_livro(self, livro: Livro):
        self.__livros.remove(livro)

    def adicionar_usuario(self, usuario: Usuario):
        self.__usuarios.append(usuario)

    def listar_usuarios(self):
        return self.__usuarios

    def buscar_usuario(self, nome: str):
        return next((usuario for usuario in self.__usuarios if usuario.nome == nome), None)

    def remover_usuario(self, usuario: Usuario):
        self.__usuarios.remove(usuario)

    def adicionar_emprestimo(self, emprestimo: Emprestimo):
        self.__emprestimos.append(emprestimo)

    def listar_emprestimos(self):
        return self.__emprestimos

    def remover_emprestimo(self, emprestimo: Emprestimo):
        self.__emprestimos.remove(emprestimo)

    def salvar(self):
        self.__livro_persistencia.salvar(self.__livros)
        self.__usuario_persistencia.salvar(self.__usuarios)
        self.__emprestimo_persistencia.salvar(self.__emprestimos)
