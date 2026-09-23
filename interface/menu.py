from abc import ABC, abstractmethod


class Menu(ABC):
    def executar(self):
        while True:
            self.exibir_opcoes()
            if not self.processar_opcao(input("Escolha uma opção: ")):
                break

    @abstractmethod
    def exibir_opcoes(self):
        pass

    @abstractmethod
    def processar_opcao(self, opcao):
        pass
