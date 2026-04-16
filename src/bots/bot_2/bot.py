import contextlib

from loguru import logger

from src.bots.bot_2.apps.perim_web import PerimWeb
from src.common.utils import criar_webdriver


def bot_2(produtos_pesquisar: list[str] = None) -> None:
    """Executa o bot 2 para buscar produtos no Perim.

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
        perim_web = PerimWeb(driver=driver)
        perim_web.abrir_tela_inicial()

        for produto_pesquisar in produtos_pesquisar:
            try:
                produto_mercado = perim_web.buscar_produto(nome_produto=produto_pesquisar)
                logger.success(f"Produto encontrado no Perim: {produto_mercado}")

            except Exception as e:
                logger.error(f"Erro ao buscar o produto '{produto_pesquisar}': {e}")

    except Exception as e:
        raise Exception(
            f"Erro inesperado no bot 2 | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
            f"Linha do erro: {e.__traceback__.tb_lineno}"
        )

    finally:
        if driver is not None:
            with contextlib.suppress(Exception):
                logger.info("Fechando o driver do Chrome")
                driver.quit()
                logger.info("Driver do Chrome fechado com sucesso")


