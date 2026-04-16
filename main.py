from loguru import logger

from src.bots.bot_1.bot import bot_1
from src.bots.bot_2.bot import bot_2
from src.common.configs.env import BOT


def main() -> None:
    """Funcao principal que executa o bot selecionado via variavel de ambiente.

    Raises:
        ValueError: Quando o valor de BOT nao corresponde aos bots disponiveis.
    """
    try:
        logger.info(f"Iniciando execucao com BOT: {BOT}")

        match BOT:
            case "1":
                bot_1()

            case "2":
                bot_2()

            case _:
                raise ValueError(f"Bot {BOT} nÃ£o mapeado.")

    except ValueError:
        raise

    except Exception as e:
        logger.error(
            f"Erro inesperado ao executar o bot | Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | "
            f"Linha do erro: {e.__traceback__.tb_lineno}"
        )
        raise


if __name__ == "__main__":
    main()



