from abc import ABC, abstractmethod


class Tela(ABC):
    def exibir(self, dados):
        self.exibir_titulo()
        self.exibir_conteudo(dados)
        input("\nPressione ENTER para continuar...")

    def sucesso(self, mensagem):
        self.__alerta("SUCESSO", mensagem)

    def erro(self, mensagem):
        self.__alerta("ERRO", mensagem)

    def aviso(self, mensagem):
        self.__alerta("AVISO", mensagem)

    def __alerta(self, tipo, mensagem):
        print(f"\n[{tipo}] {mensagem}")

    @abstractmethod
    def exibir_titulo(self):
        pass

    @abstractmethod
    def exibir_conteudo(self, dados):
        pass
