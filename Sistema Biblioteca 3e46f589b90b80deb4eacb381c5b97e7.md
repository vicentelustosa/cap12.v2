# Sistema Biblioteca

A partir da estrutura construída no capítulo e mantendo a organização da versão anterior — especialmente `aplicacao.py` como único script da camada de aplicação e `interface/` organizada em **menus e telas** — o projeto final pode ser consolidado da seguinte forma.

A implementação abaixo incorpora também a nova regra discutida no capítulo: **um livro que já esteja emprestado não pode ser emprestado novamente até ser devolvido**.

## Estrutura completa

```
biblioteca/
│
├── main.py
├── aplicacao.py
│
├── modelos/
│   ├── __init__.py
│   ├── livro.py
│   ├── usuario.py
│   └── emprestimo.py
│
├── servicos/
│   ├── __init__.py
│   ├── livro_service.py
│   ├── usuario_service.py
│   └── emprestimo_service.py
│
├── persistencia/
│   ├── __init__.py
│   ├── livro_persistencia.py
│   ├── usuario_persistencia.py
│   └── emprestimo_persistencia.py
│
└── interface/
    ├── __init__.py
    ├── menu.py
    ├── menu_principal.py
    │
    ├── menus/
    │   ├── __init__.py
    │   ├── menu_principal.py
    │   ├── menu_livros.py
    │   ├── menu_usuarios.py
    │   └── menu_emprestimos.py
    │
    └── telas/
        ├── __init__.py
        ├── tela.py
        ├── tela_livros.py
        ├── tela_usuarios.py
        └── tela_emprestimos.py
```

Os arquivos JSON serão criados automaticamente em uma pasta `dados/` quando houver dados para salvar:

```
biblioteca/
│
└── dados/
    ├── livros.json
    ├── usuarios.json
    └── emprestimos.json
```

---

# 1. Modelos

## `modelos/livro.py`

```python
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
```

## `modelos/usuario.py`

```python
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
```

## `modelos/emprestimo.py`

```python
class Emprestimo:

    def __init__(self, usuario, livro):
        self.usuario = usuario
        self.livro = livro

    def __str__(self):
        return (
            f"{self.livro.titulo} -> "
            f"{self.usuario.nome}"
        )
```

## `modelos/__init__.py`

```python
from modelos.livro import Livro
from modelos.usuario import Usuario
from modelos.emprestimo import Emprestimo

__all__ = [
    "Livro",
    "Usuario",
    "Emprestimo"
]
```

---

# 2. Aplicação

Aqui fica o único script que representa a camada da aplicação.

## `aplicacao.py`

```python
from modelos import Livro, Usuario, Emprestimo

class Biblioteca:

    def __init__(
        self,
        livro_persistencia,
        usuario_persistencia,
        emprestimo_persistencia
    ):
        self.__livro_persistencia = livro_persistencia
        self.__usuario_persistencia = usuario_persistencia
        self.__emprestimo_persistencia = (
            emprestimo_persistencia
        )

        self.__livros = (
            self.__livro_persistencia.carregar()
        )

        self.__usuarios = (
            self.__usuario_persistencia.carregar()
        )

        self.__emprestimos = (
            self.__emprestimo_persistencia.carregar(
                self.__livros,
                self.__usuarios
            )
        )

    # =========================
    # LIVROS
    # =========================

    def adicionar_livro(self, livro: Livro):
        self.__livros.append(livro)

    def listar_livros(self):
        return self.__livros

    def buscar_livro(self, titulo: str):
        for livro in self.__livros:
            if livro.titulo == titulo:
                return livro

        return None

    def remover_livro(self, livro: Livro):
        self.__livros.remove(livro)

    # =========================
    # USUÁRIOS
    # =========================

    def adicionar_usuario(self, usuario: Usuario):
        self.__usuarios.append(usuario)

    def listar_usuarios(self):
        return self.__usuarios

    def buscar_usuario(self, nome: str):
        for usuario in self.__usuarios:
            if usuario.nome == nome:
                return usuario

        return None

    def remover_usuario(self, usuario: Usuario):
        self.__usuarios.remove(usuario)

    # =========================
    # EMPRÉSTIMOS
    # =========================

    def adicionar_emprestimo(
        self,
        emprestimo: Emprestimo
    ):
        self.__emprestimos.append(emprestimo)

    def listar_emprestimos(self):
        return self.__emprestimos

    def remover_emprestimo(
        self,
        emprestimo: Emprestimo
    ):
        self.__emprestimos.remove(emprestimo)

    # =========================
    # PERSISTÊNCIA
    # =========================

    def salvar(self):

        self.__livro_persistencia.salvar(
            self.__livros
        )

        self.__usuario_persistencia.salvar(
            self.__usuarios
        )

        self.__emprestimo_persistencia.salvar(
            self.__emprestimos
        )
```

