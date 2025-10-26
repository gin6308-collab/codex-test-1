"""Tests for the task breakdown handler."""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path
from typing import Any, Callable, List

import pytest


sys.path.append(str(Path(__file__).resolve().parents[1]))

sdk_module = types.ModuleType("chatgpt_apps_sdk")


class _App:
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - simple stub
        self.views = {}
        self.handlers = {}

    def view(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.views[name] = func
            return func

        return decorator

    def handler(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.handlers[name] = func
            return func

        return decorator


sdk_module.App = _App
sys.modules.setdefault("chatgpt_apps_sdk", sdk_module)

openai_module = types.ModuleType("openai")


class _OpenAI:
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - simple stub
        pass


openai_module.OpenAI = _OpenAI
sys.modules.setdefault("openai", openai_module)

import app.main as main  # noqa: E402  (import after path adjustment)


class _StubContent:
    def __init__(self, text: str) -> None:
        self.text = text


class _StubItem:
    def __init__(self, content: List[_StubContent]) -> None:
        self.content = content


class _StubResponse:
    def __init__(self, output: List[_StubItem]) -> None:
        self.output = output


@pytest.fixture
def mock_responses_create(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the OpenAI client used by the handler."""

    class _Responses:
        @staticmethod
        def create(**_: Any) -> _StubResponse:
            payload = {
                "subtasks": [
                    {"title": "Subtask A", "guidance": "Do A first."},
                    {"title": "Subtask B", "guidance": "Then handle B."},
                ]
            }
            return _StubResponse([_StubItem([_StubContent(json.dumps(payload))])])

    stub_client = type("_StubClient", (), {"responses": _Responses})()

    monkeypatch.setattr(main, "_get_client", lambda: stub_client)


def test_break_down_task_returns_list(mock_responses_create: None) -> None:
    request = {"inputs": {"task": "Organize an event"}}

    result = main.break_down_task(request)

    assert result["type"] == "list"
    assert result["title"] == "Suggested subtasks"
    assert result["items"] == [
        {"title": "Subtask A", "body": "Do A first."},
        {"title": "Subtask B", "body": "Then handle B."},
    ]
    assert result["raw"] == [
        {"title": "Subtask A", "guidance": "Do A first."},
        {"title": "Subtask B", "guidance": "Then handle B."},
    ]


def test_break_down_task_requires_task_input() -> None:
    with pytest.raises(ValueError):
        main.break_down_task({"inputs": {"task": "   "}})

    with pytest.raises(ValueError):
        main.break_down_task({})
