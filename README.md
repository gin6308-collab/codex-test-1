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

### Setting the OpenAI API key

The app expects the `OPENAI_API_KEY` environment variable to be set before you run the
SDK CLI, tests, or the Docker container.

- **macOS / other Unix shells (bash, zsh, fish)**
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```

- **NixOS** — add the export to your shell configuration (e.g., `~/.profile` or
  `~/.config/fish/config.fish`) or set it for a single session:
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```
  For system-wide availability, you can also declare it in `configuration.nix`:
  ```nix
  environment.variables.OPENAI_API_KEY = "sk-...";
  ```

- **Windows (PowerShell)**
  ```powershell
  setx OPENAI_API_KEY "sk-..."
  # Restart the terminal or use: $env:OPENAI_API_KEY = "sk-..."
  ```

- **Docker runtime**
  Pass the variable via `docker run -e OPENAI_API_KEY=...` as shown in the Docker section
  below. You can also use `--env-file` to load the key from a local `.env` file:
  ```bash
  echo "OPENAI_API_KEY=sk-..." > .env
  docker run --rm --env-file .env -p 8000:8000 task-breakdown-app
  ```

### Running the local development server

Use the ChatGPT Apps SDK development server to test the app locally:

```bash
chatgpt-apps dev
```

The CLI watches the manifest (`app/manifest.yaml`) and the entry point (`app/main.py`) for changes. Once running, you can connect the local session to ChatGPT using the URL displayed in the terminal.

### Running with Docker

You can containerize the development server to avoid installing dependencies on the host machine.

#### Platform-specific Docker setup

- **macOS**
  1. Install Docker Desktop (via the GUI download or Homebrew):
     ```bash
     brew install --cask docker
     ```
  2. Launch Docker Desktop once so it can finish initialization and provide the background daemon required for containers.

- **Windows**
  1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) and ensure WSL 2 integration is enabled during setup.
  2. Start Docker Desktop and, if prompted, sign out/sign in so the Docker CLI can connect to the daemon.

- **NixOS**
  1. Enable the Docker service in `/etc/nixos/configuration.nix`:
     ```nix
     virtualisation.docker.enable = true;
     ```
  2. Apply the configuration and add your user to the `docker` group:
     ```bash
     sudo nixos-rebuild switch
     sudo usermod -aG docker $USER
     ```
  3. Log out and log back in (or `newgrp docker`) so your shell picks up the new group membership.

Once Docker is available, use the same workflow on every platform:

1. Build the image:
   ```bash
   docker build -t task-breakdown-app .
   ```
2. Run the container, forwarding the dev server port and providing your OpenAI API key:
   ```bash
   docker run --rm -it \
     -e OPENAI_API_KEY="sk-..." \
     -p 8000:8000 \
     task-breakdown-app
   ```
3. After the container starts, follow the URL printed by `chatgpt-apps dev` to link the running instance to ChatGPT.

The container installs the ChatGPT Apps SDK, OpenAI client, and test tooling so you can run the automated suite inside the container as needed.

### Deploying the app to ChatGPT

The ChatGPT Apps CLI (`chatgpt-apps`) must be installed in the same environment where you
exported the `OPENAI_API_KEY`. The commands are the same on every platform, but the
setup varies slightly.

- **macOS**
  1. Ensure you have Python 3.9+ available (e.g., via Homebrew `brew install python@3.11`).
  2. Create/activate your virtual environment and install the SDK/CLI:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     pip install chatgpt-apps-sdk openai
     ```
  3. Export `OPENAI_API_KEY` as shown above.
  4. Authenticate and deploy:
     ```bash
     chatgpt-apps login
     chatgpt-apps validate
     chatgpt-apps deploy
     ```

- **NixOS**
  1. Enable Python tooling (e.g., `nix-shell -p python311 python311Packages.pip`).
  2. Within the shell, install dependencies locally:
     ```bash
     pip install --user chatgpt-apps-sdk openai
     ```
  3. Ensure `OPENAI_API_KEY` is exported in the shell session.
  4. Run the same CLI workflow:
     ```bash
     chatgpt-apps login
     chatgpt-apps validate
     chatgpt-apps deploy
     ```

After deployment, the manifest and app bundle are uploaded so the Task Breakdown Assistant
is available inside ChatGPT.

### Testing the handler locally

Automated tests validate that the `break_down_task` handler produces the structure expected by the ChatGPT Apps SDK without
contacting the OpenAI API. Install the testing dependency and execute the test suite:

```bash
pip install pytest
pytest
```

The tests monkeypatch the OpenAI client so you can verify the handler logic in environments without network access or an API
key.
