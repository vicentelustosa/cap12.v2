from interface.telas.tela import Tela


class TelaUsuarios(Tela):
    def exibir_titulo(self):
        print("\n=== USUÁRIOS ===")

    def exibir_conteudo(self, usuarios):
        if not usuarios:
            self.aviso("Nenhum usuário cadastrado.")
            return
        for indice, usuario in enumerate(usuarios, start=1):
            print(f"{indice} - {usuario.nome}")
