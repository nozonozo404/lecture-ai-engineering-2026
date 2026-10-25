from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    requests = []
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=7,
        ),
        text="回答",
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            requests.append(kwargs)
            return response

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン] 入力: 12 / 出力: 7\n"
    assert requests[0]["contents"].startswith("質問")


def test_ask_includes_matching_glossary_definition(monkeypatch):
    requests = []
    response = SimpleNamespace(usage_metadata=None, text="回答")

    class FakeModels:
        def generate_content(self, **kwargs):
            requests.append(kwargs)
            return response

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    ask_module.ask("AIE2026の講座の宿題にある「3レベル」とは何ですか？")

    contents = requests[0]["contents"]
    assert "基礎（講義内容の確認）" in contents
    assert "実装（自分でコードを書く）" in contents
    assert "発展（調査や試行）" in contents
    assert "どれか1つに取り組めばその回の宿題は完了" in contents