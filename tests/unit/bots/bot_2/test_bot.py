import pytest

pytest.importorskip("pydantic", exc_type=ImportError)

from src.bots.bot_2 import bot as bot_mod


class _DriverFalso:
    def __init__(self) -> None:
        self.quit_chamado = False

    def quit(self) -> None:
        self.quit_chamado = True


class _PerimFalso:
    def __init__(self, driver: _DriverFalso) -> None:
        self.driver = driver

    def abrir_tela_inicial(self) -> None:
        return None

    def buscar_produto(self, nome_produto: str) -> dict:
        return {"nome": nome_produto}


def test_bot_2_deve_executar_e_fechar_driver(monkeypatch: pytest.MonkeyPatch) -> None:
    driver = _DriverFalso()

    monkeypatch.setattr(bot_mod, "criar_webdriver", lambda: driver)
    monkeypatch.setattr(bot_mod, "PerimWeb", _PerimFalso)

    bot_mod.bot_2(["Arroz"])

    assert driver.quit_chamado is True


def test_bot_2_deve_relancar_erro_inesperado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bot_mod, "criar_webdriver", lambda: (_ for _ in ()).throw(RuntimeError("falha")))

    with pytest.raises(Exception, match="Erro inesperado no bot 2"):
        bot_mod.bot_2(["Arroz"])
