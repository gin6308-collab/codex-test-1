"""Task breakdown ChatGPT app entry point."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from chatgpt_apps_sdk import App
from openai import OpenAI

app = App(
    name="Task Breakdown Assistant",
    description="Collect a single task description and return a set of subtasks with guidance.",
    version="0.1.0",
)


_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Return a cached OpenAI client instance."""

    global _client
    if _client is None:
        _client = OpenAI()
    return _client


@app.view("task_breakdown_form")
def task_breakdown_form() -> Dict[str, Any]:
    """Return the form definition that collects the task description."""
    return {
        "type": "form",
        "title": "Break down a task",
        "description": "Provide a task and the assistant will suggest subtasks with helpful guidance.",
        "fields": [
            {
                "name": "task",
                "title": "Task description",
                "type": "string",
                "required": True,
                "placeholder": "Plan a team offsite",
            }
        ],
        "submit_button_label": "Break down task",
        "handler": "break_down_task",
    }


@app.handler("break_down_task")
def break_down_task(request: Dict[str, Any]) -> Dict[str, Any]:
    """Use the OpenAI Responses API to produce a structured task breakdown."""
    task = request.get("inputs", {}).get("task", "").strip()
    if not task:
        raise ValueError("The task field is required.")

    client = _get_client()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are an expert project planner. Break the provided task into 3-7 "
                            "actionable subtasks. For each subtask provide a concise title and "
                            "a short paragraph of guidance.")
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Task: "
                            + task
                            + "\n\nRespond with JSON that matches the schema named task_breakdown."
                        ),
                    }
                ],
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "task_breakdown",
                "schema": {
                    "type": "object",
                    "properties": {
                        "subtasks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "guidance": {"type": "string"},
                                },
                                "required": ["title", "guidance"],
                                "additionalProperties": False,
                            },
                            "minItems": 1,
                        }
                    },
                    "required": ["subtasks"],
                    "additionalProperties": False,
                },
            },
        },
    )

    json_payload = response.output[0].content[0].text
    data = json.loads(json_payload)

    subtasks: List[Dict[str, str]] = data.get("subtasks", [])

    return {
        "type": "list",
        "title": "Suggested subtasks",
        "items": [
            {
                "title": item.get("title", "Subtask"),
                "body": item.get("guidance", ""),
            }
            for item in subtasks
        ],
        "raw": subtasks,
    }


__all__ = ["app", "break_down_task"]
