import pytest

pytest.importorskip("pydantic", exc_type=ImportError)

import main


def test_main_deve_executar_bot_1(monkeypatch: pytest.MonkeyPatch) -> None:
    chamado = {"bot_1": 0}

    monkeypatch.setattr(main, "BOT", "1")
    monkeypatch.setattr(main, "bot_1", lambda: chamado.__setitem__("bot_1", chamado["bot_1"] + 1))
    monkeypatch.setattr(main, "bot_2", lambda: None)

    main.main()

    assert chamado["bot_1"] == 1


def test_main_deve_executar_bot_2(monkeypatch: pytest.MonkeyPatch) -> None:
    chamado = {"bot_2": 0}

    monkeypatch.setattr(main, "BOT", "2")
    monkeypatch.setattr(main, "bot_1", lambda: None)
    monkeypatch.setattr(main, "bot_2", lambda: chamado.__setitem__("bot_2", chamado["bot_2"] + 1))

    main.main()

    assert chamado["bot_2"] == 1


def test_main_deve_lancar_erro_para_bot_nao_mapeado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "BOT", "99")

    with pytest.raises(ValueError, match="nao mapeado|mapeado"):
        main.main()


def test_main_deve_relancar_erro_inesperado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "BOT", "1")

    def _falha() -> None:
        raise RuntimeError("falha de execucao")

    monkeypatch.setattr(main, "bot_1", _falha)

    with pytest.raises(RuntimeError, match="falha de execucao"):
        main.main()
