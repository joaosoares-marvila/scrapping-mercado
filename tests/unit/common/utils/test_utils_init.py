from src.common import utils


def test_utils_deve_exportar_criar_webdriver() -> None:
    assert hasattr(utils, "criar_webdriver")


def test_utils_deve_exportar_carregar_variavel_ambiente() -> None:
    assert hasattr(utils, "carregar_variavel_ambiente")
