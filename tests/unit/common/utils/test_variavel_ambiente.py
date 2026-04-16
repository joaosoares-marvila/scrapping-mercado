import pytest

from src.common.utils.variavel_ambiente import carregar_variavel_ambiente


def test_deve_retornar_valor_da_variavel(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHAVE_TESTE", "valor_ok")

    valor = carregar_variavel_ambiente("CHAVE_TESTE")

    assert valor == "valor_ok"


def test_deve_lancar_erro_quando_variavel_obrigatoria_ausente(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CHAVE_OBRIGATORIA", raising=False)

    with pytest.raises(ValueError, match="nao esta definida"):
        carregar_variavel_ambiente("CHAVE_OBRIGATORIA", obrigatoria=True)


def test_deve_retornar_padrao_quando_nao_obrigatoria(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CHAVE_COM_PADRAO", raising=False)

    valor = carregar_variavel_ambiente(
        "CHAVE_COM_PADRAO",
        obrigatoria=False,
        padrao="padrao_ok",
    )

    assert valor == "padrao_ok"