Observe que a `Biblioteca` não possui mais métodos como `cadastrar_livro()` ou `emprestar_livro()`.

Ela fornece operações controladas sobre o estado:

```python
adicionar_livro()
buscar_livro()
remover_livro()
```

As regras de negócio ficam nos serviços.

---

# 3. Serviços

## `servicos/livro_service.py`

```python
from modelos import Livro

class LivroService:

    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def cadastrar(self, titulo: str):

        titulo = titulo.strip()

        if not titulo:
            raise ValueError(
                "O título do livro não pode ser vazio."
            )

        if self.__biblioteca.buscar_livro(titulo):
            raise ValueError(
                "Já existe um livro com esse título."
            )

        livro = Livro(titulo)

        self.__biblioteca.adicionar_livro(livro)
        self.__biblioteca.salvar()

        return livro

    def listar(self):
        return self.__biblioteca.listar_livros()

    def buscar(self, titulo: str):
        return self.__biblioteca.buscar_livro(titulo)

    def remover(self, titulo: str):

        livro = self.__biblioteca.buscar_livro(
            titulo
        )

        if livro is None:
            raise ValueError(
                "Livro não encontrado."
            )

        for emprestimo in (
            self.__biblioteca.listar_emprestimos()
        ):
            if emprestimo.livro == livro:
                raise ValueError(
                    "O livro está emprestado e não pode "
                    "ser removido."
                )

        self.__biblioteca.remover_livro(livro)
        self.__biblioteca.salvar()
```

---

## `servicos/usuario_service.py`

```python
from modelos import Usuario

class UsuarioService:

    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def cadastrar(self, nome: str):

        nome = nome.strip()

        if not nome:
            raise ValueError(
                "O nome do usuário não pode ser vazio."
            )

        if self.__biblioteca.buscar_usuario(nome):
            raise ValueError(
                "Já existe um usuário com esse nome."
            )

        usuario = Usuario(nome)

        self.__biblioteca.adicionar_usuario(
            usuario
        )

        self.__biblioteca.salvar()

        return usuario

    def listar(self):
        return self.__biblioteca.listar_usuarios()

    def buscar(self, nome: str):
        return self.__biblioteca.buscar_usuario(nome)

    def remover(self, nome: str):

        usuario = self.__biblioteca.buscar_usuario(
            nome
        )

        if usuario is None:
            raise ValueError(
                "Usuário não encontrado."
            )

        for emprestimo in (
            self.__biblioteca.listar_emprestimos()
        ):
            if emprestimo.usuario == usuario:
                raise ValueError(
                    "O usuário possui empréstimo ativo "
                    "e não pode ser removido."
                )

        self.__biblioteca.remover_usuario(usuario)
        self.__biblioteca.salvar()
```

---

## `servicos/emprestimo_service.py`

Aqui está a parte mais importante da evolução das regras.

```python
from modelos import Emprestimo

class EmprestimoService:

    def __init__(self, biblioteca):
        self.__biblioteca = biblioteca

    def emprestar(
        self,
        titulo_livro: str,
        nome_usuario: str
    ):

        livro = self.__biblioteca.buscar_livro(
            titulo_livro
        )

        if livro is None:
            raise ValueError(
                "Livro não encontrado."
            )

        usuario = self.__biblioteca.buscar_usuario(
            nome_usuario
        )

        if usuario is None:
            raise ValueError(
                "Usuário não encontrado."
            )

        # Nova regra:
        # um livro não pode estar emprestado
        # para dois usuários simultaneamente.

        for emprestimo in (
            self.__biblioteca.listar_emprestimos()
        ):
            if emprestimo.livro == livro:
                raise ValueError(
                    "O livro já está emprestado."
                )

        emprestimo = Emprestimo(
            usuario,
            livro
        )

        self.__biblioteca.adicionar_emprestimo(
            emprestimo
        )

        self.__biblioteca.salvar()

        return emprestimo

    def listar(self):
        return self.__biblioteca.listar_emprestimos()

    def devolver(
        self,
        titulo_livro: str
    ):

        livro = self.__biblioteca.buscar_livro(
            titulo_livro
        )

        if livro is None:
            raise ValueError(
                "Livro não encontrado."
            )

        for emprestimo in (
            self.__biblioteca.listar_emprestimos()
        ):
            if emprestimo.livro == livro:

                self.__biblioteca.remover_emprestimo(
                    emprestimo
                )

                self.__biblioteca.salvar()

                return emprestimo

        raise ValueError(
            "O livro não está emprestado."
        )
```

