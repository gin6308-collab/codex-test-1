# codex-test-1

## Task Breakdown ChatGPT App

This repository hosts a simple ChatGPT app that collects a single task description and asks the OpenAI Responses API to generate a set of actionable subtasks with guidance. The app is defined using the ChatGPT Apps SDK and can be run locally or deployed to ChatGPT.

### Prerequisites

- Python 3.9+
- An OpenAI API key with access to the Responses API (`OPENAI_API_KEY`).
- The ChatGPT Apps SDK and CLI (installed via `pip`).

### Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install chatgpt-apps-sdk openai
   ```
3. Export your OpenAI API key so the SDK can authenticate requests:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

### Running the local development server

Use the ChatGPT Apps SDK development server to test the app locally:

```bash
chatgpt-apps dev
```

The CLI watches the manifest (`app/manifest.yaml`) and the entry point (`app/main.py`) for changes. Once running, you can connect the local session to ChatGPT using the URL displayed in the terminal.

### Deploying the app to ChatGPT

1. Authenticate the ChatGPT Apps CLI (only required once):
   ```bash
   chatgpt-apps login
   ```
2. Validate the manifest:
   ```bash
   chatgpt-apps validate
   ```
3. Publish the app:
   ```bash
   chatgpt-apps deploy
   ```

The deployment process uploads the manifest and app bundle so that the Task Breakdown Assistant is available inside ChatGPT.

### Testing the handler locally

Automated tests validate that the `break_down_task` handler produces the structure expected by the ChatGPT Apps SDK without
contacting the OpenAI API. Install the testing dependency and execute the test suite:

```bash
pip install pytest
pytest
```

The tests monkeypatch the OpenAI client so you can verify the handler logic in environments without network access or an API
key.
