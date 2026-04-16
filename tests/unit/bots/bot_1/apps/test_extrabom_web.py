import pytest
from selenium.common.exceptions import TimeoutException

pytest.importorskip("pydantic", exc_type=ImportError)

from src.bots.bot_1.apps import extrabom_web as extrabom_mod


class _ElementoFalso:
    def __init__(self, texto: str = "", href: str = "") -> None:
        self.text = texto
        self._href = href
        self.clicado = False
        self.textos_enviados: list[str] = []

    def click(self) -> None:
        self.clicado = True

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


def test_abrir_tela_inicial_deve_fechar_anuncio(monkeypatch: pytest.MonkeyPatch) -> None:
    botao = _ElementoFalso()
    _WaitFalso.fila = [botao]

    class _Driver:
        def __init__(self) -> None:
            self.urls: list[str] = []

        def get(self, url: str) -> None:
            self.urls.append(url)

    driver = _Driver()

    monkeypatch.setattr(extrabom_mod, "WebDriverWait", _WaitFalso)

    web = extrabom_mod.ExtrabomWeb(driver=driver)
    web.abrir_tela_inicial()

    assert driver.urls[-1] == "https://www.extrabom.com.br/"
    assert botao.clicado is True


def test_busca_deve_retornar_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    campo = _ElementoFalso()
    btn = _ElementoFalso()
    titulo = _ElementoFalso(texto="Arroz tipo 1")
    valor = _ElementoFalso(texto="R$ 10,99")
    link = _ElementoFalso(href="https://exemplo.com/produto")
    _WaitFalso.fila = [campo, btn, titulo, valor, link]

    class _Driver:
        pass

    monkeypatch.setattr(extrabom_mod, "WebDriverWait", _WaitFalso)

    web = extrabom_mod.ExtrabomWeb(driver=_Driver())
    retorno = web.buscar_produto("Arroz")

    assert retorno.nome_mercado == "Extrabom"
    assert retorno.termo_pesquisa == "Arroz"
    assert retorno.titulo == "Arroz tipo 1"
    assert retorno.valor == 10.99
    assert str(retorno.link) == "https://exemplo.com/produto"
    assert campo.textos_enviados == ["Arroz"]
    assert btn.clicado is True


def test_busca_deve_lancar_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    _WaitFalso.fila = [TimeoutException("timeout")]

    class _Driver:
        pass

    monkeypatch.setattr(extrabom_mod, "WebDriverWait", _WaitFalso)

    web = extrabom_mod.ExtrabomWeb(driver=_Driver())

    with pytest.raises(TimeoutException):
        web.buscar_produto("Arroz")
