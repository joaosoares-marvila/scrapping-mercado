
import contextlib

from loguru import logger

from src.bots.bot_1.apps.extrabom_web import ExtrabomWeb
from src.common.utils.criar_webdriver import criar_webdriver


def bot_1(produtos_pesquisar: list[str] = None) -> None:
    """Executa o bot 1 para buscar produtos no Extrabom.

    Args:
        produtos_pesquisar: Lista de produtos a pesquisar. Se nao informada,
            utiliza a lista padrao.

    Raises:
        Exception: Para erros inesperados durante a execucao do bot.
    """
    driver = None

    try:
        if not produtos_pesquisar:
            produtos_pesquisar = [
                "Arroz",
                "FeijÃ£o",
                "MacarrÃ£o",
            ]

        driver = criar_webdriver()
        extrabom_web = ExtrabomWeb(driver=driver)
        extrabom_web.abrir_tela_inicial()

        for produto_pesquisar in produtos_pesquisar:
            try:
                produto_mercado = extrabom_web.buscar_produto(nome_produto=produto_pesquisar)
                logger.success(f"Produto encontrado no Extrabom: {produto_mercado}")

            except Exception as e:
                logger.error(f"Erro ao buscar o produto '{produto_pesquisar}': {e}")

    except Exception as e:
        raise Exception(
            f"Erro inesperado no bot 1 | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
            f"Linha do erro: {e.__traceback__.tb_lineno}"
        )

    finally:
        if driver is not None:
            with contextlib.suppress(Exception):
                logger.info("Fechando o driver do Chrome")
                driver.quit()
                logger.info("Driver do Chrome fechado com sucesso")

