param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PytestArgs
)

# Executar da raiz do projeto.
uv run --extra dev pytest -q @PytestArgs
