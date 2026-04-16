from pathlib import Path

import pytest
from selenium import webdriver

from src.common.utils.criar_webdriver import criar_webdriver


class _DriverFalso:
    pass


def test_deve_chamar_chrome_com_opcoes(monkeypatch: pytest.MonkeyPatch) -> None:
    chamado: dict[str, webdriver.ChromeOptions] = {}

    def _chrome_falso(*, options: webdriver.ChromeOptions) -> _DriverFalso:
        chamado["options"] = options
        return _DriverFalso()

    monkeypatch.setattr(webdriver, "Chrome", _chrome_falso)

    driver = criar_webdriver(headless=True)

    assert isinstance(driver, _DriverFalso)
    assert "options" in chamado


def test_deve_criar_diretorio_de_download(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    destino = tmp_path / "downloads_teste"

    def _chrome_falso(*, options: webdriver.ChromeOptions) -> _DriverFalso:
        return _DriverFalso()

    monkeypatch.setattr(webdriver, "Chrome", _chrome_falso)

    criar_webdriver(diretorio_downloads=destino)

    assert destino.exists()
    assert destino.is_dir()