Essa classe concentra as regras relacionadas à operação:

```
EmprestimoService
│
├── livro existe?
├── usuário existe?
├── livro está disponível?
├── cria empréstimo
└── devolve empréstimo
```

---

## `servicos/__init__.py`

```python
from servicos.livro_service import LivroService
from servicos.usuario_service import UsuarioService
from servicos.emprestimo_service import EmprestimoService

__all__ = [
    "LivroService",
    "UsuarioService",
    "EmprestimoService"
]
```

---

# 4. Persistência

## `persistencia/livro_persistencia.py`

```python
import json
import os

from modelos import Livro

class LivroPersistencia:

    def __init__(self, arquivo):
        self.__arquivo = arquivo

    def salvar(self, livros):

        self.__criar_diretorio()

        dados = []

        for livro in livros:
            dados.append({
                "titulo": livro.titulo
            })

        with open(
            self.__arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):

        if not os.path.exists(self.__arquivo):
            return []

        with open(
            self.__arquivo,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        livros = []

        for item in dados:
            livro = Livro(item["titulo"])
            livros.append(livro)

        return livros

    def __criar_diretorio(self):

        diretorio = os.path.dirname(
            self.__arquivo
        )

        if diretorio:
            os.makedirs(
                diretorio,
                exist_ok=True
            )
```

---

## `persistencia/usuario_persistencia.py`

```python
import json
import os

from modelos import Usuario

class UsuarioPersistencia:

    def __init__(self, arquivo):
        self.__arquivo = arquivo

    def salvar(self, usuarios):

        self.__criar_diretorio()

        dados = []

        for usuario in usuarios:
            dados.append({
                "nome": usuario.nome
            })

        with open(
            self.__arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):

        if not os.path.exists(self.__arquivo):
            return []

        with open(
            self.__arquivo,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        usuarios = []

        for item in dados:
            usuario = Usuario(item["nome"])
            usuarios.append(usuario)

        return usuarios

    def __criar_diretorio(self):

        diretorio = os.path.dirname(
            self.__arquivo
        )

        if diretorio:
            os.makedirs(
                diretorio,
                exist_ok=True
            )
```

---

## `persistencia/emprestimo_persistencia.py`

Como o empréstimo possui relações com `Livro` e `Usuario`, armazenamos referências aos dados que permitem localizar esses objetos posteriormente.

```python
import json
import os

from modelos import Emprestimo

class EmprestimoPersistencia:

    def __init__(self, arquivo):
        self.__arquivo = arquivo

    def salvar(self, emprestimos):

        self.__criar_diretorio()

        dados = []

        for emprestimo in emprestimos:
            dados.append({
                "livro": emprestimo.livro.titulo,
                "usuario": emprestimo.usuario.nome
            })

        with open(
            self.__arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self, livros, usuarios):

        if not os.path.exists(self.__arquivo):
            return []

        with open(
            self.__arquivo,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        emprestimos = []

        for item in dados:

            livro = self.__buscar_livro(
                livros,
                item["livro"]
            )

            usuario = self.__buscar_usuario(
                usuarios,
                item["usuario"]
            )

            if livro is None or usuario is None:
                continue

            emprestimo = Emprestimo(
                usuario,
                livro
            )

            emprestimos.append(emprestimo)

        return emprestimos

    def __buscar_livro(
        self,
        livros,
        titulo
    ):
        for livro in livros:
            if livro.titulo == titulo:
                return livro

        return None

    def __buscar_usuario(
        self,
        usuarios,
        nome
    ):
        for usuario in usuarios:
            if usuario.nome == nome:
                return usuario

        return None

    def __criar_diretorio(self):

        diretorio = os.path.dirname(
            self.__arquivo
        )

        if diretorio:
            os.makedirs(
                diretorio,
                exist_ok=True
            )
```

---

## `persistencia/__init__.py`

```python
from persistencia.livro_persistencia import (
    LivroPersistencia
)

from persistencia.usuario_persistencia import (
    UsuarioPersistencia
)

from persistencia.emprestimo_persistencia import (
    EmprestimoPersistencia
)

__all__ = [
    "LivroPersistencia",
    "UsuarioPersistencia",
    "EmprestimoPersistencia"
]
```

