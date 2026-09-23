from aplicacao import Biblioteca
from interface import MenuPrincipal
from persistencia import EmprestimoPersistencia, LivroPersistencia, UsuarioPersistencia
from servicos import EmprestimoService, LivroService, UsuarioService


def main():
    biblioteca = Biblioteca(
        LivroPersistencia("dados/livros.json"),
        UsuarioPersistencia("dados/usuarios.json"),
        EmprestimoPersistencia("dados/emprestimos.json"),
    )
    menu = MenuPrincipal(
        LivroService(biblioteca),
        UsuarioService(biblioteca),
        EmprestimoService(biblioteca),
    )
    menu.executar()


if __name__ == "__main__":
    main()
