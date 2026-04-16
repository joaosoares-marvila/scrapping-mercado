import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv(override=True)

def carregar_variavel_ambiente(
    chave: str,
    obrigatoria: bool = True,
    padrao: str | None = None,
) -> str | None:
    """Carrega e valida uma variavel de ambiente.

    Args:
        chave: Nome da variavel de ambiente a ser carregada.
        obrigatoria: Define se a variavel e obrigatoria. Se True, lanca excecao
            se nao encontrada e nao houver padrao.
        padrao: Valor padrao a retornar se a variavel nao estiver definida
            e nao for obrigatoria.

    Returns:
        str | None: Valor da variavel de ambiente ou o valor padrao.

    Raises:
        ValueError: Quando a variavel obrigatoria nao esta definida e sem padrao.
        Exception: Para quaisquer erros inesperados ao carregar a variavel.
    """
    try:
        logger.info(f"Carregando variavel de ambiente '{chave}'")
        valor = os.getenv(chave)

        if valor is None:
            if obrigatoria and padrao is None:
                mensagem = (
                    f"A variavel de ambiente '{chave}' nao esta definida. "
                    "Por favor, defina-a para continuar."
                )
                logger.error(mensagem)
                raise ValueError(mensagem)

            valor = padrao
            if valor is not None:
                logger.info(f"Usando valor padrao para variavel '{chave}'")
            else:
                logger.warning(f"Variavel '{chave}' nao definida e sem padrao")

        else:
            logger.info(f"Variavel de ambiente '{chave}' carregada com sucesso")

        return valor

    except ValueError:
        raise

    except Exception as e:
        raise Exception(
            f"Erro inesperado ao carregar variavel de ambiente '{chave}' "
            f"| Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | Linha do erro: {e.__traceback__.tb_lineno}"
        )