---

# 5. Interface

A estrutura anterior de menus e telas é preservada.

## `interface/menu.py`

```python
from abc import ABC, abstractmethod

class Menu(ABC):

    def executar(self):

        while True:

            self.exibir_opcoes()

            opcao = input(
                "Escolha uma opção: "
            )

            continuar = self.processar_opcao(
                opcao
            )

            if not continuar:
                break

    @abstractmethod
    def exibir_opcoes(self):
        pass

    @abstractmethod
    def processar_opcao(self, opcao):
        pass
```

---

## `interface/telas/tela.py`

```python
from abc import ABC, abstractmethod

class Tela(ABC):

    def exibir(self, dados):

        self.exibir_titulo()

        self.exibir_conteudo(dados)

        input(
            "\nPressione ENTER para continuar..."
        )

    def sucesso(self, mensagem):

        self.__alerta(
            "SUCESSO",
            mensagem
        )

    def erro(self, mensagem):

        self.__alerta(
            "ERRO",
            mensagem
        )

    def aviso(self, mensagem):

        self.__alerta(
            "AVISO",
            mensagem
        )

    def __alerta(
        self,
        tipo,
        mensagem
    ):

        print(
            f"\n[{tipo}] {mensagem}"
        )

    @abstractmethod
    def exibir_titulo(self):
        pass

    @abstractmethod
    def exibir_conteudo(self, dados):
        pass
```

---

## `interface/telas/tela_livros.py`

```python
from interface.telas.tela import Tela

class TelaLivros(Tela):

    def exibir_titulo(self):
        print("\n=== LIVROS ===")

    def exibir_conteudo(self, livros):

        if not livros:
            self.aviso(
                "Nenhum livro cadastrado."
            )
            return

        for indice, livro in enumerate(
            livros,
            start=1
        ):
            print(
                f"{indice} - {livro.titulo}"
            )
```

---

## `interface/telas/tela_usuarios.py`

```python
from interface.telas.tela import Tela

class TelaUsuarios(Tela):

    def exibir_titulo(self):
        print("\n=== USUÁRIOS ===")

    def exibir_conteudo(self, usuarios):

        if not usuarios:
            self.aviso(
                "Nenhum usuário cadastrado."
            )
            return

        for indice, usuario in enumerate(
            usuarios,
            start=1
        ):
            print(
                f"{indice} - {usuario.nome}"
            )
```

---

## `interface/telas/tela_emprestimos.py`

```python
from interface.telas.tela import Tela

class TelaEmprestimos(Tela):

    def exibir_titulo(self):
        print("\n=== EMPRÉSTIMOS ===")

    def exibir_conteudo(
        self,
        emprestimos
    ):

        if not emprestimos:
            self.aviso(
                "Nenhum empréstimo ativo."
            )
            return

        for indice, emprestimo in enumerate(
            emprestimos,
            start=1
        ):
            print(
                f"{indice} - "
                f"Livro: {emprestimo.livro.titulo} | "
                f"Usuário: {emprestimo.usuario.nome}"
            )
```

---

## `interface/telas/__init__.py`

```python
from interface.telas.tela import Tela
from interface.telas.tela_livros import TelaLivros
from interface.telas.tela_usuarios import TelaUsuarios
from interface.telas.tela_emprestimos import (
    TelaEmprestimos
)

__all__ = [
    "Tela",
    "TelaLivros",
    "TelaUsuarios",
    "TelaEmprestimos"
]
```

---

# 6. Menus

## `interface/menus/menu_livros.py`

```python
from interface.menu import Menu
from interface.telas import TelaLivros

class MenuLivros(Menu):

    def __init__(self, livro_service):

        self.__service = livro_service
        self.__tela = TelaLivros()

    def exibir_opcoes(self):

        print("\n=== LIVROS ===")
        print("1 - Cadastrar livro")
        print("2 - Listar livros")
        print("3 - Buscar livro")
        print("4 - Remover livro")
        print("0 - Voltar")

    def processar_opcao(self, opcao):

        try:

            if opcao == "1":

                titulo = input(
                    "Título do livro: "
                )

                livro = self.__service.cadastrar(
                    titulo
                )

                self.__tela.sucesso(
                    f"Livro '{livro.titulo}' "
                    "cadastrado."
                )

            elif opcao == "2":

                livros = self.__service.listar()

                self.__tela.exibir(livros)

            elif opcao == "3":

                titulo = input(
                    "Título do livro: "
                )

                livro = self.__service.buscar(
                    titulo
                )

                if livro is None:
                    self.__tela.erro(
                        "Livro não encontrado."
                    )
                else:
                    self.__tela.exibir(
                        [livro]
                    )

            elif opcao == "4":

                titulo = input(
                    "Título do livro: "
                )

                self.__service.remover(titulo)

                self.__tela.sucesso(
                    "Livro removido."
                )

            elif opcao == "0":

                return False

            else:

                self.__tela.erro(
                    "Opção inválida."
                )

        except ValueError as erro:

            self.__tela.erro(str(erro))

        return True
```

