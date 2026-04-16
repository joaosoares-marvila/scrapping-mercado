import re

from pydantic import AnyHttpUrl, BaseModel, Field, ValidationError, field_validator


class ProdutoMercadoSchema(BaseModel):
    """Representa o retorno padronizado de um produto encontrado no mercado.

    Attributes:
        nome_mercado: Nome do mercado onde o produto foi encontrado.
        termo_pesquisa: Termo utilizado para realizar a busca.
        titulo: Titulo exibido para o produto na listagem.
        valor: Valor do produto convertido para formato numerico.
        link: URL da pagina do produto.
    """

    nome_mercado: str = Field(description="Nome do mercado onde o produto foi encontrado")
    termo_pesquisa: str = Field(description="Termo pesquisado para encontrar o produto")
    titulo: str = Field(description="Titulo exibido no resultado da busca")
    valor: float = Field(description="Valor numerico do produto")
    link: AnyHttpUrl = Field(description="Link da pagina do produto")

    @field_validator("valor", mode="before")
    @classmethod
    def limpar_e_converter_valor(cls, value: object) -> float:
        """Limpa e converte o valor monetario recebido para float.

        Args:
            value: Valor bruto vindo da pagina, como texto ou numero.

        Returns:
            float: Valor numerico normalizado para uso interno.

        Raises:
            TypeError: Quando o valor nao eh string, int ou float.
            ValueError: Quando nao ha numero valido para conversao.
        """
        if isinstance(value, (int, float)):
            return float(value)

        if not isinstance(value, str):
            raise TypeError("O campo 'valor' deve ser string, int ou float")

        texto = value.strip()
        if not texto:
            raise ValueError("O campo 'valor' esta vazio")

        # Mantem apenas digitos e separadores para normalizar formatos como 'R$ 1.234,56'.
        texto = re.sub(r"[^\d,\.]", "", texto)

        if not texto:
            raise ValueError("Nao foi possivel extrair numeros do campo 'valor'")

        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")
        else:
            partes = texto.split(".")
            if len(partes) > 2:
                texto = "".join(partes[:-1]) + "." + partes[-1]

        try:
            return float(texto)
        except ValueError as exc:
            raise ValueError(f"Nao foi possivel converter o campo 'valor' para float: {value}") from exc
