import json
from pathlib import Path

from modelos import Usuario


class UsuarioPersistencia:
    def __init__(self, arquivo):
        self.__arquivo = Path(arquivo)

    def salvar(self, usuarios):
        self.__arquivo.parent.mkdir(parents=True, exist_ok=True)
        with self.__arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump([{"nome": usuario.nome} for usuario in usuarios], arquivo, ensure_ascii=False, indent=4)

    def carregar(self):
        if not self.__arquivo.exists():
            return []
        with self.__arquivo.open(encoding="utf-8") as arquivo:
            return [Usuario(item["nome"]) for item in json.load(arquivo)]
