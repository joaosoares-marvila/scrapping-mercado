import pytest

pydantic = pytest.importorskip("pydantic", exc_type=ImportError)
ValidationError = pydantic.ValidationError

from src.common.schemas.produto_mercado_schema import ProdutoMercadoSchema


def test_deve_converter_valor_brasileiro_para_float() -> None:
    schema = ProdutoMercadoSchema(
        nome_mercado="Extrabom",
        termo_pesquisa="Arroz",
        titulo="Arroz tipo 1",
        valor="R$ 1.234,56",
        link="https://exemplo.com/produto",
    )

    assert schema.valor == 1234.56


def test_deve_aceitar_valor_numerico_direto() -> None:
    schema = ProdutoMercadoSchema(
        nome_mercado="Perim",
        termo_pesquisa="Feijao",
        titulo="Feijao carioca",
        valor=19.9,
        link="https://exemplo.com/item",
    )

    assert schema.valor == 19.9


def test_deve_falhar_quando_valor_for_invalido() -> None:
    with pytest.raises(ValidationError):
        ProdutoMercadoSchema(
            nome_mercado="Perim",
            termo_pesquisa="Macarrao",
            titulo="Macarrao parafuso",
            valor="sem_numero",
            link="https://exemplo.com/item",
        )
