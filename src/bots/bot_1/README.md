# Bot 1 - Extrabom

Este bot automatiza a busca de produtos no site do Extrabom usando Selenium.

## Arquivos Principais

- `bot.py`: orquestra a execucao do bot, cria/fecha o webdriver e processa lista de produtos.
- `apps/extrabom_web.py`: camada de interacao com o site (abrir pagina, buscar produto e extrair dados).

## Fluxo de Execucao

1. Cria o webdriver com `criar_webdriver()`.
2. Abre a tela inicial do Extrabom.
3. Para cada produto:
   - preenche campo de busca
   - dispara pesquisa
   - extrai titulo, valor e link
4. Converte os dados para `ProdutoMercadoSchema`.
5. Fecha o driver com seguranca no bloco `finally`.

## Seletores Utilizados

- Campo de busca: `//input[@class='search-input']`
- Botao de pesquisa: `//div[@id='header']//input[contains(@class, 'icon-search')]`
- Titulo: `//div[@class='name-produto']`
- Valor: `//strong[@class='item-por__val']`
- Link: `//a[@class='carousel__box__dados']`

## Como Executar Este Bot

Opcao 1 (via variavel de ambiente no projeto):

```env
BOT=1
```

Em seguida:

```bash
python main.py
```

Opcao 2 (chamada direta da funcao em script Python):

```python
from src.bots.bot_1.bot import bot_1

bot_1(["Arroz", "Feijao", "Macarrao"])
```

## Tratamento de Erros

- Erros de timeout e erros inesperados sao tratados em `apps/extrabom_web.py`.
- Em caso de erro, a mensagem inclui modulo e linha.
- O fechamento do navegador e protegido com `contextlib.suppress(Exception)`.
