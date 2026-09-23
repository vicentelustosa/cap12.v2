import json
from pathlib import Path

from modelos import Livro


class LivroPersistencia:
    def __init__(self, arquivo):
        self.__arquivo = Path(arquivo)

    def salvar(self, livros):
        self.__arquivo.parent.mkdir(parents=True, exist_ok=True)
        with self.__arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump([{"titulo": livro.titulo} for livro in livros], arquivo, ensure_ascii=False, indent=4)

    def carregar(self):
        if not self.__arquivo.exists():
            return []
        with self.__arquivo.open(encoding="utf-8") as arquivo:
            return [Livro(item["titulo"]) for item in json.load(arquivo)]
