import pytest
from selenium.common.exceptions import TimeoutException

pytest.importorskip("pydantic", exc_type=ImportError)

from src.bots.bot_2.apps import perim_web as perim_mod


class _ElementoFalso:
    def __init__(self, texto: str = "", href: str = "") -> None:
        self.text = texto
        self._href = href
        self.clicado = False
        self.textos_enviados: list[str] = []
        self.limpo = False

    def click(self) -> None:
        self.clicado = True

    def clear(self) -> None:
        self.limpo = True

    def send_keys(self, valor: str) -> None:
        self.textos_enviados.append(valor)

    def get_attribute(self, nome: str) -> str:
        if nome == "href":
            return self._href
        return ""


class _WaitFalso:
    fila: list[object] = []

    def __init__(self, _driver: object, _timeout: int) -> None:
        pass

    def until(self, _condicao: object) -> object:
        item = _WaitFalso.fila.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def test_busca_deve_retornar_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    campo = _ElementoFalso()
    btn = _ElementoFalso()
    titulo = _ElementoFalso(texto="Feijao carioca")
    valor = _ElementoFalso(texto="R$ 12,50")
    link = _ElementoFalso(href="https://exemplo.com/item")
    _WaitFalso.fila = [campo, btn, titulo, valor, link]

    class _Driver:
        def __init__(self) -> None:
            self.urls: list[str] = []

        def get(self, url: str) -> None:
            self.urls.append(url)

    driver = _Driver()
    monkeypatch.setattr(perim_mod, "WebDriverWait", _WaitFalso)

    web = perim_mod.PerimWeb(driver=driver)
    retorno = web.buscar_produto("Feijao")

    assert driver.urls[-1] == "https://www.perim.com.br/"
    assert retorno.nome_mercado == "Perim"
    assert retorno.termo_pesquisa == "Feijao"
    assert retorno.valor == 12.5
    assert campo.limpo is True
    assert campo.textos_enviados == ["Feijao"]
    assert btn.clicado is True


def test_busca_deve_lancar_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    _WaitFalso.fila = [TimeoutException("timeout")]

    class _Driver:
        def get(self, _url: str) -> None:
            return None

    monkeypatch.setattr(perim_mod, "WebDriverWait", _WaitFalso)

    web = perim_mod.PerimWeb(driver=_Driver())

    with pytest.raises(TimeoutException):
        web.buscar_produto("Feijao")
