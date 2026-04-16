# Scrapping Mercado

Projeto em Python para busca automatizada de produtos em sites de mercados usando Selenium.

Atualmente o projeto possui dois bots:
- Bot 1: Extrabom
- Bot 2: Perim

## Tecnologias

- Python 3.13+
- Selenium
- Pydantic
- Loguru
- python-dotenv

## Estrutura do Projeto

```text
main.py
src/
	bots/
		bot_1/
			apps/
				extrabom_web.py
			bot.py
		bot_2/
			apps/
				perim_web.py
			bot.py
	common/
		configs/
			env.py
		schemas/
			produto_mercado_schema.py
		utils/
			criar_webdriver.py
			variavel_ambiente.py
```

## Configuracao de Ambiente

1. Crie um arquivo `.env` na raiz do projeto.
2. Defina a variavel `BOT` com o valor do bot desejado.

Exemplo:

```env
BOT=1
```

Valores aceitos para `BOT`:
- `1`: executa o bot do Extrabom
- `2`: executa o bot do Perim

## Instalacao

Com `uv`:

```bash
uv sync
```

Ou com `pip`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Execucao

Opcao 1, executando o arquivo principal:

```bash
python main.py
```

Opcao 2, usando o script definido no pyproject:

```bash
scrapping-mercado
```

## Retorno Padronizado

As buscas retornam um schema Pydantic com os campos:
- `nome_mercado`
- `termo_pesquisa`
- `titulo`
- `valor` (convertido para float)
- `link`

## Observacoes

- O projeto depende de Chrome instalado e driver compativel com a versao do navegador.
- Em caso de timeout ou falhas de selenium, os erros sao registrados com modulo e linha para facilitar debug.
