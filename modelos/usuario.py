class Usuario:
    def __init__(self, nome: str):
        self.nome = nome

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str):
        self.__nome = valor.strip()

    def __str__(self):
        return self.nome
