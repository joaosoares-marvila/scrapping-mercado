import importlib
import sys

import pytest

from src.common.utils import variavel_ambiente


@pytest.mark.parametrize("valor", ["1", "2"])
def test_env_deve_carregar_bot_pelo_helper(monkeypatch: pytest.MonkeyPatch, valor: str) -> None:
    monkeypatch.setattr(
        variavel_ambiente,
        "carregar_variavel_ambiente",
        lambda chave, obrigatoria=True, padrao=None: valor,
    )

    sys.modules.pop("src.common.configs.env", None)
    env = importlib.import_module("src.common.configs.env")

    assert env.BOT == valor
