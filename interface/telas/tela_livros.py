from interface.telas.tela import Tela


class TelaLivros(Tela):
    def exibir_titulo(self):
        print("\n=== LIVROS ===")

    def exibir_conteudo(self, livros):
        if not livros:
            self.aviso("Nenhum livro cadastrado.")
            return
        for livro in livros:
            print(livro)