---

## `interface/menus/menu_usuarios.py`

```python
from interface.menu import Menu
from interface.telas import TelaUsuarios

class MenuUsuarios(Menu):

    def __init__(self, usuario_service):

        self.__service = usuario_service
        self.__tela = TelaUsuarios()

    def exibir_opcoes(self):

        print("\n=== USUÁRIOS ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Buscar usuário")
        print("4 - Remover usuário")
        print("0 - Voltar")

    def processar_opcao(self, opcao):

        try:

            if opcao == "1":

                nome = input(
                    "Nome do usuário: "
                )

                usuario = self.__service.cadastrar(
                    nome
                )

                self.__tela.sucesso(
                    f"Usuário '{usuario.nome}' "
                    "cadastrado."
                )

            elif opcao == "2":

                usuarios = self.__service.listar()

                self.__tela.exibir(usuarios)

            elif opcao == "3":

                nome = input(
                    "Nome do usuário: "
                )

                usuario = self.__service.buscar(
                    nome
                )

                if usuario is None:
                    self.__tela.erro(
                        "Usuário não encontrado."
                    )
                else:
                    self.__tela.exibir(
                        [usuario]
                    )

            elif opcao == "4":

                nome = input(
                    "Nome do usuário: "
                )

                self.__service.remover(nome)

                self.__tela.sucesso(
                    "Usuário removido."
                )

            elif opcao == "0":

                return False

            else:

                self.__tela.erro(
                    "Opção inválida."
                )

        except ValueError as erro:

            self.__tela.erro(str(erro))

        return True
```

---

## `interface/menus/menu_emprestimos.py`

```python
from interface.menu import Menu
from interface.telas import TelaEmprestimos

class MenuEmprestimos(Menu):

    def __init__(self, emprestimo_service):

        self.__service = emprestimo_service
        self.__tela = TelaEmprestimos()

    def exibir_opcoes(self):

        print("\n=== EMPRÉSTIMOS ===")
        print("1 - Realizar empréstimo")
        print("2 - Listar empréstimos")
        print("3 - Devolver livro")
        print("0 - Voltar")

    def processar_opcao(self, opcao):

        try:

            if opcao == "1":

                titulo = input(
                    "Título do livro: "
                )

                nome = input(
                    "Nome do usuário: "
                )

                emprestimo = (
                    self.__service.emprestar(
                        titulo,
                        nome
                    )
                )

                self.__tela.sucesso(
                    "Empréstimo realizado: "
                    f"{emprestimo.livro.titulo} "
                    f"para {emprestimo.usuario.nome}."
                )

            elif opcao == "2":

                emprestimos = (
                    self.__service.listar()
                )

                self.__tela.exibir(
                    emprestimos
                )

            elif opcao == "3":

                titulo = input(
                    "Título do livro: "
                )

                emprestimo = (
                    self.__service.devolver(
                        titulo
                    )
                )

                self.__tela.sucesso(
                    f"Livro '{emprestimo.livro.titulo}' "
                    "devolvido."
                )

            elif opcao == "0":

                return False

            else:

                self.__tela.erro(
                    "Opção inválida."
                )

        except ValueError as erro:

            self.__tela.erro(str(erro))

        return True
```

---

## `interface/menus/menu_principal.py`

O menu principal recebe os três serviços e organiza os submenus.

