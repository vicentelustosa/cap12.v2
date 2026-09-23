class Livro:
    def __init__(self, titulo: str):
        self.titulo = titulo

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str):
        self.__titulo = valor.strip()

    def __str__(self):
        return self.titulo
