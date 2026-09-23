from interface.telas.tela import Tela


class TelaEmprestimos(Tela):
    def exibir_titulo(self):
        print("\n=== EMPRÉSTIMOS ===")

    def exibir_conteudo(self, emprestimos):
        if not emprestimos:
            self.aviso("Nenhum empréstimo ativo.")
            return
        for indice, emprestimo in enumerate(emprestimos, start=1):
            print(f"{indice} - Livro: {emprestimo.livro.titulo} | Usuário: {emprestimo.usuario.nome}")
