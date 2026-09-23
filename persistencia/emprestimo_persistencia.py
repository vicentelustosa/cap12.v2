import json
from pathlib import Path

from modelos import Emprestimo


class EmprestimoPersistencia:
    def __init__(self, arquivo):
        self.__arquivo = Path(arquivo)

    def salvar(self, emprestimos):
        self.__arquivo.parent.mkdir(parents=True, exist_ok=True)
        dados = [{"livro": e.livro.titulo, "usuario": e.usuario.nome} for e in emprestimos]
        with self.__arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self, livros, usuarios):
        if not self.__arquivo.exists():
            return []
        with self.__arquivo.open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        emprestimos = []
        for item in dados:
            livro = next((livro for livro in livros if livro.titulo == item["livro"]), None)
            usuario = next((usuario for usuario in usuarios if usuario.nome == item["usuario"]), None)
            if livro is not None and usuario is not None:
                emprestimos.append(Emprestimo(usuario, livro))
        return emprestimos
