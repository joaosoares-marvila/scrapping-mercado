# Bot 2 - Perim

Este bot automatiza a busca de produtos no site do Perim usando Selenium.

## Arquivos Principais

- `bot.py`: orquestra a execucao do bot, cria/fecha o webdriver e processa lista de produtos.
- `apps/perim_web.py`: camada de interacao com o site (buscar produto e extrair dados).

## Fluxo de Execucao

1. Cria o webdriver com `criar_webdriver()`.
2. Para cada produto:
   - abre a pagina do Perim
   - preenche campo de busca
   - dispara pesquisa
   - extrai titulo, valor e link
3. Converte os dados para `ProdutoMercadoSchema`.
4. Fecha o driver com seguranca no bloco `finally`.

## Seletores Utilizados

- Campo de busca: `//input[@id='inputBuscaRapida']`
- Botao de pesquisa: `//button[@class='btn btn-search']`
- Titulo: `//p[contains(@class, 'text-success description')]`
- Valor: `//div[contains(@class, 'info-price ng-star-inserted')]`
- Link: `//a[@class='ghost-link clearfix']`

## Como Executar Este Bot

Opcao 1 (via variavel de ambiente no projeto):

```env
BOT=2
```

Em seguida:

```bash
python main.py
```

Opcao 2 (chamada direta da funcao em script Python):

```python
from src.bots.bot_2.bot import bot_2

bot_2(["Arroz", "Feijao", "Macarrao"])
```

## Tratamento de Erros

- Erros de timeout e erros inesperados sao tratados em `apps/perim_web.py`.
- Em caso de erro, a mensagem inclui modulo e linha.
- O fechamento do navegador e protegido com `contextlib.suppress(Exception)`.
