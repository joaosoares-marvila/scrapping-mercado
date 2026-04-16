@echo off
setlocal

REM Executar da raiz do projeto.
uv run --extra dev pytest -q %*

endlocal
