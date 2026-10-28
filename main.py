# Python — main.py
from aplicacao import Aplicacao
from interface import MenuPrincipal


def main():
    with Aplicacao() as aplicacao:
        menu = MenuPrincipal(aplicacao)
        menu.executar()


if __name__ == "__main__":
    main()