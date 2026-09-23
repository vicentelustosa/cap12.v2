from modelos import Usuario


class UsuarioService:
    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def cadastrar(self, nome: str):
        nome = nome.strip()
        if not nome:
            raise ValueError("O nome do usuário não pode ser vazio.")
        if self.__biblioteca.buscar_usuario(nome):
            raise ValueError("Já existe um usuário com esse nome.")
        usuario = Usuario(nome)
        self.__biblioteca.adicionar_usuario(usuario)
        self.__biblioteca.salvar()
        return usuario

    def listar(self):
        return self.__biblioteca.listar_usuarios()

    def buscar(self, nome: str):
        return self.__biblioteca.buscar_usuario(nome.strip())

    def remover(self, nome: str):
        usuario = self.buscar(nome)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")
        if any(e.usuario == usuario for e in self.__biblioteca.listar_emprestimos()):
            raise ValueError("O usuário possui empréstimo ativo e não pode ser removido.")
        self.__biblioteca.remover_usuario(usuario)
        self.__biblioteca.salvar()
