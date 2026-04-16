from pathlib import Path

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def criar_webdriver(
    headless: bool = False,
    diretorio_downloads: str | Path | None = None,
) -> webdriver.Chrome:
    """Cria e retorna uma instancia configurada do WebDriver do Chrome.

    Args:
        headless: Define se o navegador deve iniciar sem interface grafica.
        diretorio_downloads: Caminho para o diretorio de downloads do navegador.
            Quando nao informado, o Chrome usa o diretorio padrao do sistema.

    Returns:
        webdriver.Chrome: Instancia configurada do driver do Chrome.

    Raises:
        PermissionError: Quando nao ha permissao para criar o diretorio de downloads.
        WebDriverException: Quando ocorre erro ao inicializar o WebDriver do Chrome.
        Exception: Para quaisquer erros inesperados durante a criacao da instancia.
    """
    try:
        logger.info("Iniciando criacao da instancia do WebDriver do Chrome")

        opcoes = webdriver.ChromeOptions()

        if headless:
            opcoes.add_argument("--headless=new")

        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])

        preferencias: dict[str, str | bool] = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }

        if diretorio_downloads is not None:
            try:
                caminho_download = Path(diretorio_downloads).expanduser().resolve()
                caminho_download.mkdir(parents=True, exist_ok=True)
                preferencias["download.default_directory"] = str(caminho_download)
                logger.info(f"Diretorio de downloads configurado: {caminho_download}")

            except PermissionError as e:
                raise PermissionError(
                    f"Sem permissao para criar o diretorio de downloads | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
                    f"Linha do erro: {e.__traceback__.tb_lineno}"
                )

        opcoes.add_experimental_option("prefs", preferencias)

        driver = webdriver.Chrome(options=opcoes)
        logger.info("WebDriver do Chrome criado com sucesso")

        return driver

    except PermissionError:
        raise

    except WebDriverException as e:
        raise WebDriverException(
            f"Erro ao inicializar o WebDriver do Chrome | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
            f"Linha do erro: {e.__traceback__.tb_lineno}"
        )

    except Exception as e:
        raise Exception(
            f"Erro inesperado ao criar a instancia do WebDriver | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
            f"Linha do erro: {e.__traceback__.tb_lineno}"
        )