```python
from interface.menu import Menu
from interface.menus.menu_livros import MenuLivros
from interface.menus.menu_usuarios import MenuUsuarios
from interface.menus.menu_emprestimos import (
    MenuEmprestimos
)

class MenuPrincipal(Menu):

    def __init__(
        self,
        livro_service,
        usuario_service,
        emprestimo_service
    ):

        self.__menu_livros = MenuLivros(
            livro_service
        )

        self.__menu_usuarios = MenuUsuarios(
            usuario_service
        )

        self.__menu_emprestimos = (
            MenuEmprestimos(
                emprestimo_service
            )
        )

    def exibir_opcoes(self):

        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1 - Livros")
        print("2 - Usuários")
        print("3 - Empréstimos")
        print("0 - Sair")

    def processar_opcao(self, opcao):

        if opcao == "1":

            self.__menu_livros.executar()

        elif opcao == "2":

            self.__menu_usuarios.executar()

        elif opcao == "3":

            self.__menu_emprestimos.executar()

        elif opcao == "0":

            print(
                "\nEncerrando sistema..."
            )

            return False

        else:

            print(
                "\n[ERRO] Opção inválida."
            )

        return True
```

---

## `interface/menus/__init__.py`

```python
from interface.menus.menu_principal import (
    MenuPrincipal
)

from interface.menus.menu_livros import (
    MenuLivros
)

from interface.menus.menu_usuarios import (
    MenuUsuarios
)

from interface.menus.menu_emprestimos import (
    MenuEmprestimos
)

__all__ = [
    "MenuPrincipal",
    "MenuLivros",
    "MenuUsuarios",
    "MenuEmprestimos"
]
```

---

# 7. Compatibilidade com a estrutura anterior

Como a estrutura anterior possuía também:

```
interface/menu_principal.py
```

podemos utilizá-lo apenas como ponto de acesso ao menu principal.

## `interface/menu_principal.py`

```python
from interface.menus.menu_principal import (
    MenuPrincipal
)

__all__ = [
    "MenuPrincipal"
]
```

Assim, continuamos podendo utilizar:

```python
from interface import MenuPrincipal
```

sem duplicar a implementação.

---

## `interface/__init__.py`

```python
from interface.menu import Menu
from interface.menu_principal import MenuPrincipal

__all__ = [
    "Menu",
    "MenuPrincipal"
]
```

---

# 8. Ponto de entrada

## `main.py`

O `main.py` permanece pequeno. Ele apenas cria a aplicação, obtém os serviços e inicia o menu.

```python
from aplicacao import Biblioteca

from persistencia import (
    LivroPersistencia,
    UsuarioPersistencia,
    EmprestimoPersistencia
)

from servicos import (
    LivroService,
    UsuarioService,
    EmprestimoService
)

from interface import MenuPrincipal

def main():

    livro_persistencia = LivroPersistencia(
        "dados/livros.json"
    )

    usuario_persistencia = UsuarioPersistencia(
        "dados/usuarios.json"
    )

    emprestimo_persistencia = (
        EmprestimoPersistencia(
            "dados/emprestimos.json"
        )
    )

    biblioteca = Biblioteca(
        livro_persistencia,
        usuario_persistencia,
        emprestimo_persistencia
    )

    livro_service = LivroService(
        biblioteca
    )

    usuario_service = UsuarioService(
        biblioteca
    )

    emprestimo_service = EmprestimoService(
        biblioteca
    )

    menu = MenuPrincipal(
        livro_service,
        usuario_service,
        emprestimo_service
    )

    menu.executar()

if __name__ == "__main__":
    main()
```

### Resultado da arquitetura

O fluxo final de uma operação fica bem definido:

```
                    USUÁRIO
                       │
                       ▼
                    MENUS
                       │
                       ▼
                    SERVIÇO
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
          REGRAS            APLICAÇÃO
                                │
                                ▼
                             MODELOS
                                │
                                ▼
                          PERSISTÊNCIA
                                │
                                ▼
                              JSON
```

Por exemplo, ao realizar um empréstimo:

```
MenuEmprestimos
       │
       ▼
EmprestimoService
       │
       ├── procura o livro
       ├── verifica se existe
       ├── procura o usuário
       ├── verifica se existe
       ├── verifica se o livro
       │   já está emprestado
       │
       ▼
    Emprestimo
       │
       ▼
    Biblioteca
       │
       ▼
emprestimos.json
```

Isso concretiza a principal evolução apresentada no capítulo: **a interface não contém regras de negócio, os modelos não conhecem a interface, os serviços não manipulam diretamente os arquivos e a persistência não decide as regras do sistema**.

A estrutura também deixa o projeto preparado para a próxima evolução indicada na conclusão do capítulo: substituir a persistência em JSON por uma camada baseada em **ORM**, mantendo, tanto quanto possível, os serviços e a interface independentes da tecnologia utilizada para armazenamento.